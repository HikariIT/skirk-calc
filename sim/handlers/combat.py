from common.enum.event import LogEventType
from common.logger.logger import Logger
from common.struct.event.attack import AttackEvent
from sim.handlers.base import BaseHandler


class CombatHandler(BaseHandler):

    def __init__(self):
        self.logger = Logger(__name__)
        super().__init__(self.logger, 0)

    def apply_attack(self, attack_event: AttackEvent) -> None:
        self.logger.event(LogEventType.DAMAGE, attack_event.data.attacker_name, attack_event.data.ability_name, attack_event=attack_event)