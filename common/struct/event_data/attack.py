from dataclasses import dataclass

from common.enum.attack import AttackType, AttackAdditionalType
from common.enum.element import Element
from common.enum.stats import CharacterStats
from typing import Optional

@dataclass
class AttackDetails:
    attacker_index: int
    attacker_name: str
    ability_name: str
    attack_type: AttackType
    attack_additional_type: AttackAdditionalType
    poise_damage: float
    icd_tag: str
    icd_group: str
    element: Element

    multipliers: list[float]
    stats: list[CharacterStats]
    flat_dmg: Optional[float] = 0.0

    hitlag_frames: Optional[float] = 0.0
    hitlag_factor: Optional[float] = 0.0

    def __repr__(self):
        return str(self.to_json()) # type: ignore

