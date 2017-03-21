from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.views import View

from users.services import UserService


class AddRoleView(View):

    def post(self, request):
        current_user = request.user
        if(current_user.is_authenticated):
            error_roles = ''
            roles = request.POST.getlist('selected_roles[]')
            for role in roles:
                try:
                    user = UserService.create(role, current_user)
                    UserService.save(user)
                    group = Group.objects.get(name=role)
                    current_user.groups.add(group)
                    user.groups.add(group)
                except Exception as e:
                    print e
                    error_roles = error_roles + role + ' '

            if(error_roles != ''):
                pass
        return HttpResponseRedirect("/")