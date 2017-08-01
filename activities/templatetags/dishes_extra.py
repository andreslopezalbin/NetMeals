from django import template

from activities.models import Dish
from users.models import Guest

register = template.Library()

@register.filter
def is_subscribed(user, dish_id):
    result = False
    if (dish_id is not None):
        result = Guest.objects.get(id=user.id).dish_assisted.filter(id=dish_id).__len__() == 1

    return result

@register.filter
def is_dish_owner(user, dish_id):
    result = False
    if(dish_id is not None):
        result = Dish.objects.get(id=dish_id).owner.id == user.id

    return result