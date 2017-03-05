from __future__ import unicode_literals

from django.db import models as models
from core import models as core_models
from django.contrib.auth.models import User


# Create your models here.
class Guest(User):
    def __str__(self):
        return self.get_username()

    class Meta:
        permissions = (
            ('guest', 'Guest'),
        )


class Host(Guest):
    PLAN = (
        ('B', 'Basic'),
        ('P', 'Premium'),
        ('UP', 'Ultra Premium'),
    )

    plan = models.CharField(max_length=2, choices=PLAN)

    class Meta:
        # This model will not be used to create any database table
        abstract = True

    def __str__(self):
        return self.get_username() + ':' + self.get_plan_display()


class Chef(Host):
    def __str__(self):
        return self.get_username()


class Manager(Host):
    def __str__(self):
        return self.get_username()


class Monitor(Host):
    def __str__(self):
        return self.get_username()


class Ingredients(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=50)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.TextField(max_length=30)
    description = models.TextField(max_length=250)
    owner = models.ForeignKey(Chef)
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
        return self.objects.select_related().get(ActivityTime.duration)

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
    manager = models.ForeignKey(Monitor)


class Event(models.Model):
    transaction_uid = models.TextField(max_length=50)
    date = models.DateField()

    # Relationships
    user = models.ForeignKey(Guest)
    local = models.ForeignKey(Local)
