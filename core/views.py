from django.shortcuts import render, redirect

from users.util.users_util import *

from django.http.response import HttpResponseRedirect
from django.utils import translation


# Create your views here.


def index(request):
    result = "Hello, world. You're at the <app> index."
    current_user = request.user
    if (current_user is not None and current_user.is_authenticated()):
        if (is_monitor(current_user)):
            result = result + " Monitor!!!"
    return render(request, 'index.html')


def no_permission(request):
    return render(request, 'no_permission.html')


def change_language(request):
    user_language = request.GET['language']
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language

    return redirect(request.META.get('HTTP_REFERER'))


def prueba(request):
    return render(request, 'prueba.html')


