from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from users.models import Guest


class Feedback(models.Model):
    score = models.PositiveSmallIntegerField()
    comment = models.CharField(max_length=140)
    commented = models.ForeignKey(Guest, related_name="%(class)s_commented")  # Persona comentada
    commentator = models.ForeignKey(Guest, related_name="%(class)s_commentator")  # Persona que comenta
    reported = models.BooleanField(default=False)

    def __str__(self):
        return 'score: ' + str(self.score) + '; commented: ' + self.commented.__str__()

class OutcomingPayment(models.Model):
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now_add=True, blank=False)
    is_executed = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

class IncomingPayment(models.Model):
    paypal_payment_id = models.CharField(max_length=140)
    paypal_sale_id = models.CharField(max_length=140)
    user = models.ForeignKey(User)
    dish = models.ForeignKey('activities.Dish', null=True, blank=True, default=None)
    activity = models.ForeignKey('activities.ActivityTime', null=True, blank=True, default=None)
    executed_incoming = models.BooleanField(default=False)
    executed_outcoming = models.BooleanField(default=False)
    outcoming_payment = models.ForeignKey(OutcomingPayment, null=True, blank=True, default=None)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    refund_id = models.CharField(max_length=140, null=True, blank=True, default=None)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

