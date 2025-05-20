from dataclasses import dataclass
from dataclasses_json import dataclass_json

from common.struct.event_data.heal import HealDetails

@dataclass_json
@dataclass
class HealEvent:
    data: HealDetails
    target_index: int
    heal_initial: float
    heal_final: float       # Amount of healing that actually occurs, after taking into accounts bond of life, etc.
    heal_overflow: float    # Amount of healing that overflows, if any, otherwise 0.

    def __repr__(self):
        return str(self.to_json()) # type: ignore