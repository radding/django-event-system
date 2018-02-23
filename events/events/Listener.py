from .Meta import EventListenerMeta
from .Event import Event

class EventListener(metaclass=EventListenerMeta):
    listensFor = []
    def handle(self, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        if len(args) > 1:
            if issubclass(type(args[1]), Event):
                args = args[1:]
                pass
            pass
        self.handle(*args, **kwargs)
        pass
