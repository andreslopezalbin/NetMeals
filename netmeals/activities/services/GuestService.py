from activities.models import Guest
from django.contrib.auth.models import Permission


def create(form):
    res = Guest(first_name=form.cleaned_data['first_name'],
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])
    return res


def save(guest):
    guest.save()
    guest.user_permissions.add(Permission.objects.get(codename="guest"))
