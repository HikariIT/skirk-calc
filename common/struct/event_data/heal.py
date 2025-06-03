from dataclasses import dataclass
from dataclasses_json import dataclass_json

from common.enum.heal import HealType

@dataclass_json
@dataclass
class HealDetails:
    healer_index: int       # Index of the character performing the heal
    target_index: int       # -1 means all allies
    heal_bonus: float       # Amount of healing bonus (percentage)
    heal_type: HealType
    amount: float
    name: str

    def __repr__(self):
        return str(self.to_json()) # type: ignore

@dataclass_json
@dataclass
class DrainDetails:
    target_index: int
    amount: float
    name: str