from common.enum.event import Event
from common.logger.logger import Logger
from typing import Callable



class PubSub:

    def __init__(self):
        self.logger = Logger(__name__)
        self.logger.info("PubSub initialized")
        self.subscriber_list = {
            event: {} for event in Event
        }

    def subscribe(self, event: Event, callback: Callable, key: str):
        self.subscriber_list[event][key] = callback

    def unsubscribe(self, event: Event, key: str):
        if event in self.subscriber_list and key in self.subscriber_list[event]:
            self.subscriber_list[event].pop(key)

    def publish(self, event: Event, *args, **kwargs):
        if event in self.subscriber_list:
            for key, callback in self.subscriber_list[event].items():
                callback(*args, **kwargs)
                self.logger.info(f"Callback {key} executed for event {event.name} with args: {args} and kwargs: {kwargs}")

