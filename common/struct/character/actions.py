from dataclasses import dataclass

from common.enum.heal import HealType

@dataclass
class HealAction:
    heal_type: HealType
    value: float

