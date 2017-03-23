from __future__ import unicode_literals

from django.db import models as models
from core import models as core_models
from django.contrib.auth.models import User
from users.models import Chef, Guest, Manager, Monitor


# Create your models here.

class Ingredients(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=50)

    def __str__(self):
        return self.name


default_pic = 'http://i.huffpost.com/gen/1452575/images/o-BEAUTIFUL-FOOD-facebook.jpg'


class Dish(models.Model):
    name = models.TextField(max_length=30)
    description = models.TextField(max_length=250)
    owner = models.ForeignKey(Chef)
    photo = models.URLField(default=default_pic)
    ingredients = models.ManyToManyField(Ingredients)
    assistants = models.ManyToManyField(Guest, related_name='dish_assisted')

    def __str__(self):
        return self.name + ':' + self.owner.get_username()


class Feedback(core_models.Feedback):
    dish = models.ForeignKey(Dish)

    def __str__(self):
        return self.actor.get_username() + ':' + self.comment + ':' + self.dish


class Activity(models.Model):
    name = models.TextField(max_length=30)
    description = models.TextField(max_length=250)
    place = models.TextField(max_length=250)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    # Relationships
    owner = models.ForeignKey(Monitor)
    assistants = models.ManyToManyField(Guest, related_name='activity_assisted')

    @property
    def estimated_duration(self):
        pass

    def __str__(self):
        return self.name + ':' + self.owner.get_username()


class ActivityTime(models.Model):
    date = models.DateTimeField()
    duration = models.DecimalField(max_digits=5, decimal_places=2)

    # Relationships
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return self.activity.name + ':' + self.date


class Local(models.Model):
    name = models.TextField(max_length=30)
    description = models.TextField(max_length=250)
    address = models.TextField(max_length=250)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    manager = models.ForeignKey(Manager)


class Event(models.Model):
    transaction_uid = models.TextField(max_length=50)
    date = models.DateField()

    # Relationships
    user = models.ForeignKey(Guest)
    local = models.ForeignKey(Local)
