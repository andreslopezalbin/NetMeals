from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext

from activities.services import activity_service
from activities.services import dish_service
from core.models import IncomingPayment
from core.services import incoming_payments_service
from core.services import paypal_service
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
    result = "Hello, world. You're at the <app> index."
    current_user = request.user
    if (current_user is not None and current_user.is_authenticated()):
        if (is_monitor(current_user)):
            result = result + " Monitor!!!"
    return render(request, 'index.html')


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


def paypal_execute_payment(request):
    response = {}
    if request.method == "POST":
        paypal_payment_id = request.POST['paymentID']
        payer_id = request.POST['payerID']
        is_executed = paypal_service.execute_payment(paypal_payment_id, payer_id)
        if (is_executed):
            incoming_payment = incoming_payments_service.update_executed_payment(paypal_payment_id)

            response = {"payment_id": paypal_payment_id,
                        "executed": is_executed}
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
