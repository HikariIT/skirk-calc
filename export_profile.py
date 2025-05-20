from common.enum.char_stats import CharStats
from common.enum.stats import ArtifactMainStat, ArtifactSubStat
from profiles.character import CharacterBaseProfile, CharacterProfile
from profiles.weapon import WeaponProfile
from profiles.talents import TalentProfile
from common.enum.element import Element
from common.enum.artifact_set import ArtifactSetKey
from common.enum.weapon import WeaponType
from profiles.artifacts import ArtifactMainStats


skirk_profile = CharacterProfile(
    base=CharacterBaseProfile(
        name="Skirk",
        rarity=5,
        element=Element.CRYO,
        level=90,
        max_level=90,
        ascension=6,
        constellation=0
    ),
    weapon=WeaponProfile(
        name="Calamity of Eshu",
        weapon_type=WeaponType.SWORD,
        refinement=5,
        level=90,
        max_level=90
    ),
    talents=TalentProfile.get_kqms(),
    stats = {
        CharStats.CRIT_DMG.name: 0.384,
    },
    main_stats=ArtifactMainStats(
        5,
        sands=ArtifactMainStat.ATK_PERCENTAGE,
        goblet=ArtifactMainStat.ATK_PERCENTAGE,
        circlet=ArtifactMainStat.CRIT_DMG
    ),
    sets={
        ArtifactSetKey.MARECHAUSSE_HUNTER.value: 4,
    },
    substat_rolls={
        ArtifactSubStat.HP.value: 2,
        ArtifactSubStat.HP_PERCENTAGE.value: 2,
        ArtifactSubStat.ATK.value: 2,
        ArtifactSubStat.ATK_PERCENTAGE.value: 2,
        ArtifactSubStat.DEF.value: 2,
        ArtifactSubStat.DEF_PERCENTAGE.value: 2,
        ArtifactSubStat.ELEMENTAL_MASTERY.value: 2,
        ArtifactSubStat.ENERGY_RECHARGE.value: 2,
        ArtifactSubStat.CRIT_RATE.value: 2,
        ArtifactSubStat.CRIT_DMG.value: 2,
    }
)


with open('static/profiles/skirk_mh_eshu.json', 'w') as f:
    f.write(skirk_profile.to_json(indent=2)) # type: ignore


furina_profile = CharacterProfile(
    base=CharacterBaseProfile(
        name="Furina",
        rarity=5,
        element=Element.HYDRO,
        level=90,
        max_level=90,
        ascension=6,
        constellation=2
    ),
    weapon=WeaponProfile(
        name="Fleuve Cendre Ferryman",
        weapon_type=WeaponType.SWORD,
        refinement=5,
        level=90,
        max_level=90
    ),
    talents=TalentProfile.get_kqms(),
    stats = {
        CharStats.CRIT_RATE.name: 0.192,
    },
    main_stats=ArtifactMainStats(
        5,
        sands=ArtifactMainStat.ENERGY_RECHARGE,
        goblet=ArtifactMainStat.HYDRO_DMG_BONUS,
        circlet=ArtifactMainStat.CRIT_RATE
    ),
    sets={
        ArtifactSetKey.GOLDEN_TROUPE.value: 4,
    },
    substat_rolls={
        ArtifactSubStat.HP.value: 2,
        ArtifactSubStat.HP_PERCENTAGE.value: 2,
        ArtifactSubStat.ATK.value: 2,
        ArtifactSubStat.ATK_PERCENTAGE.value: 2,
        ArtifactSubStat.DEF.value: 2,
        ArtifactSubStat.DEF_PERCENTAGE.value: 2,
        ArtifactSubStat.ELEMENTAL_MASTERY.value: 2,
        ArtifactSubStat.ENERGY_RECHARGE.value: 2,
        ArtifactSubStat.CRIT_RATE.value: 2,
        ArtifactSubStat.CRIT_DMG.value: 2,
    }
)


with open('static/profiles/furina_gt_c2_fcf_ersands.json', 'w') as f:
    f.write(furina_profile.to_json(indent=2)) # type: ignore