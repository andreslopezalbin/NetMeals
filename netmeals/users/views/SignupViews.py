from django.shortcuts import render
from django.views import View

from activities.forms.GuestForms import SignUpForm
from activities.services import GuestService


class SignupView(View):
    def get(self, request):
        form = SignUpForm()
        context = {
            'form': form,
        }
        return render(request, 'signup.html', context)

    def post(self, request):
        form = SignUpForm(request.POST)
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

    def delete(self):
        pass

    def put(self):
        pass
