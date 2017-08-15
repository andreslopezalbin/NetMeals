from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View

from activities.models import DishFeedback, ActivityFeedback
from core.models import Feedback
from users.forms.GuestForms import SignUpForm
from users.forms.ProfileForm import GuestForm, AboutMeForm
from users.models import Guest, User_Plan
from users.services import UserService
from random import shuffle, random


class RegistrationView(View):  # Vista de la Registracion basada en vistas de Django ( View )

    def get(self, request):
        form = SignUpForm()
        context = {
            'form': form,
        }
        return render(request, 'signup.html', context)

    @transaction.atomic
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            guest = UserService.create_guest(form)
            password = form.cleaned_data.get('password')
            guest.set_password(password)
            UserService.save(guest)
            return render(request, 'signup-host.html')
        else:
            message = ""
            for field, errors in form.errors.items():
                for error in errors:
                    message += error
            context = {
                'form': form, 'message': message
            }
            return render(request, 'registerGuest.html', context)


@login_required
@transaction.atomic
def edit_profile(request):
    guest = request.user.guest
    if request.method == "POST":
        form = GuestForm(data=request.POST, instance=guest, prefix='guest')
        if form.is_valid():
            form.save()
            return redirect("profile", guest.username)
        else:
            context = {
                'guest_form': form,
            }
    else:
        guest_form = GuestForm(instance=guest, prefix='guest')
        subscription = User_Plan.objects.filter(user_id=request.user.id).first()
        context = {'guest_form': guest_form,
                   'is_subscribed': subscription is not None and subscription.is_active
                   }
    return render(request, 'profile/edit_profile.html', context)


@login_required
@transaction.atomic
def edit_about_me(request):
    guest = request.user.guest
    if request.method == "POST":
        form = AboutMeForm(data=request.POST, instance=guest, prefix='guest')
        if form.is_valid():
            form.save()
            return redirect("profile", guest.username)
        else:
            context = {
                'guest_form': form,
            }
    else:
        guest_form = AboutMeForm(instance=guest, prefix='guest')
        subscription = User_Plan.objects.filter(user_id=request.user.id).first()
        context = {'guest_form': guest_form,
                   'is_subscribed': subscription is not None and subscription.is_active
                   }
    return render(request, 'profile/edit_about_me.html', context)


def view_profile(request, username):
    if request.method == "GET":
        user = Guest.objects.get(username=username)

        feedback_list = Feedback.objects.filter(commented_id=user.id).order_by('?')[:3]

        context = {'user': user, 'feedback_list': feedback_list,
                   }
        return render(request, 'profile/profile.html', context)
