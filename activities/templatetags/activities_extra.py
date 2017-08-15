from django import template

from activities.models import Activity, ActivityTime
from users.models import Guest

register = template.Library()

@register.filter
def is_subscribed(user, activity_id):
    result = False
    if (activity_id is not None):
        result = Guest.objects.get(id=user.id).activity_assisted.filter(id=activity_id).__len__() == 1

    return result

@register.filter
def is_activity_owner(user, activity_id):
    result = False
    if(activity_id is not None):
        result = Activity.objects.get(id=activity_id).owner.id == user.id

    return result