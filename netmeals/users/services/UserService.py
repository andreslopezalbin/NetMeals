from activities.models import Guest, Monitor, Manager, Chef
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group

def create_guest(form):
    res = Guest(first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])
    return res

def create(role, current_user):
    user = None
    if current_user is not None and current_user.is_authenticated():
        if role == 'Monitor':
            user = Monitor(first_name=current_user.first_name,
                last_name=current_user.last_name,
                email=current_user.email,
                username=current_user.username,
                password=current_user.password,
                guest_ptr_id = current_user.id,
                id=current_user.id)
        elif role == 'Manager':
            user = Manager(first_name=current_user.first_name,
                last_name=current_user.last_name,
                email=current_user.email,
                username=current_user.username,
                password=current_user.password,
                guest_ptr_id=current_user.id,
                id=current_user.id)
        elif role == 'Chef':
            user = Chef(first_name=current_user.first_name,
                last_name=current_user.last_name,
                email=current_user.email,
                username=current_user.username,
                password=current_user.password,
                guest_ptr_id=current_user.id,
                id=current_user.id)
    return user
    # if user is not None:
    #     group = Group.objects.get(name=role)
    #     user.groups.add(group)

def save(user):
    user.save()
