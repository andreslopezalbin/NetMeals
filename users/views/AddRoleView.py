from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.views import View

from core.services import paypal_service
from core.util.session_constants import SESSION_USER_ROLES, SESSION_USER_PLAN, SESSION_SIGNEDUP_SUCCESS
from users.models import User_Plan
from users.services import UserService
from users.services.UserService import get_plan
from users.util.users_constants import PLAN_FREE


class AddRoleView(View):
    def post(self, request):
        response = {}
        current_user = request.user
        if current_user.is_authenticated:
            roles = request.POST.getlist('selected_roles[]')
            request.session[SESSION_USER_ROLES] = roles
            plan_request = request.POST.get('selected_plan')
            plan = get_plan(plan_request)
            if plan_request == PLAN_FREE:
                for role in roles:
                    try:
                        user = UserService.create(role, current_user)
                        UserService.save(user)
                        group = Group.objects.get(name=role)
                        current_user.groups.add(group)
                        user.groups.add(group)

                    except Exception as e:
                        print(e)
                        error_roles = error_roles + role + ' '
                user_plan = User_Plan.objects.filter(user_id=current_user.id).first()
                if (user_plan is not None):
                    if (user_plan.is_active and user_plan.paypal_agreement_id is not ''):
                        paypal_service.cancel_subscription(request.user)

                    user_plan.paypal_agreement_id = ''
                    user_plan.is_active = True
                else:
                    user_plan = User_Plan(user_id=current_user.id,
                                          plan_id=plan.id,
                                          paypal_agreement_id='',
                                          is_active=True)
                user_plan.save()
                request.session[SESSION_SIGNEDUP_SUCCESS] = True
            else:
                request.session[SESSION_USER_PLAN] = plan_request
                approval_href = paypal_service.create_billing_agreement(plan)
                if(approval_href):
                    response = {"approval_href": approval_href}
        return JsonResponse(response)
