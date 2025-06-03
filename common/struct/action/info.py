from dataclasses import dataclass
from typing import Callable

from common.enum.action import ActionType
from common.enum.char_state import CharacterState


@dataclass
class ActionInfo:
    frames: Callable[[ActionType], int]
    animation_length: int
    can_queue_after: int        # Earliest frame this action can be queued after
    state: CharacterState