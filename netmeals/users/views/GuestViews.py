from django.db import transaction
from django.shortcuts import render
from django.views import View

from users.forms.GuestForms import SignUpForm
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
