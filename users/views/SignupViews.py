from django.contrib import auth
from django.shortcuts import render
from django.views import View
from django.db import transaction

from users.forms.GuestForms import SignUpForm
from users.services import UserService
from users.decorators.user_decorators import anonymous_required
from django.utils.decorators import method_decorator

@method_decorator(anonymous_required("/no_permission"), name='dispatch')
class SignupView(View):

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
            auth.login(request, guest)
            return render(request, 'signup-host.html')
        else:
            message = ""
            for field, errors in form.errors.items():
                for error in errors:
                    message += error
            context = {
                'form': form, 'message': message
            }
            return render(request, 'signup-host.html', context)

class SignupRolesView(View):
    def get(self, request):
        return render(request, 'signup-host.html')
