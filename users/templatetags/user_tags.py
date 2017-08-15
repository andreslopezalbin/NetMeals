# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import date
from django.utils.translation import ugettext_lazy as _

# Stdlib imports

# Core Django imports
from django import template

# Third-party app imports

# Realative imports of the 'app-name' package


register = template.Library()


@register.filter('has_group')
def has_group(user, group_name):
    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False


@register.filter(name='times')
def times(number):
    return range(number)


@register.filter(name='years')
def times(birthday):
    if birthday is not None:
        today = date.today()
        return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


@register.filter(name='dish_media')
def dish_media(dish):
    if dish is not None:
        feedbacks = dish.dishfeedback_set.all()
        media = 0
        for feedback in feedbacks:
            media += feedback.score
        return media / len(feedbacks)


@register.filter(name='activity_media')
def dish_media(activity):
    if activity is not None:
        feedbacks = activity.activityfeedback_set.all()
        media = 0
        for feedback in feedbacks:
            media += feedback.score
        return media / len(feedbacks)


@register.filter(name='activity_assisted')
def activity_assisted(activity):
    if activity is not None:
        activitytime_set = activity.activitytime_set.all()
        assistants = 0
        for activitytime in activitytime_set:
            assistants += len(activitytime.assistants.all())
        return assistants
