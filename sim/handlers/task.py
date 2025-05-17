import heapq
from common.struct.simulation.task import Task
from typing import Callable, Tuple


class PriorityQueue:

    def __init__(self):
        self._queue: list[tuple[int, int, Task]] = []
        self._index = 0

    def push(self, task: Task):
        heapq.heappush(self._queue, (task.frame, self._index, task))
        self._index += 1

    def pop(self) -> Task:
        return heapq.heappop(self._queue)[2]

    def peek(self) -> Task | None:
        return self._queue[0][2] if self._queue else None

class TaskHandler:

    frame: int
    queue: PriorityQueue

    def __init__(self):
        self.frame = 0
        self.queue = PriorityQueue()

    def add_task(self, callback: Callable, delay: int):
        self.queue.push(Task(self.frame + delay, callback))

    def advance_frame(self, frames: int):
        self.frame += frames

    def execute_tasks(self):
        while True:
            next_task = self.queue.peek()
            if not next_task or next_task.frame > self.frame:
                break
            task = self.queue.pop()
            task.callback()