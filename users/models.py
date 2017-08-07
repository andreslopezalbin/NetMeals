from __future__ import unicode_literals

from statistics import mode

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Guest(User):
    photo = models.ImageField(upload_to='media/', null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)

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

class Plan(models.Model):
    paypal_plan_id = models.CharField(max_length=140)
    amount = models.DecimalField(max_digits=9 , decimal_places=2)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=140)

class User_Plan(models.Model):
    user = models.ForeignKey(User)
    plan = models.ForeignKey(Plan)
    paypal_agreement_id = models.CharField(max_length=140)