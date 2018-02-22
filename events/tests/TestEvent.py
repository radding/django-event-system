from events.events import Event, EventListener, Dispatcher

import re
from django.test import TestCase
from unittest.mock import Mock
import gevent
import collections
import mock

class TestEvent(Event):
    pass

class TestListener(EventListener):
    listensFor = [TestEvent, ]
    def handle(self, event):
        print('What the fuck?') 

class TestEventAndListener(TestCase):
    @mock.patch.object(TestListener, 'handle')
    def test_eventDispatches(self, mock):
        Dispatcher.ClearQueue()
        TestEvent.Dispatch()
        self.assertTrue(mock.called)
        pass
