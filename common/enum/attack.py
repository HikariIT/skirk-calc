from enum import Enum

class AttackType(Enum):
    NONE = 0
    NORMAL = 1
    EXTRA = 2
    PLUNGE = 3
    ELEMENTAL_SKILL = 4
    ELEMENTAL_SKILL_HOLD = 5
    ELEMENTAL_BURST = 6
    WEAPON_SKILL = 7
    MONA_BUBBLE_BREAK = 8
    NONE_STAT = 9
    REACTION_ATTACK_DELIM = 10
    OVERLOAD_DAMAGE = 11
    SUPERCONDUCT_DAMAGE = 12
    EC_DAMAGE = 13
    SHATTER = 14
    SWIRL_PYRO = 15
    SWIRL_HYDRO = 16
    SWIRL_CRYO = 17
    SWIRL_ELECTRO = 18
    BURNING_DAMAGE = 19
    BLOOM = 20
    BOUNTIFUL_CORE = 21
    BURGEON = 22
    HYPERBLOOM = 23
    LENGTH = 24


class StrikeType(Enum):
    DEFAULT = 0
    PIERCING = 1
    BLUNT = 2
    SLASH = 3
    SPEAR = 4


class AttackAdditionalType(Enum):
    NONE = 0
    NIGHTSOUL = 1