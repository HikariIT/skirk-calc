from typing import Optional, Callable
from common.logger.logger import Logger
from numpy import random

from common.struct.event.attack import AttackEvent
from common.struct.event_data.attack import AttackDetails
from common.struct.simulation.snapshot import Snapshot
from sim.config.config import SimulationConfig
from sim.handlers.combat import CombatHandler
from sim.handlers.event import EventHandler
from sim.handlers.player import PlayerHandler
from sim.handlers.task import TaskHandler


class Handlers:
    task_handler: TaskHandler
    event_handler: EventHandler
    combat_handler: CombatHandler
    player_handler: PlayerHandler

    def __init__(self, task: TaskHandler, event: EventHandler, combat: CombatHandler, player: PlayerHandler):
        self.task_handler = task
        self.event_handler = event
        self.combat_handler = combat
        self.player_handler = player


class Core:
    seed: int
    frame: int
    max_duration: int
    rand: random.Generator
    logger: Logger
    handlers: Handlers

    def __init__(self, task: TaskHandler, event: EventHandler, combat: CombatHandler, player: PlayerHandler, cfg: SimulationConfig):
        self.task_handler = task
        self.event_handler = event
        self.combat_handler = combat
        self.player_handler = player

        self.seed = cfg.seed
        self.rand = random.default_rng(self.seed)
        self.logger = Logger(__name__)

        self.frame = 0
        self.max_duration = cfg.frame_duration

    def advance_frame(self, frame: int = 1):
        self.frame += frame
        self.task_handler.advance_frame(frame)
        self.event_handler.advance_frame(frame)
        self.combat_handler.advance_frame(frame)
        self.player_handler.advance_frame(frame)

    def queue_attack(self, attack_details: AttackDetails, delay: int = 0,   snapshot: Optional[Snapshot] = None, callbacks: Optional[list[Callable]] = None):
        if snapshot is None:
            snapshot = self.player_handler.get_snapshot(attack_details.attacker_index)
        attack_event = AttackEvent(
            data=attack_details,
            snapshot=snapshot,
            callbacks=callbacks if callbacks is not None else []
        )
        if delay < 0:
            raise ValueError("Delay cannot be negative")

        if delay == 0:
            self.combat_handler.apply_attack(attack_event)
        else:
            self.task_handler.add_task(
                'attack-after-delay',
                lambda: self.combat_handler.apply_attack(attack_event),
                delay
            )

