from common.enum.artifact_set import ArtifactSetKey
from common.enum.character import CharacterKey
from common.enum.weapon import WeaponKey

from character.furina.furina import Furina

from weapon.fleuve_cendre_ferryman.fleuve_cendre_ferryman import FleuveCendreFerryman

from artifact_set.golden_troupe.golden_troupe import GoldenTroupe


class Registry:

    _character_registry = {
        CharacterKey.FURINA.value: Furina
    }

    _weapon_registry = {
        WeaponKey.FLEUVE_CENDRE_FERRYMAN.value: FleuveCendreFerryman
    }

    _artifact_registry = {
        ArtifactSetKey.GOLDEN_TROUPE.value: GoldenTroupe
    }

    def get_character(self, key: str):
        if key in self._character_registry:
            return self._character_registry[key]
        else:
            raise ValueError(f"Character {key} not found in registry.")

    def get_weapon(self, key: str):
        if key in self._weapon_registry:
            return self._weapon_registry[key]
        else:
            raise ValueError(f"Weapon {key} not found in registry.")

    def get_artifact_set(self, key: str):
        if key in self._artifact_registry:
            return self._artifact_registry[key]
        else:
            raise ValueError(f"Artifact set {key} not found in registry.")