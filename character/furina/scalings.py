from base.character.scalings import CharacterScalings
from common.enum.stats import CharacterStats


class FurinaScalings(CharacterScalings):
    # Currently available for level 90 / 90 only due to KQMS restrictions
    BASE_HP = 15307.39
    BASE_ATK = 243.96
    BASE_DEF = 695.54
    ASCENSION_STAT = CharacterStats.CRIT_RATE
    ASCENSION_STAT_VALUE = 0.192
    BURST_DMG = [0.114064, 0.122619, 0.131174, 0.14258, 0.151135, 0.15969, 0.171096, 0.182502, 0.193909, 0.205315, 0.216722, 0.228128, 0.242386, 0.256644, 0.270902]
    BURST_FANFARE_DMG_SCALING = [0.0007, 0.0009, 0.0011, 0.0013, 0.0015, 0.0017, 0.0019, 0.0021, 0.0023, 0.0025, 0.0027, 0.0029, 0.0031, 0.0033, 0.0035]
    BURST_FANFARE_INCOMING_HEALING_BONUS_SCALING = [0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008, 0.0009, 0.001, 0.0011, 0.0012, 0.0013, 0.0014, 0.0015]