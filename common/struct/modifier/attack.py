from common.struct.modifier.modifier import BaseModifier, ModifierFunctionResult
from common.struct.event.attack import AttackEvent
from typing import Callable


type AttackModifierFunction = Callable[[AttackEvent], ModifierFunctionResult]


class CharacterAttackModifier(BaseModifier):
    get_value: AttackModifierFunction

    def __init__(self, status_key: str, frame_duration: int, hitlag: bool, value: AttackModifierFunction, status_expiry: int = 0, status_extension: int = 0):
        super().__init__(status_key, frame_duration, hitlag, status_expiry, status_extension)
        self.get_value = value