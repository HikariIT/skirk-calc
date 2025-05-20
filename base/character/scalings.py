from common.enum.stats import CharacterStats


class CharacterScalings:

    BASE_HP: float
    BASE_ATK: float
    BASE_DEF: float
    ASCENSION_STAT: CharacterStats
    ASCENSION_STAT_VALUE: float

    def get_base_hp(self) -> float:
        return self.BASE_HP

    def get_base_atk(self) -> float:
        return self.BASE_ATK

    def get_base_def(self) -> float:
        return self.BASE_DEF

    def get_ascension_stat(self) -> tuple[CharacterStats, float]:
        return self.ASCENSION_STAT, self.ASCENSION_STAT_VALUE