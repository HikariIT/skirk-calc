from dataclasses_json import dataclass_json
from dataclasses import dataclass

from common.exception.validation import ValidationError
from common.enum.stats import ArtifactMainStat


@dataclass_json
@dataclass
class ArtifactMainStats:
    rarity: int
    sands: ArtifactMainStat
    goblet: ArtifactMainStat
    circlet: ArtifactMainStat

    def __post_init__(self):
        self._validate_main_stats()

    def _validate_main_stats(self):
        legal_sands = {
            ArtifactMainStat.ATK_PERCENTAGE, ArtifactMainStat.DEF_PERCENTAGE, ArtifactMainStat.HP_PERCENTAGE,
            ArtifactMainStat.ENERGY_RECHARGE, ArtifactMainStat.ELEMENTAL_MASTERY
        }
        legal_goblets = {
            ArtifactMainStat.ATK_PERCENTAGE, ArtifactMainStat.DEF_PERCENTAGE, ArtifactMainStat.HP_PERCENTAGE,
            ArtifactMainStat.PYRO_DMG_BONUS, ArtifactMainStat.HYDRO_DMG_BONUS, ArtifactMainStat.ELECTRO_DMG_BONUS,
            ArtifactMainStat.ANEMO_DMG_BONUS, ArtifactMainStat.GEO_DMG_BONUS, ArtifactMainStat.DENDRO_DMG_BONUS,
            ArtifactMainStat.PHYSICAL_DMG_BONUS, ArtifactMainStat.ELEMENTAL_MASTERY
        }
        legal_circlets = {
            ArtifactMainStat.ATK_PERCENTAGE, ArtifactMainStat.DEF_PERCENTAGE, ArtifactMainStat.HP_PERCENTAGE,
            ArtifactMainStat.CRIT_RATE, ArtifactMainStat.CRIT_DMG, ArtifactMainStat.ELEMENTAL_MASTERY,
            ArtifactMainStat.HEALING_BONUS
        }
        if self.sands not in legal_sands:
            raise ValidationError(f"Invalid sands: {self.sands}. Must be one of {legal_sands}")
        if self.goblet not in legal_goblets:
            raise ValidationError(f"Invalid goblet: {self.goblet}. Must be one of {legal_goblets}")
        if self.circlet not in legal_circlets:
            raise ValidationError(f"Invalid circlet: {self.circlet}. Must be one of {legal_circlets}")
