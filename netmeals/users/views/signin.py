from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from users.forms import LoginForm


class LoginView(View):
    def get(self, request):
        error_messages = []
        form = LoginForm()
        context = {
            'errors': error_messages,
            'login_form': form
        }
        return render(request, '../templates/login.html', context)

    def post(self, request):
        error_messages = []
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('usr')
            password = form.cleaned_data.get('pwd')
            user = authenticate(username=username, password=password)
            if user is None:
                error_messages.append('incorrect pass')
            else:
                if user.is_active:
                    auth.login(request, user)
                    url = request.GET.get('next',
                                          'index')  # si no existe parametro GET 'next', le mandamos a 'photos_home'
                    return redirect(url)
                else:
                    error_messages.append('inactive user')
        context = {
            'errors': error_messages,
            'login_form': form
        }
        return render(request, '../templates/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
