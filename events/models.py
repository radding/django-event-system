from django.db import models
from events.events.Observer import Observer

# Create your models here

class TestModel(models.Model):
    name = models.CharField(max_length=255)
    value = models.IntegerField()
    pass

class TestObserver(Observer):
    observes = TestModel

    def creating(self, test):
        print('creating a TestModel with name:', test.name)

    def created(self, test):
         print('created a TestModel with name:', test.name)

    def updating(self, test):
         print('updating a TestModel with name:', test.name)

    def updated(self, test):
         print('updated a TestModel with name:', test.name)

    def deleting(self, test):
         print('deleting a TestModel with name:', test.name)

    def deleted(self, test):
         print('deleted a TestModel with name:', test.name)