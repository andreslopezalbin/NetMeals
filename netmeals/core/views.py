from django.shortcuts import render

from users.util.users_util import *


# Create your views here.


def index(request):
    result = "Hello, world. You're at the <app> index."
    current_user = request.user
    if(current_user is not None and current_user.is_authenticated()):
        if(is_monitor(current_user)):
            result = result + " Monitor!!!"
    return render(request, 'index.html')

def no_permission(request):
    return render(request, 'no_permission.html')


