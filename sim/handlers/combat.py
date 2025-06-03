from numpy import random
from common.enum.event import Event, LogEventType
from common.logger.logger import Logger
from common.struct.event.attack import AttackEvent
from sim.handlers.base import BaseHandler
from sim.handlers.event import EventHandler
from sim.handlers.player import PlayerHandler
from sim.handlers.task import TaskHandler


class CombatHandler(BaseHandler):

    player_handler: PlayerHandler
    event_handler: EventHandler
    task_handler: TaskHandler
    rand: random.Generator
    _default_enemy: None

    def __init__(self, event: EventHandler, task: TaskHandler, player: PlayerHandler, enable_hitlag: bool = True) -> None:
        self.logger = Logger(__name__)
        super().__init__(self.logger, 0)

        self.enable_hitlag = enable_hitlag
        self.player_handler = player
        self.event_handler = event
        self.task_handler = task
        self.enemies = []

        self.logger.info("CombatHandler initialized with random generator and event/task/player handlers.")

    def set_random_generator(self, rand: random.Generator) -> None:
        self.rand = rand
        self.logger.info("Random generator set for CombatHandler.")

    def apply_attack(self, attack_event: AttackEvent) -> None:
        self.event_handler.publish(Event.ON_APPLY_ATTACK, attack_event)
        self.logger.event(LogEventType.DAMAGE, attack_event.data.attacker_name, attack_event.data.ability_name, attack_event=attack_event)

    def add_enemy(self, enemy) -> None:
        self.enemies.append(enemy)
        self.logger.info(f"Enemy {enemy} added to CombatHandler.")
        if self._default_enemy is None:
            self._default_enemy = enemy
            self.logger.info(f"Default enemy set to {enemy}.")

    def get_enemy(self):
        if self._default_enemy is None:
            raise ValueError("No default enemy set. Please add an enemy first.")
        self.logger.info(f"Returning default enemy: {self._default_enemy}.")
        return self._default_enemy