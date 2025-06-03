from common.struct.modifier.modifier import BaseModifier, ModifierResult
from typing import Callable


type IncomingHealingBonusModifierFunction = Callable[[], tuple[float, ModifierResult, str]]


class IncomingHealingBonusModifier(BaseModifier):
    value: IncomingHealingBonusModifierFunction

    def __init__(self, status_key: str, frame_duration: int, hitlag: bool, value: IncomingHealingBonusModifierFunction, status_expiry: int = 0, status_extension: int = 0):
        super().__init__(status_key, frame_duration, hitlag, status_expiry, status_extension)
        self.value = value