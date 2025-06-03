from base.character.interfaces import CharacterBaseInterface
from base.character.attributes import (
    CharacterSkillConstellationUpgradeAttributes,
    CharacterNormalAttackAttributes,
    CharacterEquipmentAttributes,
    CharacterEnergyAttributes,
    CharacterTalentAttributes,
    CharacterBaseAttributes,
)
from base.character.modifiers import ModifierHandler
from base.character.scalings import CharacterScalings
from base.weapon.weapon import WeaponBase
from common.enum.event import Event, LogEventType
from common.enum.heal import HealType
from common.enum.stats import CharacterStatValues, CharacterStats
from common.exception.simulation import WeaponMissingError
from common.struct.character.result import ActionResult
from common.struct.event.heal import HealEvent
from common.struct.event_data.heal import HealDetails
from common.struct.simulation.snapshot import Snapshot
from profiles.character import CharacterProfile
from common.enum.action import ActionType
from common.logger.logger import Logger
from sim.handlers.task import TaskHandler
from sim.handlers.event import EventHandler
from sim.core.core import Core


class CharacterWrapper(CharacterBaseInterface):

    logger: Logger
    event_handler: EventHandler
    task_handler: TaskHandler
    modifier_handler: ModifierHandler

    base: CharacterBaseAttributes
    talents: CharacterTalentAttributes
    constellation_upgrades: CharacterSkillConstellationUpgradeAttributes
    equipment: CharacterEquipmentAttributes
    energy: CharacterEnergyAttributes
    scalings: CharacterScalings

    has_arkhe_alignment: bool
    starting_hp: int
    starting_hp_percentage: int

    normal: CharacterNormalAttackAttributes
    base_stats: CharacterStatValues
    index: int

    def __init__(self,
                 profile: CharacterProfile | None = None,
                 frame: int | None = None,
                 logger: Logger | None = None,
                 pubsub: EventHandler | None = None,
                 task_handler: TaskHandler | None = None,
                 index: int = 0
        ) -> None:
        if profile is None or frame is None or logger is None or pubsub is None or task_handler is None:
            return

        self.base = CharacterBaseAttributes.from_profile(profile)

        self.logger = logger
        self.event_handler = pubsub
        self.task_handler = task_handler
        self.modifier_handler = ModifierHandler(frame, self.logger, self.base.name)

        self.talents = CharacterTalentAttributes(
            profile.talents.attack,
            profile.talents.skill,
            profile.talents.burst
        )
        self.constellation_upgrades = CharacterSkillConstellationUpgradeAttributes(-1, -1, -1)
        self.equipment = CharacterEquipmentAttributes(
            None,
        )
        self.energy = CharacterEnergyAttributes(0, 0, 0)

        self.has_arkhe_alignment = False
        self.starting_hp = 0
        self.starting_hp_percentage = 100

        self.normal = CharacterNormalAttackAttributes(0, 0)
        self.base_stats = {}
        self.index = index


class CharacterBase(CharacterWrapper):
    core: Core
    action_cooldown: dict[ActionType, int]
    available_charges: dict[ActionType, int]

    current_hp_percentage: float
    current_bond_of_life: float

    def __init__(self, wrapper: CharacterWrapper, core: Core):
        self.clone_wrapper_attributes(wrapper)
        self.available_charges = {}
        self.action_cooldown = {}
        self.core = core
        self.current_hp_percentage = 1
        self.current_bond_of_life = 0

    def clone_wrapper_attributes(self, wrapper: CharacterWrapper) -> None:
        self.logger = wrapper.logger
        self.event_handler = wrapper.event_handler
        self.task_handler = wrapper.task_handler

        self.base = wrapper.base
        self.talents = wrapper.talents
        self.constellation_upgrades = wrapper.constellation_upgrades
        self.equipment = wrapper.equipment
        self.energy = wrapper.energy

        self.has_arkhe_alignment = wrapper.has_arkhe_alignment
        self.starting_hp = wrapper.starting_hp
        self.starting_hp_percentage = wrapper.starting_hp_percentage

        self.normal = wrapper.normal
        self.base_stats = wrapper.base_stats
        self.modifier_handler = wrapper.modifier_handler
        self.index = wrapper.index

    def calculate_stats(self, character_profile: CharacterProfile) -> None:
        # Initialize base stats (with weapon base ATK)
        base_stats = self.get_base_stats()
        if self.equipment.weapon is None:
            raise WeaponMissingError(f"Weapon is not set for character {self.base.name}")
        base_atk = base_stats[CharacterStats.BASE_ATK] + self.equipment.weapon.get_base_atk()
        stats = CharacterStats.get_default_dict()
        stats[CharacterStats.BASE_ATK] = base_atk
        stats[CharacterStats.BASE_DEF] = base_stats[CharacterStats.BASE_DEF]
        stats[CharacterStats.BASE_HP] = base_stats[CharacterStats.BASE_HP]

        # Apply Ascension bonus
        ascension_stat, value = self.scalings.get_ascension_stat()
        stats[ascension_stat] += value

        # Apply Weapon main stat
        weapon_stat, value = self.equipment.weapon.get_main_stat()
        stats[weapon_stat] += value

        # Apply Artifact stats
        artifact_stats = character_profile.get_artifact_stats()
        self.base_stats = CharacterStats.add_dict(stats, artifact_stats)

        self.logger.event(LogEventType.CHARACTER, self.base.name, 'total-stats', name=self.base.name, arguments=self.base_stats)
        snapshot = self.snapshot()
        self.logger.event(LogEventType.CHARACTER, self.base.name, 'final-stats', name=self.base.name, arguments=snapshot)

    def snapshot(self) -> Snapshot:
        stats = self.base_stats.copy()

        if not stats:
            return Snapshot(CharacterStats.get_empty_dict(), self.base.level, self.core.frame)

        base_atk = stats.pop(CharacterStats.BASE_ATK)
        base_def = stats.pop(CharacterStats.BASE_DEF)
        base_hp = stats.pop(CharacterStats.BASE_HP)

        flat_hp_bonus = stats.pop(CharacterStats.HP)
        flat_atk_bonus = stats.pop(CharacterStats.ATK)
        flat_def_bonus = stats.pop(CharacterStats.DEF)

        percentage_hp_bonus = stats.pop(CharacterStats.HP_PERCENTAGE)
        percentage_atk_bonus = stats.pop(CharacterStats.ATK_PERCENTAGE)
        percentage_def_bonus = stats.pop(CharacterStats.DEF_PERCENTAGE)

        # TODO: Apply modifiers

        stats[CharacterStats.ATK] = base_atk * (1 + percentage_atk_bonus) + flat_atk_bonus
        stats[CharacterStats.DEF] = base_def * (1 + percentage_def_bonus) + flat_def_bonus
        stats[CharacterStats.HP] = base_hp * (1 + percentage_hp_bonus) + flat_hp_bonus

        self.logger.event(LogEventType.SNAPSHOT, self.base.name, 'snapshot', name=self.base.name, stats=stats)
        return Snapshot(stats, self.base.level, self.core.frame)

    def set_weapon(self, weapon: WeaponBase) -> None:
        self.equipment.weapon = weapon
        self.logger.info(f"Weapon set to {weapon.base.name}")

    # HP interface

    def _calculate_heal_amount(self, heal_details: HealDetails) -> tuple[float, float]:
        if heal_details.heal_type == HealType.FLAT:
            heal_amount = heal_details.amount
        elif heal_details.heal_type == HealType.PERCENTAGE:
            heal_amount = heal_details.amount * self.get_max_hp()
        incoming_healing_bonus = self.modifier_handler.get_healing_bonus()
        return heal_amount, incoming_healing_bonus

    def get_max_hp(self) -> float:
        return self.snapshot().stats[CharacterStats.HP]

    def get_current_hp(self) -> float:
        return self.current_hp_percentage * self.get_max_hp()

    def get_current_hp_percent(self) -> float:
        return self.current_hp_percentage

    def get_current_bond_of_life(self) -> float:
        return self.current_bond_of_life

    def set_hp(self, hp: float) -> None:
        max_hp = self.get_max_hp()
        hp_percentage = hp / max_hp
        self.current_hp_percentage = min(max(hp_percentage, 0), 1)
        self.logger.event(LogEventType.CHARACTER, self.base.name, 'set-hp', hp=max_hp, hp_percentage=self.current_hp_percentage)

    def modify_hp(self, hp: float) -> None:
        new_hp = self.get_current_hp() + hp
        self.set_hp(new_hp)

    def set_bond_of_life(self, bond_of_life: float) -> None:
        self.current_bond_of_life = min(max(bond_of_life, 0), self.get_max_hp() * 2)

    def modify_bond_of_life(self, bond_of_life: float) -> None:
        if bond_of_life < 0:
            return
        previous_bond_of_life = self.get_current_bond_of_life()
        self.set_bond_of_life(previous_bond_of_life + bond_of_life)
        self.core.event_handler.publish(Event.ON_HP_DEBT, self.index, previous_bond_of_life - self.current_bond_of_life)

    def heal(self, hp: HealDetails) -> ActionResult:
        heal_amount, incoming_healing_bonus = self._calculate_heal_amount(hp)

        previous_hp = self.get_current_hp()
        previous_bond_of_life = self.get_current_bond_of_life()

        heal_without_bond_of_life = heal_amount * (1 + incoming_healing_bonus)
        heal_adjusted = heal_without_bond_of_life - previous_bond_of_life
        if heal_adjusted < 0:
            heal_adjusted = 0

        heal_overflow = previous_hp + heal_adjusted - self.get_max_hp()
        if heal_overflow < 0:
            heal_adjusted = 0

        self.modify_hp(heal_adjusted)
        self.modify_bond_of_life(-heal_without_bond_of_life)

        heal_event = HealEvent(
            data=hp,
            target_index=self.index,
            heal_initial=heal_amount,
            heal_final=heal_adjusted,
            heal_overflow=heal_overflow,
        )
        self.logger.event(LogEventType.HEAL, self.base.name, 'heal', args=heal_event)
        self.event_handler.publish(Event.ON_HEAL, heal_event)
        return ActionResult(no_frames=0)

    # Energy and cooldown interface

    def set_cooldown(self, action: ActionType, frames: int) -> None:
        if frames < 0:
            raise ValueError("Cooldown frames cannot be negative")
        self.action_cooldown[action] = frames
        self.logger.event(LogEventType.CHARACTER, self.base.name, 'set-cooldown', action=action, frames=frames)

    def consume_energy(self, delay: int = 0) -> None:
        if delay > 0:
            self.task_handler.add_task(
                f'{self.base.name}-consume-energy',
                lambda: self._consume_energy_task(),
                delay
            )
        else:
            self._consume_energy_task()

    def _consume_energy_task(self) -> None:
        self.logger.event(
            LogEventType.CHARACTER, self.base.name, 'consume-energy',
            pre_consume=self.energy.energy,
            post_consume=0,
            max_energy=self.energy.max_energy,
        )
        self.energy.energy = 0