from base.character.character import CharacterBase, CharacterWrapper
from character.furina.scalings import FurinaScalings
from common.enum.action import ActionType
from common.enum.attack import AttackAdditionalType, AttackType
from common.enum.element import Element
from common.enum.icd import ICDGroup, ICDTag
from common.struct.action.info import ActionInfo
from common.struct.event.attack import AttackEvent
from common.struct.event_data.attack import AttackDetails
from common.struct.event_data.heal import HealDetails
from common.struct.event.heal import DrainEvent, HealEvent

from common.enum.stats import CharacterStats, CharacterStatValues
from common.enum.event import Event, LogEventType
from common.enum.modifier import ModifierResult
from common.enum.arkhe import Arkhe
from common.enum.heal import HealType

from common.const.const import HEAL_ALL_TARGETS, MODIFIER_PERMANENT_DURATION

from common.struct.modifier.attack import CharacterAttackModifier

from common.struct.modifier.healing_bonus import IncomingHealingBonusModifier
from common.struct.modifier.modifier import ModifierFunctionResult
from profiles.character import CharacterProfile
from sim.core.core import Core
from dataclasses import dataclass
from typing import Optional


@dataclass
class FurinaInternalData:
    fanfare_stacks: float
    max_fanfare_stacks: int
    max_fanfare_stacks_c2: int
    a4_buffs: CharacterStatValues
    a4_interval_reduction: float
    fanfare_freeze_queued: bool
    burst_buffs: CharacterStatValues
    arkhe: Arkhe

    SALON_MEMBER_KEY: str = 'Salon Member'
    A4_CHECK_INTERVAL: int = 30

    # Burst ------
    BURST_HITMARK: int = 98
    BURST_KEY: str = 'furina-burst'
    BURST_DURATION: int = int(18.2 * 60)
    BURST_COOLDOWN: int = int(15.0 * 60)
    BURST_ENERGY_CONSUME_DELAY: int = 7
    FANFARE_HP_CHANGE_TO_GAIN_DELAY: int = 6                                    # Frames from the drain to the gain of the Fanfare buff
    FANFARE_FREEZE_DURATION: int = 30 + FANFARE_HP_CHANGE_TO_GAIN_DELAY - 1   # Frames from the gain to the next gain of the Fanfare buff
    FANFARE_FREEZE_TASK_DELAY: int = 1
    FANFARE_FREEZE_KEY: str = 'furina-freeze-fanfare-gain'


class Furina(CharacterBase):

    scalings: FurinaScalings

    def __init__(self, core: Core, wrapper: CharacterWrapper, profile: CharacterProfile):
        self._data = FurinaInternalData(
            fanfare_stacks=0.0,
            max_fanfare_stacks=300,
            max_fanfare_stacks_c2=300,
            fanfare_freeze_queued=False,
            a4_buffs={},
            a4_interval_reduction=0.0,
            burst_buffs={},
            arkhe=Arkhe.OUSIA
        )
        self.scalings = FurinaScalings()
        self.clone_wrapper_attributes(wrapper)

        super().__init__(wrapper, core)

        self.energy.max_energy = 60
        self.normal.max_hits = 4
        self.constellation_upgrades.skill = 5
        self.constellation_upgrades.burst = 3
        self.has_arkhe_alignment = True

    def initialize(self):
        self.logger.info("Furina initialized")
        self.logger.info(f"Internal data: {self._data}")
        self.a1()
        self.a4()
        self._a4_tick()
        self._elemental_burst_init()

    def elemental_skill(self):
        pass

    # When the active character in your party receives healing, if the source of the healing is not Furina herself
    # and the healing overflows, then Furina will heal nearby party members for 2% of their Max HP once every 2s
    # within the next 4s.
    def a1(self):
        if self.base.ascension < 1:
            return
        self.core.event_handler.subscribe(
            Event.ON_HEAL,
            self._a1_callback,
            'furina-a1'
        )

    def _a1_callback(self, *args, **kwargs):
        heal_event: HealEvent = args[0]
        if heal_event.data.healer_index == self.index:
            return
        if heal_event.target_index != self.core.player_handler.active:
            return
        if heal_event.heal_overflow <= 0:
            return
        if not self.modifier_handler.has_status_active('furina-a1-hot'):
            self.core.task_handler.add_task('furina-a1-hot-instance1', self._a1_heal, 2 * 60)

        self.modifier_handler.add_status('furina-a1-hot', 4 * 60, False)

    def _a1_heal(self, *args, **kwargs):
        if not self.modifier_handler.has_status_active('furina-a1-hot'):
            return
        self.core.player_handler.heal(
            HealDetails(
                healer_index=self.index,
                target_index=HEAL_ALL_TARGETS,
                heal_type=HealType.PERCENTAGE,
                amount=0.02,
                heal_bonus=0.0,
                name='furina-a1-hot',
            )
        )

        self.core.task_handler.add_task('furina-a1-hot-instance2', self._a1_heal, 2 * 60)

    # Every 1,000 points of Furina's Max HP can buff the different Arkhe-aligned Salon Solitaire in the following ways:
    # Will increase Salon Member DMG dealt by 0.7%, up to a maximum of 28%.
    # Will decrease active character healing interval of the Singer of Many Waters by 0.4%, up to a maximum of 16%.
    def a4(self):
        if self.base.ascension < 4:
            return
        self._data.a4_buffs = CharacterStats.get_empty_dict()
        self.modifier_handler.add_attack_modifier(
            CharacterAttackModifier(
                status_key='furina-a4-dmg-bonus',
                frame_duration=MODIFIER_PERMANENT_DURATION,
                hitlag=False,
                value=self._a4_callback,
                status_expiry=0, # Permanent
                status_extension=0, # No extension
            )
        )

    def _a4_callback(self, attack_event: AttackEvent) -> ModifierFunctionResult:
        if attack_event.data.attack_type != AttackType.ELEMENTAL_SKILL:
            return {}, ModifierResult.REJECTED, 'Not an Elemental Skill'
        if self._data.SALON_MEMBER_KEY in attack_event.data.ability_name:
            return {}, ModifierResult.REJECTED, 'Not a Salon Member damage instance'
        return self._data.a4_buffs, ModifierResult.APPLIED, 'A4 buff applied'

    def _a4_tick(self):
        if self.base.ascension < 4:
            return

        self._data.a4_buffs[CharacterStats.ALL_DMG_BONUS] = min(self.get_max_hp() / 1000 * 0.007, 0.28)
        self._data.a4_interval_reduction = min(self.get_max_hp() / 1000 * 0.004, 0.16)
        # self.logger.event(LogEventType.MODIFIER, self.base.name, 'a4-tick', a4_buffs=self._data.a4_buffs, interval=self._data.a4_interval_reduction)
        self.core.task_handler.add_task('furina-a4-tick', self._a4_tick, self._data.A4_CHECK_INTERVAL)

    # Rouses the impulse to revel, creating a stage of foam that will deal AoE Hydro DMG based on Furina's Max HP and cause nearby party members
    # to enter the Universal Revelry state: During this time, when nearby party members' HP increases or decreases, 1 Fanfare point will be granted to
    # Furina for each percentage point of their Max HP by which their HP changes.
    # At the same time, Furina will increase the DMG dealt by and Incoming Healing Bonus of all nearby party members based on the amount of Fanfare she has.
    # When the duration ends, Furina's Fanfare points will be cleared.
    def elemental_burst(self) -> ActionInfo:
        attack_details = AttackDetails(
            attacker_index=self.index,
            attacker_name=self.base.name,
            ability_name='Let the People Rejoice',
            attack_type=AttackType.ELEMENTAL_BURST,
            attack_additional_type=AttackAdditionalType.NONE,
            poise_damage=0,
            icd_tag=ICDTag.NONE,
            icd_group=ICDGroup.DEFAULT,
            element=Element.HYDRO,
            aura_durability=25.0,
            flat_dmg=self.get_max_hp() * self.scalings.BURST_DMG[self.talents.burst],
            multipliers=[],
            stats=[],
        )

        self._data.fanfare_stacks = 0.0
        self.modifier_handler.delete_status(self._data.BURST_KEY)
        self.core.task_handler.add_task(
            'furina-burst-add-burst-status',
            self._elemental_burst_add_status,
            95
        )
        self.core.queue_attack(attack_details, delay=self._data.BURST_HITMARK, snapshot_delay=self._data.BURST_HITMARK)
        self.set_cooldown(ActionType.BURST, self._data.BURST_COOLDOWN)
        self.consume_energy(self._data.BURST_ENERGY_CONSUME_DELAY)
        return

    def _elemental_burst_add_status(self):
        if self.base.constellation >= 1:
            self._data.fanfare_stacks = 150.0
        self.modifier_handler.add_status(self._data.BURST_KEY, self._data.BURST_DURATION, True)

    def _elemental_burst_fanfare_add_generator(self, amount: float):
        def _fanfare_add_generator():
            fanfare_multiplier = 1.0 if self.base.constellation < 2 else 3.5
            old_fanfare_stacks = self._data.fanfare_stacks
            fanfare_stacks_added = amount * fanfare_multiplier
            self._data.fanfare_stacks = min(
                self._data.fanfare_stacks + fanfare_stacks_added,
                self._data.max_fanfare_stacks
            )
            self.logger.event(
                LogEventType.CHARACTER,
                self.base.name,
                'fanfare-add',
                desc='Fanfare Gained',
                old_fanfare_stacks=old_fanfare_stacks,
                new_fanfare_stacks=self._data.fanfare_stacks
            )
        return _fanfare_add_generator

    def _elemental_burst_queue_fanfare_add(self, amount: float):
        if not self.modifier_handler.has_status_active(self._data.FANFARE_FREEZE_KEY):
            if not self._data.fanfare_freeze_queued:
                self._data.fanfare_freeze_queued = True
                self.core.task_handler.add_task(
                    self._data.FANFARE_FREEZE_KEY,
                    self._elemental_burst_queue_fanfare_freeze,
                    self._data.FANFARE_FREEZE_TASK_DELAY
                )

            delay = self._data.FANFARE_HP_CHANGE_TO_GAIN_DELAY  # Frames from HP change to fanfare gain for heals in the same frame
        else:
            delay = self.modifier_handler.get_remaining_status_duration(self._data.FANFARE_FREEZE_KEY) # Fanfare gets added when freeze expires

        self.core.task_handler.add_task(
            'furina-fanfare-gain',
            self._elemental_burst_fanfare_add_generator(amount),
            delay
        )

    def _elemental_burst_queue_fanfare_freeze(self):
        self.modifier_handler.add_status(
            self._data.FANFARE_FREEZE_KEY,
            self._data.FANFARE_FREEZE_DURATION,
            False
        )
        self._data.fanfare_freeze_queued = False

    def _elemental_burst_init(self):
        if self.base.constellation >= 1:
            self._data.max_fanfare_stacks = 400
            self._data.max_fanfare_stacks_c2 = 400

        if self.base.constellation >= 2:
            self._data.max_fanfare_stacks_c2 = 800

        self._data.burst_buffs = CharacterStats.get_empty_dict()

        self.core.event_handler.subscribe(
            Event.ON_HEAL,
            self._elemental_burst_heal_callback,
            'furina-burst-heal-callback'
        )

        self.core.event_handler.subscribe(
            Event.ON_DRAIN,
            self._elemental_burst_drain_callback,
            'furina-burst-drain-callback'
        )

        for character in self.core.player_handler.get_characters():
            character: CharacterBase
            character.modifier_handler.add_attack_modifier(
                CharacterAttackModifier(
                    status_key='furina-burst-dmg-bonus',
                    frame_duration=MODIFIER_PERMANENT_DURATION,
                    hitlag=False,
                    value=self._elemental_burst_dmg_bonus_callback,
                )
            )
            character.modifier_handler.add_incoming_healing_bonus_modifier(
                IncomingHealingBonusModifier(
                    status_key='furina-burst-incoming-healing-bonus',
                    frame_duration=MODIFIER_PERMANENT_DURATION,
                    hitlag=False,
                    value=self._elemental_burst_incoming_healing_bonus_callback,
                )
            )

    def _elemental_burst_dmg_bonus_callback(self, attack_event: AttackEvent) -> ModifierFunctionResult:
        if not self.modifier_handler.has_status_active(self._data.BURST_KEY):
            return {}, ModifierResult.REJECTED, 'Furin Burst is not active'
        dmg_bonus = self.scalings.BURST_FANFARE_DMG_SCALING[self.talents.burst]
        self._data.burst_buffs[CharacterStats.ALL_DMG_BONUS] = min(self._data.fanfare_stacks, self._data.max_fanfare_stacks) *  dmg_bonus
        return self._data.burst_buffs, ModifierResult.APPLIED, 'Furina Burst damage bonus applied'

    def _elemental_burst_incoming_healing_bonus_callback(self) -> tuple[float, ModifierResult, str]:
        if not self.modifier_handler.has_status_active(self._data.BURST_KEY):
            return 0.0, ModifierResult.REJECTED, 'Furina Burst is not active'
        healing_bonus = self.scalings.BURST_FANFARE_INCOMING_HEALING_BONUS_SCALING[self.talents.burst]
        return min(self._data.fanfare_stacks, self._data.max_fanfare_stacks) * healing_bonus, ModifierResult.APPLIED, 'Furina Burst incoming healing bonus applied'

    def _elemental_burst_heal_callback(self, *args, **kwargs):
        if not self.modifier_handler.has_status_active(self._data.BURST_KEY):
            return

        heal_event: HealEvent = args[0]

        if heal_event.heal_final <= 0:
            return

        if abs(heal_event.heal_final - heal_event.heal_overflow) < 1e-9:
            return

        character: CharacterBase = self.core.player_handler.get_by_index(heal_event.target_index)
        amount = (heal_event.heal_final - heal_event.heal_overflow) / character.get_max_hp() * 100

        self._elemental_burst_queue_fanfare_add(amount)

    def _elemental_burst_drain_callback(self, *args, **kwargs):
        if not self.modifier_handler.has_status_active(self._data.BURST_KEY):
            return

        drain_event: DrainEvent = args[0]

        if drain_event.data.amount <= 0:
            return

        character: CharacterBase = self.core.player_handler.get_by_index(drain_event.data.target_index)
        amount = drain_event.data.amount / character.get_max_hp() * 100
        self._elemental_burst_queue_fanfare_add(amount)

    def get_base_stats(self) -> CharacterStatValues:
        return {
            CharacterStats.BASE_ATK: self.scalings.get_base_atk(),
            CharacterStats.BASE_HP: self.scalings.get_base_hp(),
            CharacterStats.BASE_DEF: self.scalings.get_base_def(),
        }