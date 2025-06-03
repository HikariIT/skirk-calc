from common.enum.action import CharacterAction
from common.struct.event_data.heal import HealDetails
from common.struct.simulation.snapshot import Snapshot
from common.const.const import HEAL_ALL_TARGETS
from common.enum.event import LogEventType
from common.logger.logger import Logger

from sim.handlers.event import EventHandler
from sim.handlers.base import BaseHandler
from sim.handlers.task import TaskHandler

from copy import copy


class PlayerHandler(BaseHandler):

    logger: Logger
    frame: int
    _active_index: int
    _characters: list
    _artifact_sets: list
    _delays: dict[CharacterAction, int]
    _event_handler: EventHandler
    _task_handler: TaskHandler
    _enable_hitlag: bool

    def __init__(self, event: EventHandler, task: TaskHandler, delays: dict[CharacterAction, int], enable_hitlag: bool = True):
        self.logger = Logger(__name__)
        super().__init__(self.logger, 0)

        self._active_index = 0
        self._characters = []
        self._artifact_sets = []
        self._delays = delays
        self._event_handler = event
        self._task_handler = task
        self._enable_hitlag = enable_hitlag
        self.logger.info(f"PlayerHandler initialized with delays {self._delays} and hitlag {'enabled' if self._enable_hitlag else 'disabled'}.")

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

    def tick(self):
        super().tick()
        for character in self._characters:
            character.modifier_handler.tick()

    def get_snapshot(self, index: int) -> Snapshot:
        character = self.get_by_index(index)
        return character.snapshot()

    def get_by_index(self, index: int):
        if index >= len(self._characters):
            raise IndexError(f"Index {index} out of range for characters list.")
        return self._characters[index]

    def get_characters(self):
        return self._characters