import re
from django.test import TestCase
from unittest.mock import Mock
import gevent
import collections

from events.events import Dispatcher

# Create your tests here.

class TestDispatcher(TestCase):
    
    @Dispatcher.MocksDispatch
    def test_register_handler(self):
        Dispatcher.handlers = collections.defaultdict(list)
        self.assertEquals(len(Dispatcher.handlers[re.compile('test_event')]), 0)
        called = True
        def testHandler(*args):
            called = False
        Dispatcher.RegisterHandler('test_event', testHandler)
        self.assertEquals(len(Dispatcher.handlers[re.compile('test_event')]), 1)        
        pass

    @Dispatcher.MocksDispatch
    def test_dispatch(self):
        cb = Mock()
        Dispatcher.RegisterHandler('test_event::2', cb)
        Dispatcher.Dispatch('test_event::2')
        gevent.sleep()
        self.assertTrue(cb.called)
        pass

    @Dispatcher.MocksDispatch
    def test_regex_dispatch(self):
        cb3 = Mock()
        cb4 = Mock()
        cb5 = Mock()
        cb6 = Mock()
        Dispatcher.RegisterHandler('test_event::3', cb3)
        Dispatcher.RegisterHandler('test_event', cb4)
        ##Test that this callback gets called for any number between 2 and 5
        Dispatcher.RegisterHandler('test_event::[2-5]', cb5)
        Dispatcher.RegisterHandler('test_event(.*)', cb6)

        Dispatcher.Dispatch('test_event::3')
        gevent.sleep()
        self.assertTrue(cb3.called)
        self.assertFalse(cb4.called)
        self.assertTrue(cb5.called)
        self.assertTrue(cb6.called)

        cb3.reset_mock()
        cb4.reset_mock()
        cb5.reset_mock()
        cb6.reset_mock()

        Dispatcher.Dispatch('test_event')
        gevent.sleep()
        self.assertFalse(cb3.called)
        self.assertTrue(cb4.called)
        self.assertFalse(cb5.called)
        self.assertTrue(cb6.called)

        cb3.reset_mock()
        cb4.reset_mock()
        cb5.reset_mock()
        cb6.reset_mock()

        Dispatcher.Dispatch('test_event::some::event')
        gevent.sleep()
        self.assertFalse(cb3.called)
        self.assertFalse(cb4.called)
        self.assertFalse(cb5.called)
        self.assertTrue(cb6.called)
        pass
