from dataclasses import dataclass

from character.base.artifact.artifact_set import ArtifactSetWrapper
from character.base.weapon.weapon import WeaponWrapper
from common.enum.artifact_set import ArtifactSet
from common.enum.element import Element
from profiles.character import CharacterProfile

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
    weapon: WeaponWrapper
    sets: dict[ArtifactSet, int]

@dataclass
class CharacterEnergyAttributes:
    energy: float
    max_energy: float
    particle_delay: int

@dataclass
class CharacterNormalAttackAttributes:
    max_hits: int
    counter: int

@dataclass
class CharacterBaseStatAttributes:
    hp: float
    hpp: float
    atk: float
    atkp: float
    defence: float
    defencep: float
    em: float
    er: float
    crit_rate: float
    crit_dmg: float
    healing_bonus: float
    pyro_dmg_bonus: float
    hydro_dmg_bonus: float
    cryo_dmg_bonus: float
    electro_dmg_bonus: float
    anemo_dmg_bonus: float
    geo_dmg_bonus: float
    dendro_dmg_bonus: float
    physical_dmg_bonus: float
    attack_speed: float
    all_dmg_bonus: float
    base_hp: float
    base_atk: float
    base_def: float