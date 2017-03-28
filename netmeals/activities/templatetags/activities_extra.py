from django import template

from users.models import Guest

register = template.Library()

@register.filter
def is_subscribed(user, activity_id):
    return Guest.objects.get(id=user.id).activity_assisted.filter(id=activity_id).__len__() == 1