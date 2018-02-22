import gevent
from .Dispatcher import Dispatcher

class EventListenerMeta(type):
    def __new__(cls, clsname, superclasses, attributedict):
        listensFor = attributedict.get('listensFor')
        if len(superclasses) > 0 and (listensFor is None or len(listensFor) < 1):
            raise TypeError('{}.listensFor must be defined and have atleast one event'.format(clsname))
        klass = super().__new__(cls, clsname, superclasses, attributedict)
        if len(superclasses) > 0:
            for _klass in listensFor:
                if isinstance(_klass, str):
                    Dispatcher.RegisterHandler(_klass, klass())
                    pass
                else:
                    _klass.AddListener(klass())
                    pass
                pass
        return klass
