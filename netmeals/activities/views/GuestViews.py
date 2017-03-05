from django.db import transaction
from django.shortcuts import render
from django.views import View

from activities.forms.GuestForms import GuestRegistrationForm
from activities.services import GuestService


class RegistrationView(View):  # Vista de la Registracion basada en vistas de Django ( View )

    def get(self, request):
        form = GuestRegistrationForm()
        context = {
            'form': form,
        }
        return render(request, 'registerGuest.html', context)

    @transaction.atomic
    def post(self, request):
        form = GuestRegistrationForm(request.POST)
        if form.is_valid():
            guest = GuestService.create(form)
            password = form.cleaned_data.get('password')
            guest.set_password(password)
            GuestService.save(guest)
            return render(request, 'suc.html')
        else:
            message = ""
            for field, errors in form.errors.items():
                for error in errors:
                    message += error
            context = {
                'form': form, 'message': message
            }
            return render(request, 'registerGuest.html', context)
