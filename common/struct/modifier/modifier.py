from dataclasses import dataclass


@dataclass
class BaseModifier:
    status_key: str
    frame_duration: int
    hitlag: bool
    status_expiry: int = 0
    status_extension: int = 0

    def update_expiry(self, frame: int) -> None:
        if self.frame_duration < 0:
            self.status_expiry = -1
        else:
            self.status_expiry = frame + self.frame_duration