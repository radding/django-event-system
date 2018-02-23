from events.events import Event, EventListener, Dispatcher

import re
from django.test import TestCase
from unittest.mock import Mock
import gevent
import collections

class TestEvent(Event):
    pass

class TestEventAndListener(TestCase):

    @Dispatcher.MocksDispatch
    def test_eventDispatches(self):
        class TestListener(EventListener):
            listensFor = [
                TestEvent,
            ]
            def handle(self, event):
                print('What the?')
                pass
            pass
        mock = Mock()
        TestListener.handle = mock
        event = TestEvent.Dispatch()
        self.assertTrue(TestListener.handle.called)
        TestListener.handle.assert_called_with(event)
        pass
