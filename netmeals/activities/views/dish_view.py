from django.shortcuts import render

from activities.models import Dish
from users.templatetags.user_tags import has_group


def findall(request):
    if request.method == "GET":
        dishes = Dish.objects.all()
        context = {'dishes': dishes}
        return render(request, '../templates/dish/list.html', context)


def findmine(request):
    if request.user.groups.filter(name='Chef').exists():
        dishes = request.user.guest.chef.dish_set.all()
        context = {'dishes': dishes}
        return render(request, '../templates/dish/list.html', context)
    else:
        return render(request, '../../core/templates/no_permission.html')
