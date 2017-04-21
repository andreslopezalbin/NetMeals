from users.util.users_constants import *

def is_group_member(user, group_name):
    result = False
    user_groups = user.groups.all()
    for group in user_groups:
        if(group.name == group_name):
            result = True
            break
    return result

def is_cheff(user):
    return is_group_member(user, GROUP_CHEF)

def is_manager(user):
    return is_group_member(user, GROUP_MANAGER)

def is_monitor(user):
    return is_group_member(user, GROUP_MONITOR)

def is_admin(user):
    return is_group_member(user, GROUP_ADMIN)