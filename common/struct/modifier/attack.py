from common.struct.modifier.modifier import BaseModifier
from common.struct.event.attack import AttackEvent
from common.enum.stats import CharacterStatValues
from common.enum.modifier import ModifierResult
from typing import Callable


type AttackModifierFunction = Callable[[AttackEvent], tuple[CharacterStatValues, ModifierResult]]


class CharacterAttackModifier(BaseModifier):
    get_value: AttackModifierFunction

    def __init__(self, status_key: str, frame_duration: int, hitlag: bool, value: AttackModifierFunction, status_expiry: int = 0, status_extension: int = 0):
        super().__init__(status_key, frame_duration, hitlag, status_expiry, status_extension)
        self.get_value = value