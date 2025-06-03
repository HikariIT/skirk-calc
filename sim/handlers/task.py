from common.utils.priority_queue import PriorityQueue
from common.struct.simulation.task import Task
from sim.handlers.base import BaseHandler
from common.logger.logger import Logger
from typing import Callable


class TaskHandler(BaseHandler):

    frame: int
    _queue: PriorityQueue

    def __init__(self):
        self.logger = Logger(__name__)
        super().__init__(self.logger, 0)
        self._queue = PriorityQueue()
        self.logger.info("TaskHandler initialized with an empty priority queue.")

    def add_task(self, task_name: str, callback: Callable, delay: int):
        self._queue.push(Task(task_name, self.frame + delay, callback))

    def execute_tasks(self):
        while True:
            next_task = self._queue.peek()
            if not next_task or next_task.frame > self.frame:
                break
            task = self._queue.pop()
            task.callback()

    def tick(self):
        super().tick()
        self.execute_tasks()