from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
import gevent
import uuid

from .Dispatcher import Dispatcher

events = [
    "creating",
    "created",
    "updating",
    "updated",
    "deleting",
    "deleted"
]

def GetPathFromClass(klass):
    return "{}::{}".format(klass.__module__.replace('.', '::'), klass.__name__)

def SignalToEvent(signal, event=None, sender=None, hook=None):
    if event is None and hook is None:
        raise TypeError("You must define either an event or hook")

    event = str(event)

    def eventDefHook(self, sender, *args, **kwargs):
        eventName = event
        _event = None
        if hook is not None:
            _event = hook(sender, *args, **kwargs)
            eventName = str(_event)
        return eventName, _event

    def signal_hook(sender, *args, **kwargs):
        args = list(args)
        args.insert(0, sender)
        eventName, event = eventDefHook(sender, *args, **kwargs)
        if event is None:
            args.insert(0, event)
            pass
        Dispatcher.Dispatch(eventName, *args, **kwargs)
        gevent.wait()
        pass

    signal.connect(signal_hook, sender=sender, weak=False, dispatch_uid=str(uuid.uuid4()))
    pass

def RegisterSignalsFor(model):
    eventName = "events::db::{}".format(GetPathFromClass(model))
    eventsDict = {}
    for event in events:
        eventsDict[event] = "{}::{}".format(eventName, event)

    def pre_save_hook(sender, instance, *args, **kwargs):
        if instance.id is None:
            Dispatcher.Dispatch(eventsDict['creating'], instance)
            pass
        else:
            Dispatcher.Dispatch(eventsDict['updating'], instance)
            pass
        gevent.sleep()
        pass
    
    def post_save_hook(sender, instance, created, *args, **kwargs):
        if created:
            Dispatcher.Dispatch(eventsDict['created'], instance)
            pass
        else:
            Dispatcher.Dispatch(eventsDict['updated'], instance)
            pass
        gevent.sleep()        
        pass

    def pre_delete_hook(sender, instance, *args, **kwargs):
        Dispatcher.Dispatch(eventsDict['deleting'], instance)
        gevent.sleep()        
        pass

    def post_delete_hook(sender, instance, *args, **kwargs):
        Dispatcher.Dispatch(eventsDict['deleted'], instance)
        gevent.sleep()        
        pass

    pre_save.connect(pre_save_hook, sender=model, weak=False, dispatch_uid=str(uuid.uuid4()))
    post_save.connect(post_save_hook, sender=model, weak=False, dispatch_uid=str(uuid.uuid4()))
    pre_delete.connect(pre_delete_hook, sender=model, weak=False, dispatch_uid=str(uuid.uuid4()))
    post_delete.connect(post_delete_hook, sender=model, weak=False, dispatch_uid=str(uuid.uuid4()))
    return eventsDict

def dispatch(event, *args, **kwargs):
    if not isinstance(event, str):
        event = event.GetEventName()
        pass
    Dispatcher.Dispatch(event, *args, **kwargs)
    pass