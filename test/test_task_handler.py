import pytest
import os
import sys

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sim.handlers.task import TaskHandler

@pytest.mark.ut
class TestTaskHandler:

    @pytest.fixture(autouse=True)
    def _setup(self):
        self.task_handler = TaskHandler()

    def test_init(self):
        assert self.task_handler.frame == 0
        assert self.task_handler._queue is not None

    def test_add_task(self):
        def dummy_task():
            print('2137')

        self.task_handler.add_task(dummy_task, 5)
        next_task = self.task_handler._queue.peek()

        assert next_task is not None
        assert next_task.frame == 5
        assert next_task.callback == dummy_task

    def test_calls_task(self, mocker):
        task_mock = mocker.Mock()

        self.task_handler.add_task(task_mock, 5)
        self.task_handler.tick(5)
        self.task_handler.execute_tasks()
        task_mock.assert_called_once()

    def test_executes_multiple_tasks_at_the_same_frame(self, mocker):
        task_mock_1 = mocker.Mock()
        task_mock_2 = mocker.Mock()

        self.task_handler.add_task(task_mock_1, 5)
        self.task_handler.add_task(task_mock_2, 5)
        self.task_handler.tick(5)
        self.task_handler.execute_tasks()

        task_mock_1.assert_called_once()
        task_mock_2.assert_called_once()

