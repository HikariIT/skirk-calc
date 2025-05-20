from dataclasses import dataclass
from dataclasses_json import dataclass_json

from static.data.artifact_values import ARTIFACT_MAIN_STATS_LVL_20, ARTIFACT_SUBSTATS_MEDIAN_VALUES
from common.enum.element import Element
from common.enum.stats import ArtifactSubStat, CharacterStatValues, CharacterStats
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
    substat_rolls: dict[str, int]

    def get_artifact_stats(self) -> CharacterStatValues:
        initial_stats = CharacterStats.get_empty_dict()
        stat_sands = CharacterStats.from_artifact_main_stat(self.main_stats.sands)
        stat_goblet = CharacterStats.from_artifact_main_stat(self.main_stats.goblet)
        stat_circlet = CharacterStats.from_artifact_main_stat(self.main_stats.circlet)

        initial_stats[stat_sands] = ARTIFACT_MAIN_STATS_LVL_20[self.main_stats.sands]
        initial_stats[stat_goblet] = ARTIFACT_MAIN_STATS_LVL_20[self.main_stats.goblet]
        initial_stats[stat_circlet] = ARTIFACT_MAIN_STATS_LVL_20[self.main_stats.circlet]

        for stat, rolls in self.substat_rolls.items():
            sub_stat = ArtifactSubStat.from_str(stat)
            stat_enum = CharacterStats.from_artifact_sub_stat(sub_stat)
            initial_stats[stat_enum] += ARTIFACT_SUBSTATS_MEDIAN_VALUES[sub_stat] * rolls

        return initial_stats


