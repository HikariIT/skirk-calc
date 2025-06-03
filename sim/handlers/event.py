from common.enum.event import Event, LogEventType
from sim.handlers.base import BaseHandler
from common.logger.logger import Logger
from typing import Callable


class EventHandler(BaseHandler):

    def __init__(self):
        self.logger = Logger(__name__)
        super().__init__(self.logger, 0)

        self.subscriber_list = {
            event: {} for event in Event
        }
        self.logger.info("EventHandler initialized with empty subscriber list for all events.")

    def subscribe(self, event: Event, callback: Callable, key: str):
        self.subscriber_list[event][key] = callback

    def unsubscribe(self, event: Event, key: str):
        if event in self.subscriber_list and key in self.subscriber_list[event]:
            self.subscriber_list[event].pop(key)

    def publish(self, event: Event, *args, **kwargs):
        if event in self.subscriber_list:
            for key, callback in self.subscriber_list[event].items():
                self.logger.event(LogEventType.EVENT, 'Simulation', f'callback-{key}', name=event.name, arguments=args, named_arguments=kwargs)
                callback(*args, **kwargs)

