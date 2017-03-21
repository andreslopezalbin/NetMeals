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



def no_permission(request):
    return render(request, 'no_permission.html')


