import json
from datetime import date
from urllib.parse import urlparse

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import View

from activities.forms.DishForm import DishForm
from activities.models import Dish, Guest
from activities.services import dish_service

from activities.forms.DishFeedbackForm import DishFeedbackForm
from core.services import paypal_service


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


def schedule(request):
    if request.method == "GET" and request.user.groups.filter(name='Chef').exists():
        dishes = request.user.guest.chef.dish_set.all()
        user_language = request.LANGUAGE_CODE
        today = date.today()
        items = []
        for dish in dishes:
            item = {'title': dish.name,
                    'url': 'details/' + str(dish.id),
                    'start': str(dish.date) + " " + str(dish.hour),
                    'color': '#257e4a'}

            items.append(item)
        data = json.dumps(items)
        context = {'items': data, 'language': user_language, 'today': today}
        return render(request, '../templates/dish/scheduler.html', context)


def details(request, dish_id):
    dish = Dish.objects.get(id=dish_id)
    # if request.user.groups.filter(name='Chef').exists() and dish.owner == request.user.guest.chef:
    available_seats = dish.max_assistants - len(dish.assistants.all())
    context = {'dish': dish, 'available_seats': range(0, available_seats)}
    return render(request, '../templates/dish/details.html', context)
    # else:
    #     return render(request, '../../core/templates/no_permission.html')


def delete(request, dish_id):
    try:
        dish = Dish.objects.get(id=dish_id)
        if request.user.groups.filter(name='Chef').exists() and dish.owner == request.user.guest.chef:
            dish.delete()
            dishes = request.user.guest.chef.dish_set.all()
            context = {'dishes': dishes, 'deleted': True}
            return render(request, '../templates/dish/list.html', context)
        else:
            available_seats = dish.max_assistants - len(dish.assistants.all())
            context = {'dish': dish, 'available_seats': range(0, available_seats), 'delete_error': True}
            return render(request, '../templates/dish/details.html', context)
    except ObjectDoesNotExist:
        dishes = request.user.guest.chef.dish_set.all()
        context = {'dishes': dishes, 'error': True}
        return render(request, '../templates/dish/list.html', context)


@login_required
@transaction.atomic
def create(request):
    if request.user.groups.filter(name='Chef').exists():
        if request.method == "POST":
            form = DishForm(request.POST)
            if form.is_valid():
                dish = form.create(request)
                dish.save()

                return redirect("my_dishes")
            else:
                context = {
                    'form': form, 'create': True
                }
        else:
            form = DishForm(place=request.user.guest.place)
            context = {
                'form': form, 'create': True
            }
        return render(request, 'dish/edit.html', context)
    else:
        return render(request, '../../core/templates/no_permission.html')


@transaction.atomic
@login_required()
def edit(request, dish_id):
    if request.user.groups.filter(name='Chef').exists():
        dish = Dish.objects.get(id=dish_id)
        if dish.date > date.today() and len(dish.assistants.all()) == 0:
            if request.method == "POST":
                form = DishForm(data=request.POST, instance=dish, prefix='dish')
                if form.is_valid():
                    dish = form.create(request)
                    dish.save()

                    return redirect("my_dishes")
                else:
                    context = {
                        'form': form,
                    }
            else:
                form = DishForm(instance=dish, prefix='dish')
                context = {
                    'form': form,
                }
            return render(request, 'dish/edit.html', context)
        else:
            return render(request, '../../core/templates/no_permission.html')

    else:
        return render(request, '../../core/templates/no_permission.html')


class DishSubscriptionView(View):
    def post(self, request, dish_id):
        dish_service.subscribe(dish_id, request)
        result_url = "/"
        if (request.META.get('HTTP_REFERER') is not None):
            result_url = urlparse(request.META.get('HTTP_REFERER')).path

        return HttpResponseRedirect(result_url)


class DishUnsubscriptionView(View):
    def post(self, request, dish_id):
        result = {"is_refunded": False}
        is_refunded = paypal_service.execute_refound(request, dish_id, None)
        if(is_refunded):
            result["is_refunded"] = True
            dish_service.unsubscribe(dish_id, request)

        return JsonResponse(result)

def feedback(request, dish_id):
    dish = Dish.objects.get(id=dish_id)
    if request.method == "POST":
        form = DishFeedbackForm(request.POST)
        if form.is_valid():
            dishfeedback = form.save(commit=False)
            dishfeedback.dish = dish
            dishfeedback.commentator = request.user.guest
            dishfeedback.commented_id = dish.owner.id
            dishfeedback.save()
            # update_avg_rating(local.pk)
            return redirect('details_dish', dish_id=dish_id)
    else:
        form = DishFeedbackForm()
    return render(request, 'dish/feedback.html', {'form': form})
