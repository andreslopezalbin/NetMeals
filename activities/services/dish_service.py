from django.shortcuts import get_object_or_404

from activities.models import Dish
from users.models import Guest
from core.services.paypal_service import execute_refound


def subscribe(dish_id, request):
    dish = get_object_or_404(Dish, id=dish_id)
    guest = Guest.objects.get(id=request.user.id)

    if (dish.owner_id != request.user.id):
        dish.assistants.add(guest)

def unsubscribe(dish_id, request):
    dish = get_object_or_404(Dish, id=dish_id)
    execute_refound('84R42069FD595684E')

    guest = Guest.objects.get(id=request.user.id)
    # dish.assistants.remove(guest)



