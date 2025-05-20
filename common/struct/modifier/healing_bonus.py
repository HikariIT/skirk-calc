from common.struct.modifier.modifier import BaseModifier


class HealingBonusModifier(BaseModifier):
    value: float

    def __init__(self, status_key: str, frame_duration: int, hitlag: bool, value: float, status_expiry: int = 0, status_extension: int = 0):
        super().__init__(status_key, frame_duration, hitlag, status_expiry, status_extension)
        self.value = value