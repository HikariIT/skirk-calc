from character.base.character.interfaces import CharacterBaseInterface
from character.base.character.attributes import (
    CharacterSkillConstellationUpgradeAttributes,
    CharacterNormalAttackAttributes,
    CharacterEquipmentAttributes,
    CharacterEnergyAttributes,
    CharacterTalentAttributes,
    CharacterBaseAttributes,
    CharacterBaseStatAttributes
)
from character.base.modifier.modifier import Modifier
from character.base.weapon.weapon import WeaponWrapper
from common.enum.artifact_set import ArtifactSet
from profiles.character import CharacterProfile
from common.enum.action import ActionType
from common.logger.logger import Logger
from sim.handlers.task import TaskHandler
from sim.core.core import Core
from sim.pubsub import PubSub


class CharacterWrapper(CharacterBaseInterface):

    logger: Logger
    pubsub: PubSub
    task_handler: TaskHandler

    base: CharacterBaseAttributes
    talents: CharacterTalentAttributes
    constellation_upgrades: CharacterSkillConstellationUpgradeAttributes
    equipment: CharacterEquipmentAttributes
    energy: CharacterEnergyAttributes

    has_arkhe_alignment: bool
    starting_hp: int
    starting_hp_percentage: int

    normal: CharacterNormalAttackAttributes
    base_stats: CharacterBaseStatAttributes
    modifiers: list[Modifier]
    frame: int

    def __init__(self,
                 profile: CharacterProfile | None = None,
                 frame: int | None = None,
                 log: Logger | None = None,
                 pubsub: PubSub | None = None,
                 task_handler: TaskHandler | None = None
        ) -> None:
        if profile is None or frame is None or log is None or pubsub is None or task_handler is None:
            return

        self.logger = log
        self.pubsub = pubsub
        self.task_handler = task_handler

        self.base = CharacterBaseAttributes.from_profile(profile)
        self.talents = CharacterTalentAttributes(
            profile.talents.attack,
            profile.talents.skill,
            profile.talents.burst
        )
        self.constellation_upgrades = CharacterSkillConstellationUpgradeAttributes(-1, -1, -1)
        self.equipment = CharacterEquipmentAttributes(
            WeaponWrapper.from_profile(profile.weapon),
            {ArtifactSet.get_from_name(set_name): set_count for set_name, set_count in profile.sets.items()}
        )
        self.energy = CharacterEnergyAttributes(0, 0, 0)

        self.has_arkhe_alignment = False
        self.starting_hp = 0
        self.starting_hp_percentage = 100

        self.normal = CharacterNormalAttackAttributes(0, 0)
        self.base_stats = CharacterBaseStatAttributes(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.modifiers = []
        self.frame = frame


class CharacterBase(CharacterWrapper):
    core: Core
    action_cooldown: dict[ActionType, int]
    available_charges: dict[ActionType, int]

    def __init__(self, wrapper: CharacterWrapper, core: Core):
        self.clone_wrapper_attributes(wrapper)
        self.available_charges = {}
        self.action_cooldown = {}
        self.core = core

    def clone_wrapper_attributes(self, wrapper: CharacterWrapper) -> None:
        self.logger = wrapper.logger
        self.pubsub = wrapper.pubsub
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
        self.modifiers = wrapper.modifiers
        self.frame = wrapper.frame
