from dataclasses import dataclass
from typing import Callable


@dataclass
class Task:
    name: str
    frame: int
    callback: Callable