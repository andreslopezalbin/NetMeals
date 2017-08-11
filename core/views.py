from urllib.parse import urlparse

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import Group
from django.db import transaction
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.template import loader
from paypalrestsdk import BillingAgreement

from activities.models import DishFeedback
from core.services import incoming_payments_service
from core.services import paypal_service
from core.services import search_service
from core.util.session_constants import SESSION_USER_ROLES, SESSION_USER_PLAN, SESSION_SIGNEDUP_SUCCESS
from users.models import User_Plan, Guest
from users.services import UserService
from users.services.UserService import get_plan

from django.http.response import HttpResponseRedirect, JsonResponse, HttpResponse
from django.utils import translation

from django.views.decorators.csrf import csrf_protect

from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth


# Create your views here.


def index(request):
    context = {}

    if SESSION_SIGNEDUP_SUCCESS in request.session:
        context = {
            "signup_success": True
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
        if (paypal_payment_id is not None):
            incoming_payment = incoming_payments_service.create_incoming_payment(amount, event_id, event_type,
                                                                                 request.user, paypal_payment_id)
            incoming_payment.save()

            response = {"paypal_payment_id": paypal_payment_id}

    return JsonResponse(response)


def paypal_billing_agreement_cancel(request):
    if request.method == "POST":
        response = dict(paypal_service.cancel_subscription(request.user))
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
                user_plan = User_Plan.objects.filter(user_id=current_user.id).first()
                if (user_plan is not None):
                    if (user_plan.is_active):
                        paypal_service.cancel_subscription(request.user)

                    user_plan.paypal_agreement_id = paypal_agreement_id
                    user_plan.is_active = True
                else:
                    user_plan = User_Plan(user_id=current_user.id,
                                          plan_id=plan.id,
                                          paypal_agreement_id=paypal_agreement_id,
                                          is_active=True)
                user_plan.save()
                request.session[SESSION_SIGNEDUP_SUCCESS] = True

    return HttpResponseRedirect("/")


def paypal_execute_payment(request):
    response = {}
    if request.method == "POST":
        paypal_payment_id = request.POST['paymentID']
        payer_id = request.POST['payerID']
        sale_id = paypal_service.execute_payment(paypal_payment_id, payer_id)
        if (sale_id):
            incoming_payments_service.update_executed_payment(paypal_payment_id, sale_id)

            response = {"payment_id": paypal_payment_id,
                        "executed": True}
    return JsonResponse(response)


@staff_member_required
def dashboard(request):
    # rankings = DishFeedback.objects.values('commented_id').annotate(avg=Avg('score')).order_by('-avg')
    chef_ranking = Guest.objects.annotate(avg=Avg('dishfeedback_commented__score')).exclude(avg__isnull=True).values(
        'chef', 'avg').order_by('-avg')

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
    context = {'users_register': users_register,
               'meses': meses,
               'users': users,
               'dashboard': True,
               'chef_ranking': chef_ranking}
    return render(request, 'dashboard/dashboard.html', context
                  )


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

    return render(request, 'dashboard/table.html', {'users': users, 'users_dashboard': True})


@staff_member_required
def deactivate_user(request, user_id):
    result = {'is_deactivated': False}
    try:
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()
        result['is_deactivated'] = True
    except Exception:
        pass
    return JsonResponse(result)


@staff_member_required
def activate_user(request, user_id):
    result = {'is_deactivated': True}
    try:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        result['is_deactivated'] = False
    except Exception:
        pass
    return JsonResponse(result)


def rankings(request):
    chef_ranking = Guest.objects.annotate(avg=Avg('dishfeedback_commented__score')).exclude(avg__isnull=True).values(
        'username', 'photo', 'avg').order_by('-avg')
    monitor_ranking = Guest.objects.annotate(avg=Avg('activityfeedback_commented__score')).exclude(
        avg__isnull=True).values('username', 'photo', 'avg').order_by('-avg')
    context = {'chef_ranking': chef_ranking,
               'monitor_ranking': monitor_ranking}
    return render(request, 'ratings.html', context)


def search(request):
    if request.method == "GET":
        context = {}
        latitude = request.GET['latitude']
        longitude = request.GET['longitude']
        if(latitude is not None and longitude is not None):
            activities, dishes = search_service.search_by_proximity(latitude, longitude)
            context["activities"] = activities
            context["dishes"] = dishes

    return render(request, 'search.html', context)
