from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from users.models import Guest


class Feedback(models.Model):
    score = models.PositiveSmallIntegerField()
    comment = models.CharField(max_length=140)
    actor = models.ForeignKey(Guest)

    class Meta:
        abstract = True

    def __str__(self):
        return self.actor.get_username() + ':' + self.comment


from activities.models import Activity, Dish
class IncomingPayment(models.Model):
    paypal_payment_id = models.CharField(max_length=140)
    user = models.ForeignKey(User)
    dish = models.ForeignKey(Dish, null=True, blank=True, default = None)
    activity = models.ForeignKey(Activity, null=True, blank=True, default = None)
    executed_incoming = models.BooleanField(default=False)
    executed_outcoming = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    refound_id = models.CharField(max_length=140, null=True, blank=True, default = None)
    amount = models.DecimalField(max_digits=9 , decimal_places=2)


