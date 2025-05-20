from typing import Callable

from common.struct.event_data.attack import AttackDetails
from common.struct.simulation.snapshot import Snapshot


class AttackEvent:
    data: AttackDetails
    snapshot: Snapshot
    callbacks: list[Callable]

    def __init__(self, data: AttackDetails, snapshot: Snapshot, callbacks: list[Callable]):
        self.data = data
        self.snapshot = snapshot
        self.callbacks = []

    def __repr__(self):
        return str(self.to_json()) # type: ignore