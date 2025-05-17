from common.enum.character import CharacterKey
from character.furina.furina import Furina


class CharacterRegistry:

    _registry = {
        CharacterKey.FURINA.value: Furina
    }

    def get_character(self, key: str):
        if key in self._registry:
            return self._registry[key]
        else:
            raise ValueError(f"Character {key} not found in registry.")