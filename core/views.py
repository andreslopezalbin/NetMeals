from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext

from core.services import paypal_service
from users.util.users_util import *

from django.http.response import HttpResponseRedirect, JsonResponse
from django.utils import translation

from django.views.decorators.csrf import csrf_protect

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
        importe = request.POST['importe']
        description = request.POST['description']
        payment_id = paypal_service.create_payment(importe, description)
        if(payment_id is not None):
            response = {"payment_id" : payment_id}
    return JsonResponse(response)

def paypal_execute_payment(request):
    response = {}
    if request.method == "POST":
        payment_id = request.POST['paymentID']
        payer_id = request.POST['payerID']
        is_executed = paypal_service.execute_payment(payment_id, payer_id)
        if(is_executed):
            response = {"payment_id" : payment_id,
                        "executed" : is_executed}
    return JsonResponse(response)


