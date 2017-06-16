from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models as models
from core import models as core_models
from django.contrib.auth.models import User
from users.models import Chef, Guest, Manager, Monitor
from django.utils.translation import ugettext_lazy as _


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
    photo = models.URLField()
    ingredients = models.ManyToManyField(Ingredients)
    max_assistants = models.PositiveIntegerField(default=1)
    assistants = models.ManyToManyField(Guest, related_name='dish_assisted')
    contribution = models.DecimalField(default=1.0, max_digits=4, decimal_places=2)
    date = models.DateField()
    hour = models.TimeField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            if not self.photo:
                self.photo = "/static/images/dish-food-1.jpg"
        except:
            # when new photo then we do nothing, normal case
            pass
        super(Dish, self).save(*args, **kwargs)



class Feedback(core_models.Feedback):
    dish = models.ForeignKey(Dish)

    def __str__(self):
        return self.actor.get_username() + ':' + self.comment + ':' + self.dish


class Activity(models.Model):
    name = models.TextField(max_length=70)
    short_description = models.TextField(max_length=140)
    description = models.TextField(max_length=250)
    place = models.TextField(max_length=250)
    latitude = models.DecimalField(max_digits=23, decimal_places=20)
    longitude = models.DecimalField(max_digits=23, decimal_places=20)
    photo = models.ImageField(upload_to='media/', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    price_per_person = models.DecimalField(max_digits=5, decimal_places=2)
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
    start_hour = models.TextField(max_length=5)
    end_hour = models.TextField(max_length=5)

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
