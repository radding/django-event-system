from gevent.event import Event as GEvent
from .Dispatcher import Dispatcher
from .utils import GetPathFromClass
import gevent

class Event:
    Name = None

    @classmethod
    def GetEventName(cls):
        return cls.Name or GetPathFromClass(cls)
    
    @classmethod
    def AddListener(cls, callable):
        Dispatcher.RegisterHandler(cls.GetEventName(), callable)

    @classmethod
    def DispatchAsync(cls, *args, **kwargs):
        event = cls(*args, **kwargs)
        Dispatcher.Dispatch(cls.GetEventName(), event)
        return event
    
    @classmethod
    def Dispatch(cls, *args, **kwargs):
        event = cls.DispatchAsync(*args, **kwargs)
        gevent.sleep()
        return event

    def __str__(self):
        return type(self).GetEventName()

    def __repr__(self):
        return str(self)