import collections
import gevent
from gevent.queue import Queue
import re

class DispatchMeta(type):
    def __new__(cls, *args, **kwargs):
        klass = super().__new__(cls, *args, **kwargs)
        gevent.spawn(klass.HandleDispatch)
        return klass

class Dispatcher(metaclass=DispatchMeta):
    queue = Queue()
    handlers = collections.defaultdict(list)

    @classmethod
    def ClearQueue(cls):
        cls.queue = Queue()
        pass

    @classmethod
    def Dispatch(cls, event, *args, **kwargs):
        args = list(args)
        args.insert(0, event)
        cls.queue.put(dict(event=event, args=args, kwargs=kwargs))
        pass

    @classmethod
    def RegisterHandler(cls, eventName, handler):
        cls.handlers[re.compile(eventName)].append(handler)
        pass
    
    @classmethod
    def HandleDispatch(cls):
        while True:
            lastDispatch = cls.queue.get()
            for key, value in cls.handlers.items():
                if key.fullmatch(lastDispatch['event']) is not None:
                    for i in value:
                        i(*lastDispatch['args'], **lastDispatch['kwargs'])
                    pass
                pass
            pass
