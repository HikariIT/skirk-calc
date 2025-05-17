from dataclasses import dataclass
from common.enum.stats import CharacterStats


@dataclass
class CharacterBasicStatInfo:
    base_hp: float
    base_atk: float
    base_def: float
    ascension_stat_type: CharacterStats
    ascension_stat_value: float