from enum import Enum


class CharacterStats(Enum):
    HP = 1
    HP_PERCENTAGE = 2
    ATK = 3
    ATK_PERCENTAGE = 4
    DEF = 5
    DEF_PERCENTAGE = 6
    ENERGY_RECHARGE = 7
    ELEMENTAL_MASTERY = 8
    CRIT_RATE = 9
    CRIT_DMG = 10
    HEALING_BONUS = 11
    PYRO_DMG_BONUS = 12
    CRYO_DMG_BONUS = 13
    HYDRO_DMG_BONUS = 14
    ELECTRO_DMG_BONUS = 15
    ANEMO_DMG_BONUS = 16
    GEO_DMG_BONUS = 17
    DENDRO_DMG_BONUS = 18
    PHYSICAL_DMG_BONUS = 19
    ATTACK_SPEED = 20
    ALL_DMG_BONUS = 21
    BASE_HP = 22
    BASE_ATK = 23
    BASE_DEF = 24

    @staticmethod
    def get_empty_dict() -> dict['CharacterStats', float]:
        return {
            key: 0.0 for key in CharacterStats
        }

    @staticmethod
    def get_default_dict() -> dict['CharacterStats', float]:
        default_dict = {
            key: 0.0 for key in CharacterStats
        }
        default_dict[CharacterStats.CRIT_RATE] = 0.05
        default_dict[CharacterStats.CRIT_DMG] = 0.5
        default_dict[CharacterStats.ENERGY_RECHARGE] = 1.0
        return default_dict

    @staticmethod
    def add_dict(stats_dict: dict['CharacterStats', float], stats_dict_other: dict['CharacterStats', float]):
        for key in CharacterStats:
            stats_dict[key] += stats_dict_other[key]
        return stats_dict

    @staticmethod
    def from_artifact_main_stat(stat: 'ArtifactMainStat') -> 'CharacterStats':
        character_stat_map = {
            ArtifactMainStat.HP: CharacterStats.HP,
            ArtifactMainStat.ATK: CharacterStats.ATK,
            ArtifactMainStat.ELEMENTAL_MASTERY: CharacterStats.ELEMENTAL_MASTERY,
            ArtifactMainStat.CRIT_RATE: CharacterStats.CRIT_RATE,
            ArtifactMainStat.CRIT_DMG: CharacterStats.CRIT_DMG,
            ArtifactMainStat.ENERGY_RECHARGE: CharacterStats.ENERGY_RECHARGE,
            ArtifactMainStat.HP_PERCENTAGE: CharacterStats.HP_PERCENTAGE,
            ArtifactMainStat.ATK_PERCENTAGE: CharacterStats.ATK_PERCENTAGE,
            ArtifactMainStat.DEF_PERCENTAGE: CharacterStats.DEF_PERCENTAGE,
            ArtifactMainStat.PYRO_DMG_BONUS: CharacterStats.PYRO_DMG_BONUS,
            ArtifactMainStat.HYDRO_DMG_BONUS: CharacterStats.HYDRO_DMG_BONUS,
            ArtifactMainStat.ELECTRO_DMG_BONUS: CharacterStats.ELECTRO_DMG_BONUS,
            ArtifactMainStat.ANEMO_DMG_BONUS: CharacterStats.ANEMO_DMG_BONUS,
            ArtifactMainStat.GEO_DMG_BONUS: CharacterStats.GEO_DMG_BONUS,
            ArtifactMainStat.DENDRO_DMG_BONUS: CharacterStats.DENDRO_DMG_BONUS,
            ArtifactMainStat.PHYSICAL_DMG_BONUS: CharacterStats.PHYSICAL_DMG_BONUS,
            ArtifactMainStat.HEALING_BONUS: CharacterStats.HEALING_BONUS,
        }
        if stat in character_stat_map:
            return character_stat_map[stat]
        else:
            raise ValueError(f"Invalid ArtifactMainStat for conversion: {stat}")

    @staticmethod
    def from_artifact_sub_stat(stat: 'ArtifactSubStat') -> 'CharacterStats':
        character_stat_map = {
            ArtifactSubStat.HP: CharacterStats.HP,
            ArtifactSubStat.ATK: CharacterStats.ATK,
            ArtifactSubStat.DEF: CharacterStats.DEF,
            ArtifactSubStat.ELEMENTAL_MASTERY: CharacterStats.ELEMENTAL_MASTERY,
            ArtifactSubStat.CRIT_RATE: CharacterStats.CRIT_RATE,
            ArtifactSubStat.CRIT_DMG: CharacterStats.CRIT_DMG,
            ArtifactSubStat.ENERGY_RECHARGE: CharacterStats.ENERGY_RECHARGE,
            ArtifactSubStat.HP_PERCENTAGE: CharacterStats.HP_PERCENTAGE,
            ArtifactSubStat.ATK_PERCENTAGE: CharacterStats.ATK_PERCENTAGE,
            ArtifactSubStat.DEF_PERCENTAGE: CharacterStats.DEF_PERCENTAGE,
        }
        if stat in character_stat_map:
            return character_stat_map[stat]
        else:
            raise ValueError(f"Invalid ArtifactSubStat for conversion: {stat}")


type CharacterStatValues = dict[CharacterStats, float]


class ReactionBonusStats(Enum):
    SWIRL_DMG_BONUS = 1
    OVERLOAD_DMG_BONUS = 2
    ELECTRO_CHARGED_DMG_BONUS = 3
    MELT_DMG_BONUS = 4
    VAPORIZE_DMG_BONUS = 5
    SHATTER_DMG_BONUS = 6
    BURNING_DMG_BONUS = 7
    AGGRAVATE_DMG_BONUS = 8
    SPREAD_DMG_BONUS = 9
    BLOOM_DMG_BONUS = 10
    BURGEON_DMG_BONUS = 11
    HYPERBLOOM_DMG_BONUS = 12


class ScalingStats(Enum):
    HP_PERCENTAGE = 1
    ATK_PERCENTAGE = 2
    DEF_PERCENTAGE = 3


class ArtifactMainStat(Enum):
    HP = 'HP'
    HP_PERCENTAGE = 'HP%'
    ATK = 'ATK'
    ATK_PERCENTAGE = 'ATK%'
    DEF_PERCENTAGE = 'DEF%'
    ELEMENTAL_MASTERY = 'EM'
    ENERGY_RECHARGE = 'ER'
    CRIT_RATE = 'CR'
    CRIT_DMG = 'CD'
    HEALING_BONUS = 'HB%'
    PYRO_DMG_BONUS = 'Pyro%'
    HYDRO_DMG_BONUS = 'Hydro%'
    ELECTRO_DMG_BONUS = 'Electro%'
    ANEMO_DMG_BONUS = 'Anemo%'
    GEO_DMG_BONUS = 'Geo%'
    DENDRO_DMG_BONUS = 'Dendro%'
    PHYSICAL_DMG_BONUS = 'Phys%'

    @staticmethod
    def from_str(stat_str: str) -> 'ArtifactMainStat':
        for stat in ArtifactMainStat:
            if stat.value == stat_str:
                return stat
        raise ValueError(f"Invalid ArtifactMainStat string: {stat_str}")


class ArtifactSubStat(Enum):
    HP = 'HP'
    HP_PERCENTAGE = 'HP%'
    ATK = 'ATK'
    ATK_PERCENTAGE = 'ATK%'
    DEF = 'DEF'
    DEF_PERCENTAGE = 'DEF%'
    ELEMENTAL_MASTERY = 'EM'
    ENERGY_RECHARGE = 'ER'
    CRIT_RATE = 'CR'
    CRIT_DMG = 'CD'

    @staticmethod
    def from_str(stat_str: str) -> 'ArtifactSubStat':
        for stat in ArtifactSubStat:
            if stat.value == stat_str:
                return stat
        raise ValueError(f"Invalid ArtifactSubStat string: {stat_str}")