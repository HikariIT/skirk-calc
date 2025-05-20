from common.struct.modifier.modifier import BaseModifier


class CharacterStatusModifier(BaseModifier):

    def __init__(self, status_key: str, frame_duration: int, hitlag: bool, status_expiry: int = 0, status_extension: int = 0):
        super().__init__(status_key, frame_duration, hitlag, status_expiry, status_extension)