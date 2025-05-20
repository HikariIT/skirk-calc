from common.enum.stats import CharacterStatValues
from dataclasses import dataclass


@dataclass
class Snapshot:
    stats: CharacterStatValues
    character_lvl: int
    frame: int