from typing import Optional, Callable
from common.const.const import NO_SNAPSHOT
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


class Core:
    seed: int
    frame: int
    max_duration: int
    rand: random.Generator
    logger: Logger

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

    def tick(self):
        self.frame += 1
        self.task_handler.tick()
        self.combat_handler.tick()
        self.player_handler.tick()

    # ATTACK -------------------------------------------------------------------------------------

    def queue_attack(self, attack_details: AttackDetails, delay: int = 0, snapshot_delay: int = 0, snapshot: Optional[Snapshot] = None, callbacks: Optional[list[Callable]] = None):
        attack_event = AttackEvent(
            data=attack_details,
            callbacks=callbacks if callbacks is not None else []
        )

        if delay < 0:
            raise ValueError("Delay cannot be negative")
        if delay < snapshot_delay:
            raise ValueError("Delay cannot be less than snapshot delay")

        if snapshot_delay == NO_SNAPSHOT:
            if snapshot is None:
                raise ValueError("Snapshot cannot be none when snapshot delay is NO_SNAPSHOT")
            attack_event.set_snapshot(snapshot)
            self.queue_damage(attack_event, delay)
        elif snapshot == 0:
            snapshot = self.player_handler.get_snapshot(attack_details.attacker_index)
            attack_event.set_snapshot(snapshot)
            self.queue_damage(attack_event, delay)
        else:
            self.task_handler.add_task(
                f'{attack_details.ability_name}-snapshot',
                lambda: self._queue_attack_with_snapshot(attack_event, delay, snapshot_delay),
                snapshot_delay
            )

    def _queue_attack_with_snapshot(self, attack_event: AttackEvent, delay: int, snapshot_delay: int):
        snapshot = self.player_handler.get_snapshot(attack_event.data.attacker_index)
        attack_event.set_snapshot(snapshot)
        self.queue_damage(attack_event, delay - snapshot_delay)

    def queue_damage(self, attack_event: AttackEvent, delay: int = 0):
        if delay == 0:
            self.combat_handler.apply_attack(attack_event)
        else:
            self.task_handler.add_task(
                f'{attack_event.data.ability_name}-damage-apply',
                lambda: self.combat_handler.apply_attack(attack_event),
                delay
            )