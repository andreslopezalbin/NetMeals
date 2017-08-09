from django.http import JsonResponse
from django.views import View

from core.services import paypal_service
from core.util.session_constants import SESSION_USER_ROLES, SESSION_USER_PLAN
from users.services.UserService import get_plan


class AddRoleView(View):
    def post(self, request):
        response = {}
        current_user = request.user
        if current_user.is_authenticated:
            roles = request.POST.getlist('selected_roles[]')
            request.session[SESSION_USER_ROLES] = roles
            plan_request = request.POST.get('selected_plan')
            plan = get_plan(plan_request)
            request.session[SESSION_USER_PLAN] = plan_request
            approval_href = paypal_service.create_billing_agreement(plan)
            if(approval_href):
                response = {"approval_href": approval_href}
        return JsonResponse(response)
