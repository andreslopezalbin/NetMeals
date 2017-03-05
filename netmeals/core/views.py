from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from core.users.users_util import *
from core.decorators.user_decorators import group_required

# Create your views here.

from django.http import HttpResponse


def index(request):
    result = "Hello, world. You're at the <app> index."
    current_user = request.user
    if(current_user is not None and current_user.is_authenticated()):
        if(is_monitor(current_user)):
            result = result + " Monitor!!!"
    return render(request, 'index.html')

def signin(request):
    if(request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect("/")
        else:
            # Show an error page
            return HttpResponseRedirect("/")
    elif(request.method == "GET"):
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def no_permission(request):
    return render(request, 'no_permission.html')
