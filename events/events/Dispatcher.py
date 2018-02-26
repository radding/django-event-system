import collections
import gevent
from gevent.queue import Queue
import re
import functools
import traceback

class DispatchMeta(type):
    def __new__(cls, *args, **kwargs):
        klass = super().__new__(cls, *args, **kwargs)
        cls.gevent = gevent.spawn(klass.HandleDispatch)
        return klass

class Dispatcher(metaclass=DispatchMeta):
    queue = Queue()
    handlers = collections.defaultdict(list)
    killEvent = set()
    called = set()
    isTesting = False

    @classmethod
    def ClearQueue(cls):
        try:
            while cls.queue.get_nowait():
                pass
        except:
            pass
        pass

    @classmethod
    def Reset(cls):
        cls.ClearQueue()
        cls.killEvent = set()
        cls.called = set()
        cls.handlers = collections.defaultdict(list)
        pass

    @classmethod
    def MocksDispatch(cls, func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            cls.Reset()
            cls.isTesting = True
            result = func(self, *args, **kwargs)
            gevent.sleep()            
            cls.isTesting = False            
            while not cls.queue.empty():
                gevent.sleep()
                pass
            leftOver = cls.killEvent - cls.called
            message = "Event(s) {} were not called".format(', '.join(leftOver))
            self.assertTrue(len(leftOver) == 0, message)

            cls.Reset()
            return result
        return wrapper


    @classmethod
    def Dispatch(cls, event, *args, **kwargs):
        args = list(args)        
        args.insert(0, event)
        event = str(event)
        cls.queue.put(dict(event=event, args=args, kwargs=kwargs))
        pass

    @classmethod
    def RegisterHandler(cls, eventName, handler):
        cls.handlers[re.compile(eventName)].append(handler)
        pass

    @classmethod
    def Expect(cls, event):
        cls.killEvent.add(str(event))
        pass
    
    @classmethod
    def HandleDispatch(cls):
        while True:
            lastDispatch = cls.queue.get()
            if cls.isTesting and lastDispatch['event'] in cls.killEvent:
                cls.called.add(lastDispatch['event']) 
                continue
            for key, value in cls.handlers.items():
                if key.fullmatch(lastDispatch['event']) is not None:
                    for i in value:
                        try:
                            i(*lastDispatch['args'], **lastDispatch['kwargs'])
                        except Exception as e:
                            traceback.print_exc() 
                            pass                           
                    pass
                pass
            pass
