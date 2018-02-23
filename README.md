# django-events
A great little utility to implement an event system for django

## About
django-events utilizes gevent to build out an easy to use event system. This event system uses strings to track events and call event handlers.

### Why not just use django's built in signals?
Unlike django signals, django-events utilizes a string based system for events. This allows developers to listen using regular expressions, and add a slightly nicer interface to interact and deal with events. For example you can create events like `event::db::Model::created`, `event::db::Model::updated`, and `event::db::Model::deleted` and have a listener that listens for `event::db::Model::.*`. This listener will handle all of the defined events. 

## Install
django-events requires python3 and django 1.7+. To install, just run `pip install django-events`

## Getting started
To get started add `"events"` to your `installed_apps` in `settings.py`. That's really it.

### The Dispatcher
The Dispatcher is the central peice to django-events, every single event goes through the dispatcher. While there really isn't a need to use the dipsatcher directly, you can. The dispatcher manages the event queue, the handlers, and dispatching the event. 

#### Registering Event Handlers
In order to start using the dispatcher, you first need to define your handlers:

```python
from events import Dispatcher

Dispatcher.RegisterHandler('event::name', handler)
```

This will define a handler that will respond to `event::name` events. The handler object must be a callable object (like a function or a class with `__call__` defined). 

While it is not necessary, I recommend that you use `::` rather than `.` in your event handlers because the string you pass into register handler gets compiled into regular expression. If you want to base events off of a class and its module, there is a utility called `GetPathFromClass` you can use.

You can also, define a handler that responds to multiple events by using regular expressions:

```python
from events import Dispatcher

Dispatcher.RegisterHandler('event::name(.*)', handler)
```

This handler will respond to any event that has a tag that begins with `event::name`. This handler will respond to `event::name::some_event` as well as `event::name:some::other::event`

#### Dispatching events
To Dispatch an event, all you need to do is call `Dispatcher.Dispatch('event::name')`. This call will call every listener that is waiting for that event.

If you need to pass arguments to an event handler, all you need to is: `Dispatcher.Dispatch('event::name', *args, **kwargs)`

### The `Event` class
The `Event` class is really just here to stop you from making mistakes. All the `Event` class does is build a string for your event and gives you a `Dispatch` helper.

For example:

```python
from events import Event

class ExampleEvent(Event):
    pass
```

This makes an event that will always have the string `<modulename>::ExampleEvent`. To dispatch an `ExampleEvent`, all you need to do is `ExampleEvent.Dispatch()`. This will actually dispatch a `<modulename>::ExampleEvent` event.

If you want to give your event classes a different name, you can just define the `Name` property on the class:

```python
from events import Event

class ExampleEvent(Event):
    Name = "ExampleEvent"
    pass
```

Now `ExampleEvent.Dispatch()` will dispatch an `ExampleEvent` event.

If you want to pass data using an `Event` class, use the `__init__` method to capture the input:

```python
from events import Event

class ExampleEvent(Event):
    def __init__(self, name, value, something):
        self.name = name
        self.value = value
        self.something = something
        pass
    pass
```

Then when dispatching: `ExampleEvent.Dispatch('name', 'value, 'something')`. This will pass an `ExampleEvent` object to the handler with `name`, `value`, and `something` defined.

### The `EventListener` class

This class sets up an event listener for you. If you use this class, you don't need to do anything more than define a `listensFor` list and a `handle` method. The `handle` method will recieve the event that triggered the handler:

```python
from events import EventListener
from my.events import ExampleEvent

class ExampleEventListener(EventListener):
    listensFor = [
        ExampleEvent,
    ]

    def handle(self, event):
        # handle the event here
        pass
    pass
```

Then, when you call `ExampleEvent.Dispatch`, `ExampleEventListener`'s `handle` method will automatically get called, with event refering to the `ExampleEvent` that triggered the handler.

The `listensFor` list can contain both `Event` objects and strings. These will also be compiled into regular expressions. This allows you to have an `EventListener` listen for all events for example:


```python
from events import EventListener

class ExampleEventListener(EventListener):
    listensFor = [
        '.*',
    ]

    def handle(self, event, *args, **kwargs):
        print("Event was dispatched: ", event)
        pass
    pass
```

### The `Observer` class
In order to respond to model events, I implemented a Model observer class called `Observer`. Using this model, you can respond to events such as creating, created, updating, updated, deleting, deleted a given model. And Observer has a method that corresponds to those events and recieves a Model object. To use a model Observer, simply inherit from the `Observer` class and define a `observes` model:

```python
from events import Observer
from my.models import Example

class ExampleModelObserver(Observer):
    observes = Example
    
    def creating(self, example):
        print('creating a Example with name:', example.name)

    def created(self, example):
        print('created a Example with name:', example.name)

    def updating(self, example):
        print('updating a Example with name:', example.name)

    def updated(self, example):
        print('updated a Example with name:', example.name)

    def deleting(self, example):
        print('deleting a Example with name:', example.name)

    def deleted(self, example):
        print('deleted a Example with name:', example.name)
```

When you preform an action on a Model that is being Observed, an event with the style `events::db::path::to:ModelClass::*` will be created. For example, the event for creating an Example object will be, `events::db::my::models::Example::creating`. You can define other `EventListeners` to listen for these events. For example here is a listener that listens for any model that is created:

```python
from events import EventListener

class ExampleEventListener(EventListener):
    listensFor = [
        'events::db::(.*)::created',
    ]

    def handle(self, event, example):
        print("An Example was created:", example)
        pass
    pass
```

One thing to note is that only objects that have an `Observer` defined will create events. If you want a Model to dispatch events without defining an `Observer`, you can use `RegisterSignalsFor` to map the signals to Events:

```python
from events import RegisterSignalsFor
from my.models import Example

RegisterSignalsFor(Example)
```

Now the signals will dispatch events. I recommend doing this as early in your application as possible.

### Mapping Signals to Events
Django commes with it's own signal ideas. If you want to listen for some event in django, you would use a signal. But, as these signals are object based, its more boiler plate to listen to multiple signals or to listen to a class of events. 

But django is based on signals, so in order to make it easier to just use events instead, django-events comes with `SignalToEvent` to help convert a signal to an event. Basically, this just connects a listener to a signal and then dispatches an event. The way this works is like so:

```python
from events import SignalToEvent
from some.signals import signal

SignalToEvent(signal, event='event::from::signal')

# OR

SignalToEvent(signal, event=ExampleEvent)
```

If you want to handle events from a specific sender, you can also define a sender on the `SignalToEvent` call:

```python
SignalToEvent(signal, event=ExampleEvent, sender=SomeSender)
```

And finally, sometimes you just want to have more complex event dispatching. For that you can define a hook:

```python
def hook(*args, **kwargs):
    if args[0] == 1:
        return 'event::when::1'
    elif args[1] == 2:
        return 'event::when::2'
    return 'event::when::none'
    
SignalToEvent(signal, hook=hook)
```

the hook function must return an event or a string!

*Note:* Do not call `Event.Dispatch` inside of a hook function. If you do, the event will be dispatched twice!

## Testing
If you would like to test that certain events are raised during the course of your unit tests, django-events provide several utilies to make that easier.

### `Dispatcher.MocksDispatch` decorator
This decorator mocks and puts the Dispatcher into a test mode. In  side this environment, you are able to use a function like `Dispatcher.Expect()`.

Usage:

```python
from events.events import Dispatcher
from django.test import TestCase

class TestExample(TestCase):

    @Dispatcher.MocksDispatch
    def test_SignalToEvent(self):
        Dispatcher.Expect('some::event::to::be::fired')
        Dispatcher.Dispatch('some::event::to::be::fired')
        pass
    pass
```

### `Dispatcher.Expect()`
This lets the dispatcher know you are looking for this event, but to not actually call the listeners on the event. If the event is never called, the test will fail and the message will tell you exactly what events where not raised.
