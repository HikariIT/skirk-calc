from dataclasses import dataclass
from typing import Callable


@dataclass
class Task:
    frame: int
    callback: Callable