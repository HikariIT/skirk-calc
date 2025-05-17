import pytest
import os
import sys

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.enum.event import Event
from sim.pubsub import PubSub


@pytest.mark.ut
class TestTaskHandler:

    @pytest.fixture(autouse=True)
    def _setup(self):
        self.pubsub = PubSub()

    def test_init(self):
        assert self.pubsub.subscriber_list is not None

    def test_subscribe(self):
        def dummy_callback():
            pass

        self.pubsub.subscribe(Event.ON_ATTACK, dummy_callback, 'dummy_attack_callback')
        assert Event.ON_ATTACK in self.pubsub.subscriber_list
        assert 'dummy_attack_callback' in self.pubsub.subscriber_list[Event.ON_ATTACK]
        assert self.pubsub.subscriber_list[Event.ON_ATTACK]['dummy_attack_callback'] == dummy_callback

    def test_unsubscribe(self):
        def dummy_callback():
            pass

        self.pubsub.subscribe(Event.ON_ATTACK, dummy_callback, 'dummy_attack_callback')
        self.pubsub.unsubscribe(Event.ON_ATTACK, 'dummy_attack_callback')
        assert 'dummy_attack_callback' not in self.pubsub.subscriber_list[Event.ON_ATTACK]

    def test_publish(self, mocker):
        def dummy_callback(arg1, arg2):
            return arg1 + arg2

        self.pubsub.subscribe(Event.ON_ATTACK, dummy_callback, 'dummy_attack_callback')
        mock_callback = mocker.Mock()
        self.pubsub.subscribe(Event.ON_ATTACK, mock_callback, 'mock_callback')
        self.pubsub.publish(Event.ON_ATTACK, 1, 2)

        mock_callback.assert_called_once_with(1, 2)