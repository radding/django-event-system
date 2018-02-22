from .Meta import EventListenerMeta

class EventListener(metaclass=EventListenerMeta):
    listensFor = []
    def handle(self, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        self.handle(*args, **kwargs)
        pass
