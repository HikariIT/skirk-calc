from common.enum.event import LogEventType
from common.struct.event_data.heal import HealDetails
from common.logger.logger import Logger
from common.const.const import HEAL_ALL_TARGETS
from common.struct.simulation.snapshot import Snapshot
from sim.handlers.base import BaseHandler
from copy import copy

class PlayerHandler(BaseHandler):
    _active_index: int
    _characters: list
    _artifact_sets: list

    def __init__(self):
        self.logger = Logger(__name__)
        super().__init__(self.logger, 0)

        self._active_index = 0
        self._characters = []
        self._artifact_sets = []

    @property
    def active(self):
        return self._active_index

    @active.setter
    def active(self, index):
        self._active_index = index

    def heal(self, heal_data: HealDetails):
        self.logger.event(LogEventType.HEAL, 'Simulation', 'heal', name=heal_data.name, arguments=heal_data)
        if heal_data.target_index == HEAL_ALL_TARGETS:
            for character in self._characters:
                heal_data_target = copy(heal_data)
                heal_data_target.target_index = character.index
                character.heal(heal_data_target)

    def add_character(self, character) -> None:
        self._characters.append(character)

    def add_artifact_set(self, artifact_set) -> None:
        self._artifact_sets.append(artifact_set)

    def advance_frame(self, frame: int = 1):
        super().advance_frame(frame)
        for character in self._characters:
            character.modifier_handler.advance_frame(frame)

    def get_snapshot(self, index: int) -> Snapshot:
        if index >= len(self._characters):
            raise IndexError(f"Index {index} out of range for characters list.")
        character = self._characters[index]
        return Snapshot(
            stats=character.stats,
            character_lvl=character.level,
            frame=self.frame
        )
