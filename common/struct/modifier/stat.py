from common.enum.stats import CharacterStats, CharacterStatValues
from common.enum.modifier import ModifierResult
from common.struct.modifier.modifier import BaseModifier
from typing import Callable


type StatModifierFunction = Callable[[], tuple[CharacterStatValues, ModifierResult]]


class HealingBonusModifier(BaseModifier):
    get_value: StatModifierFunction

    def __init__(self, status_key: str, frame_duration: int, stat: CharacterStats, value: StatModifierFunction, hitlag: bool = False, status_expiry: int = 0, status_extension: int = 0):
        super().__init__(status_key, frame_duration, hitlag, status_expiry, status_extension)
        self.get_value = value