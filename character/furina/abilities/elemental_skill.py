from character.base.character.character import CharacterBase
from character.furina.furina import FurinaInternalData


def salon_solitaire(self: CharacterBase[FurinaInternalData]):
    if self.constellation >= 2:
        pass