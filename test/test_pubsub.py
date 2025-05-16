import pytest
import os
import sys

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

pytest.mark = pytest.mark.ut
from sim.handler import TaskHandler


class TestTaskHandler:

    @pytest.fixture(autouse=True)
    def _setup(self):
        self.task_handler = TaskHandler()
