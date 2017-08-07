from users.models import *
from users.util.users_constants import *

def create_guest(form):
    res = Guest(first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])
    return res

def get_plan(plan):
    result = None
    plan = Plan.objects.filter(name=plan).first()

    if(plan is not None):
        result = plan

    return result

def create(role, current_user):
    user = None
    if current_user is not None and current_user.is_authenticated():
        if role == GROUP_MONITOR:
            user = Monitor(first_name=current_user.first_name,
                last_name=current_user.last_name,
                email=current_user.email,
                username=current_user.username,
                password=current_user.password,
                guest_ptr_id = current_user.id,
                id=current_user.id
            )
        elif role == GROUP_MANAGER:
            user = Manager(first_name=current_user.first_name,
                last_name=current_user.last_name,
                email=current_user.email,
                username=current_user.username,
                password=current_user.password,
                guest_ptr_id=current_user.id,
                id=current_user.id
            )
        elif role == GROUP_CHEF:
            user = Chef(first_name=current_user.first_name,
                last_name=current_user.last_name,
                email=current_user.email,
                username=current_user.username,
                password=current_user.password,
                guest_ptr_id=current_user.id,
                id=current_user.id
            )
    return user
    # if user is not None:
    #     group = Group.objects.get(name=role)
    #     user.groups.add(group)

def save(user):
    user.save()
