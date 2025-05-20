from base.weapon.scalings import WeaponScalings
from common.enum.stats import CharacterStats


class FleuveCendreFerrymanScalings(WeaponScalings):
    # Currently for level 90 / 90 only due to KQMS restrictions

    BASE_ATK: float = 510.0
    MAIN_STAT: CharacterStats = CharacterStats.ENERGY_RECHARGE
    MAIN_STAT_VALUE: float = 0.459
    ATTRIBUTES: dict[str, list[float]] = {
        'skill-crit-rate-increase': [8.0, 10.0, 12.0, 14.0, 16.0],
        'er-skill-increase': [0.16, 0.2, 0.24, 0.28, 0.32],
    }

