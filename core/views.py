from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import Group
from django.db import transaction
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from paypalrestsdk import BillingAgreement

from activities.services import activity_service
from activities.services import dish_service
from core.models import IncomingPayment
from core.services import incoming_payments_service
from core.services import paypal_service
from core.util.session_constants import SESSION_USER_ROLES, SESSION_USER_PLAN, SESSION_SIGNEDUP_SUCCESS
from users.models import User_Plan
from users.services import UserService
from users.services.UserService import get_plan
from users.util.users_util import *

from django.http.response import HttpResponseRedirect, JsonResponse
from django.utils import translation

from django.views.decorators.csrf import csrf_protect

from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import date
import json


# Create your views here.


def index(request):
    context = {}

    if SESSION_SIGNEDUP_SUCCESS in request.session:
        context = {
            "signup_success" : True
        }
        del request.session[SESSION_SIGNEDUP_SUCCESS]

    return render(request, 'index.html', context)


def no_permission(request):
    return render(request, 'no_permission.html')


def change_language(request):
    user_language = request.GET['language']
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language

    return redirect(request.META.get('HTTP_REFERER'))


@csrf_protect
def paypal_test(request):
    if request.method == "GET":
        paypal_service.create_billing_plan()
        csrfContext = RequestContext(request)
        return render_to_response('paypal_form.html', csrfContext)

def paypal_create_payment(request):
    response = {}
    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        event_id = request.POST['eventId']
        event_type = request.POST['eventType']
        paypal_payment_id = paypal_service.create_payment(amount, description)
        if(paypal_payment_id is not None):
            incoming_payment = incoming_payments_service.create_incoming_payment(amount, event_id, event_type, request.user, paypal_payment_id)
            incoming_payment.save()

            response = {"paypal_payment_id" : paypal_payment_id}

    return JsonResponse(response)

def paypal_billing_agreement_cancel(request):
    if request.method == "GET":
        amount = request.GET['amount']
        description = request.GET['description']
        event_id = request.POST['eventId']
        event_type = request.POST['eventType']
        paypal_payment_id = paypal_service.create_payment(amount, description)
        if(paypal_payment_id is not None):
            incoming_payment = incoming_payments_service.create_incoming_payment(amount, event_id, event_type, request.user, paypal_payment_id)
            incoming_payment.save()

            response = {"paypal_payment_id" : paypal_payment_id}

    return JsonResponse(response)

@transaction.atomic
def paypal_billing_agreement_execute(request):
    if request.method == "GET":
        current_user = request.user
        if current_user.is_authenticated:
            error_roles = ''
            roles = request.session[SESSION_USER_ROLES]
            del request.session[SESSION_USER_ROLES]
            plan_request = request.session[SESSION_USER_PLAN]
            del request.session[SESSION_USER_PLAN]
            plan = get_plan(plan_request)
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

            if error_roles != '':
                pass

            token = request.GET['token']
            billing_agreement_response = BillingAgreement.execute(token)
            paypal_agreement_id = billing_agreement_response.id
            if (paypal_agreement_id is not None):
                user_plan = User_Plan(user_id=current_user.id,
                                      plan_id=plan.id,
                                      paypal_agreement_id=paypal_agreement_id)
                user_plan.save()
                request.session[SESSION_SIGNEDUP_SUCCESS] = True

    return HttpResponseRedirect("/")

def paypal_execute_payment(request):
    response = {}
    if request.method == "POST":
        paypal_payment_id = request.POST['paymentID']
        payer_id = request.POST['payerID']
        sale_id = paypal_service.execute_payment(paypal_payment_id, payer_id)
        if(sale_id):
            incoming_payments_service.update_executed_payment(paypal_payment_id, sale_id)

            response = {"payment_id" : paypal_payment_id,
                        "executed" : True}
    return JsonResponse(response)


@staff_member_required
def dashboard(request):
    users_register = (User.objects
                      .annotate(month=TruncMonth('date_joined'))  # Truncate to month and add to select list
                      .values('month')  # Group By month
                      .annotate(c=Count('id'))  # Select the count of the grouping
                      .values('month', 'c')
                      .order_by('month'))  # (might be redundant, haven't tested) select month and count)

    meses = []
    users = []
    for m in users_register[len(users_register) - 12:]:
        meses.append(m['month'].strftime("%B")[:3])
        users.append(m['c'])

    return render(request, 'dashboard/dashboard.html',
                  {'users_register': users_register, 'meses': meses, 'users': users})


@staff_member_required
def dashboard_users(request):
    user_list = User.objects.all()
    paginator = Paginator(user_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)

    return render(request, 'dashboard/table.html', {'users': users})
