from dataclasses import dataclass

from base.weapon.weapon import WeaponBase
from profiles.character import CharacterProfile
from common.enum.element import Element

@dataclass
class CharacterBaseAttributes:
    name: str
    rarity: int
    element: Element
    level: int
    max_level: int
    ascension: int
    constellation: int

    @staticmethod
    def from_profile(profile: CharacterProfile) -> 'CharacterBaseAttributes':
        return CharacterBaseAttributes(
            profile.base.name,
            profile.base.rarity,
            profile.base.element,
            profile.base.level,
            profile.base.max_level,
            profile.base.ascension,
            profile.base.constellation
        )

@dataclass
class CharacterTalentAttributes:
    attack: int
    skill: int
    burst: int

@dataclass
class CharacterSkillConstellationUpgradeAttributes:
    attack: int
    skill: int
    burst: int

@dataclass
class CharacterEquipmentAttributes:
    weapon: WeaponBase | None

@dataclass
class CharacterEnergyAttributes:
    energy: float
    max_energy: float
    particle_delay: int

@dataclass
class CharacterNormalAttackAttributes:
    max_hits: int
    counter: int