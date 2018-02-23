from events.events import Dispatcher, Event
from events.events.utils import *

import re
from django.test import TestCase
import django.dispatch
from unittest.mock import Mock
import gevent
import collections

class SomeClass:
    pass

class TestUtils(TestCase):

    def test_GetPathFromClass(self):
        self.assertEquals(GetPathFromClass(SomeClass), 'events::tests::TestUtils::SomeClass')
        pass

    @Dispatcher.MocksDispatch
    def test_SignalToEvent(self):
        test_signal = django.dispatch.Signal()
        Dispatcher.Expect('some::event::to::be::fired')
        SignalToEvent(test_signal, event='some::event::to::be::fired')
        test_signal.send(self.__class__)
        gevent.sleep()

        class TestEvent(Event): pass
        
        test_signal = django.dispatch.Signal()
        Dispatcher.Expect(TestEvent)
        SignalToEvent(test_signal, event=TestEvent)
        test_signal.send(self.__class__)
        gevent.sleep()

        class TestEvent2(Event): pass
        class TestEvent3(Event): pass
        
        test_signal = django.dispatch.Signal(providing_args=["test"])

        Dispatcher.Expect(TestEvent2)
        Dispatcher.Expect(TestEvent3)
        def hook(sender, signal, test):
            if test:
                return TestEvent2()
            return TestEvent3()
            
        SignalToEvent(test_signal, hook=hook)
        test_signal.send(self.__class__, test=True)
        test_signal.send(self.__class__, test=False)        
        gevent.sleep()
        pass
