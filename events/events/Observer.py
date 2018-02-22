from .Dispatcher import Dispatcher
from .utils import GetPathFromClass, RegisterSignalsFor, events
import uuid
import gevent

class ObserverMeta(type):
    def __new__(cls, clsname, superclasses, attributedict):
        klass = super().__new__(cls, clsname, superclasses, attributedict)
        observes = attributedict.get('observes')
        if clsname == "Observer":
            return klass 
        if observes is None:
            raise TypeError('{}.observes must be defined!'.format(clsname))
        eventDict = RegisterSignalsFor(observes)
        cls.instance = klass()
        for eventType, eventPath in eventDict.items():
            method = getattr(cls.instance, eventType)
            Dispatcher.RegisterHandler(eventPath, method)
            pass
        return klass

class Observer(metaclass=ObserverMeta):
    observes = None
    def creating(self, instance):
        pass
    
    def created(self, instance):
        pass

    def updating(self, instance):
        pass
    
    def updated(self, instance):
        pass
    
    def deleting(self, instance):
        pass

    def deleted(self, instance):
        pass