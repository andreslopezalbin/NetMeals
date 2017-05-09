from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Feedback(models.Model):
    score = models.PositiveSmallIntegerField()
    comment = models.CharField(max_length=140)
    actor = models.ForeignKey(User)

    class Meta:
        abstract = True

    def __str__(self):
        return self.actor.get_username() + ':' + self.comment


class Advertising(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=False)
    actor = models.ForeignKey(User)
    comment = models.CharField(max_length=140)

    class Meta:
        abstract = True

    def __str__(self):
        return self.actor.get_username() + ':' + self.comment
