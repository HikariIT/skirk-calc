from typing import TypeVar

from character.base.character.interfaces import CharacterBaseInterface
from character.base.character.attributes import (
    CharacterSkillConstellationUpgradeAttributes,
    CharacterNormalAttackAttributes,
    CharacterEquipmentAttributes,
    CharacterEnergyAttributes,
    CharacterWeaponAttributes,
    CharacterTalentAttributes,
    CharacterBaseAttributes,
    CharacterBaseStatAttributes
)
from character.base.modifier.modifier import Modifier
from common.logger.logger import Logger

T = TypeVar('T') # Represents the type of the character's internal data


class Character(CharacterBaseInterface[T]):

    logger: Logger
    # queue: EventQueue

    base: CharacterBaseAttributes
    weapon: CharacterWeaponAttributes
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
