from common.struct.simulation.task import Task
import heapq


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
