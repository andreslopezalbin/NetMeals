from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from activities.forms.DishForm import DishForm
from activities.models import Dish
from users.decorators.user_decorators import group_required
from users.templatetags.user_tags import has_group
from django.views.generic import View


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


def details(request, dish_id):
    dish = Dish.objects.get(id=dish_id)
    # if request.user.groups.filter(name='Chef').exists() and dish.owner == request.user.guest.chef:
    context = {'dish': dish}
    return render(request, '../templates/dish/details.html', context)
    # else:
    #     return render(request, '../../core/templates/no_permission.html')


@method_decorator(group_required('Chef'), name='dispatch')
class EditDish(View):
    def get(self, request):
        form = DishForm()
        context = {
            'form': form,
        }
        return render(request, 'dish/view_edit.html', context)

    def post(self, request):
        form = DishForm(request.POST)
        if form.is_valid():
            dish = form.create(request)
            self.save(dish);
            return redirect("my_dishes")
        else:
            context = {
                'form': form,
            }
            return render(request, 'dish/view_edit.html', context)

    def save(self, dish):
        if not dish.photo:
            dish.photo = "/static/images/dish-food-1.jpg"
        dish.save()
