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


