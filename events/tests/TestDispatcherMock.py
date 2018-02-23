import re
from django.test import TestCase
from unittest.mock import Mock
import gevent
import collections

from events.events import Dispatcher, Event, EventListener

# Create your tests here.

class TestEvent(Event):
    pass

class TestListener(EventListener):
    listensFor = [TestEvent, ]
    def handle(self, event):
        pass

class TestDispatcherMock(TestCase):
    
    @Dispatcher.MocksDispatch
    def test_mock_of_string(self):
        Dispatcher.Expect('event::test::event')
        Dispatcher.Dispatch('event::test::event')
        pass

    @Dispatcher.MocksDispatch
    def test_mock_of_object(self):
        Dispatcher.Expect(TestEvent)
        TestListener.handle = Mock()
        TestEvent.Dispatch()
        gevent.sleep()
        self.assertFalse(TestListener.handle.called)
        pass


