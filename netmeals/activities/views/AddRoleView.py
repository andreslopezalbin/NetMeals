from django.contrib.auth.models import Group
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect

class AddRoleView(View):

    def post(self, request):
        current_user = request.user
        if(current_user.is_authenticated):
            error_roles = ''
            roles = request.POST.getlist('selected_roles[]')
            for role in roles:
                try:
                    group = Group.objects.get(name=role)
                    current_user.groups.add(group)
                except Exception:
                    error_roles = error_roles + role + ' '

            if(error_roles != ''):
                pass
        return HttpResponseRedirect("/")