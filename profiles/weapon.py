from dataclasses import dataclass
from dataclasses_json import dataclass_json

from common.enum.weapon import WeaponType


@dataclass_json
@dataclass
class WeaponProfile:
    name: str
    weapon_type: WeaponType
    refinement: int
    level: int
    max_level: int
