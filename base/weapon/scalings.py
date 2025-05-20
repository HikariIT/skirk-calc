from common.enum.stats import CharacterStats


class WeaponScalings:
    # Currently for level 90 / 90 only due to KQMS restrictions

    BASE_ATK: float
    MAIN_STAT: CharacterStats
    MAIN_STAT_VALUE: float
    ATTRIBUTES: dict[str, list[float]]

    def get_base_atk(self) -> float:
        return self.BASE_ATK

    def get_main_stat(self) -> tuple[CharacterStats, float]:
        return self.MAIN_STAT, self.MAIN_STAT_VALUE

    def get_attributes(self, refinement: int) -> dict[str, float]:
        attributes = {}
        for key, value in self.ATTRIBUTES.items():
            attributes[key] = value[refinement - 1]
        return attributes