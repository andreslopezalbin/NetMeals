from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Guest(User):
    def __str__(self):
        return self.get_username()

    class Meta:
        pass


class Plan(models.Model):
    class Meta:
        # This model will not be used to create any database table
        abstract = True


class Host(Guest):
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
