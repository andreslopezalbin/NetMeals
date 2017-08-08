from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View

from users.forms.GuestForms import SignUpForm
from users.forms.ProfileForm import GuestForm
from users.models import User_Plan
from users.services import UserService


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
            return redirect("profile")
        else:
            context = {
                'guest_form': form,
            }
    else:
        guest_form = GuestForm(instance=guest, prefix='guest')
        subscription = User_Plan.objects.filter(user_id=request.user.id).first()
        context = {'guest_form': guest_form,
                    'is_subscribed' : subscription is not None and subscription.is_active
                   }
    return render(request, 'profile/edit_profile.html', context)


def view_profile(request):
    if request.method == "GET":
        context = {
        }
        return render(request, 'profile/profile.html', context)
