from common.enum.stats import ArtifactMainStat, ArtifactSubStat


ARTIFACT_MAIN_STATS_LVL_20: dict[ArtifactMainStat, float] = {
    ArtifactMainStat.HP: 4780,
    ArtifactMainStat.HP_PERCENTAGE: 0.466,
    ArtifactMainStat.ATK: 311,
    ArtifactMainStat.ATK_PERCENTAGE: 0.466,
    ArtifactMainStat.DEF_PERCENTAGE: 0.583,
    ArtifactMainStat.ELEMENTAL_MASTERY: 186.5,
    ArtifactMainStat.ENERGY_RECHARGE: 0.518,
    ArtifactMainStat.CRIT_RATE: 0.311,
    ArtifactMainStat.CRIT_DMG: 0.622,
    ArtifactMainStat.HEALING_BONUS: 0.466,
    ArtifactMainStat.PYRO_DMG_BONUS: 0.466,
    ArtifactMainStat.ELECTRO_DMG_BONUS: 0.466,
    ArtifactMainStat.HYDRO_DMG_BONUS: 0.466,
    ArtifactMainStat.ANEMO_DMG_BONUS: 0.466,
    ArtifactMainStat.DENDRO_DMG_BONUS: 0.466,
    ArtifactMainStat.GEO_DMG_BONUS: 0.466,
    ArtifactMainStat.PHYSICAL_DMG_BONUS: 0.583,
}

ARTIFACT_SUBSTATS_MEDIAN_VALUES: dict[ArtifactSubStat, float] = {
    ArtifactSubStat.HP: 253.94,
    ArtifactSubStat.HP_PERCENTAGE: 0.0496,
    ArtifactSubStat.ATK: 16.54,
    ArtifactSubStat.ATK_PERCENTAGE: 0.0496,
    ArtifactSubStat.DEF: 19.68,
    ArtifactSubStat.DEF_PERCENTAGE: 0.0620,
    ArtifactSubStat.ELEMENTAL_MASTERY: 19.82,
    ArtifactSubStat.ENERGY_RECHARGE: 0.0441,
    ArtifactSubStat.CRIT_RATE: 0.0331,
    ArtifactSubStat.CRIT_DMG: 0.0662,
}