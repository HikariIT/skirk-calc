from typing import Callable, Optional
import json

from common.struct.event_data.attack import AttackDetails
from common.struct.simulation.snapshot import Snapshot


class AttackEvent:
    data: AttackDetails
    snapshot: Optional[Snapshot]
    callbacks: list[Callable]

    def __init__(self, data: AttackDetails, callbacks: list[Callable]):
        self.data = data
        self.callbacks = []

    def __repr__(self):
        return f"AttackEvent(data={self.data}, callbacks={self.callbacks})"


    def set_snapshot(self, snapshot: Snapshot):
        self.snapshot = snapshot