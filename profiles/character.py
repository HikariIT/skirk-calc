from dataclasses import dataclass
from dataclasses_json import dataclass_json

from common.enum.artifact_set import ArtifactSet
from common.enum.element import Element
from profiles.artifacts import ArtifactMainStats
from profiles.talents import TalentProfile
from profiles.weapon import WeaponProfile


@dataclass_json
@dataclass
class CharacterBaseProfile:
    name: str
    rarity: int
    element: Element
    level: int
    max_level: int
    ascension: int
    constellation: int


@dataclass_json
@dataclass
class CharacterProfile:
    base: CharacterBaseProfile
    weapon: WeaponProfile
    talents: TalentProfile
    stats: dict[str, float]
    sets: dict[str, int]
    main_stats: ArtifactMainStats


