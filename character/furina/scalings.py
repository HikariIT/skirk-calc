from base.character.scalings import CharacterScalings
from common.enum.stats import CharacterStats


class FurinaScalings(CharacterScalings):
    # Currently available for level 90 / 90 only due to KQMS restrictions
    BASE_HP = 15307.39
    BASE_ATK = 243.96
    BASE_DEF = 695.54
    ASCENSION_STAT = CharacterStats.CRIT_RATE
    ASCENSION_STAT_VALUE = 0.192