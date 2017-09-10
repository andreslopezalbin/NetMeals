import datetime
import random
import string

import paypalrestsdk
from django.contrib.auth.models import User
from paypalrestsdk import BillingAgreement
from paypalrestsdk import BillingPlan
from paypalrestsdk import Payment
from paypalrestsdk import Payout
from paypalrestsdk import ResourceNotFound
from paypalrestsdk import Sale

from core.models import IncomingPayment
from core.services import payments_service
from netmeals.settings import HOST
from users.models import User_Plan
from django.utils.translation import ugettext_lazy as _


# netmeals
token = 'access_token$sandbox$s4xv6j5c5hgh3jbw$b6e7603b2a57c2c6915ac51969d330b5'
CLIENT_ID = 'AcgW36TC9aM9kml9lrKX-_oze10ts4JGIYfsertYZ0DjfoyeqGBTYWVCWg5Cvc2vACl2FyQfASwY_ZPQ'
SECRET = 'EIoZfr6_3k7AxeeK0ysKaOA9SKLI4EeVo8JL6amppTnRQvj09mu_hvPZhJ2uufrX-74UyDo94nAkPvta'

# Antonio
# token = 'access_token$sandbox$s4xv6j5c5hgh3jbw$b6e7603b2a57c2c6915ac51969d330b5'
# CLIENT_ID = 'AS6PPPNw9w6jyG1ln2LLyy-aeJNk2yxuD7DEsBLbrUqhOv_fhTRT1hCVfDo67hJnQaVwYiM5mTAb4_hQ'
# SECRET = 'EEQF5Alt6vA9i09irdnDmMIFFMpITieZj3y_4VN6P5mMN_5hElDQkw54OptPqWjHJg-jCQ2r4kiy9nzW'


paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": CLIENT_ID,
  "client_secret": SECRET })

def create_lite_billing_plan():
    result = None
    billing_plan = BillingPlan({
        "name": "Lite",
        "description": "NetMeals Lite Plan",
        "merchant_preferences": {
            "auto_bill_amount": "yes",
            "cancel_url": HOST + "paypal/subscription/cancel",
            "initial_fail_amount_action": "continue",
            "max_fail_attempts": "1",
            "return_url": HOST + "paypal/subscription/execute",
            # "setup_fee": {
            #     "currency": "USD",
            #     "value": "25"
            # }
        },
        "payment_definitions": [
            {
                "amount": {
                    "currency": "EUR",
                    "value": "9.99"
                },
                "charge_models": [
                    {
                        "amount": {
                            "currency": "EUR",
                            "value": "7.89"
                        },
                        "type": "SHIPPING"
                    },
                    {
                        "amount": {
                            "currency": "EUR",
                            "value": "2.10"
                        },
                        "type": "TAX"
                    }
                ],
                "cycles": "0",
                "frequency": "MONTH",
                "frequency_interval": "1",
                "name": "Lite",
                "type": "REGULAR"
            }
        ],
        "type": "INFINITE"
    })

    if billing_plan.create():
        result = billing_plan.id

    billing_plan.activate()

    return result

def create_premium_billing_plan():
    result = None
    billing_plan = BillingPlan({
        "name": "Premium",
        "description": "NetMeals Premium Plan",
        "merchant_preferences": {
            "auto_bill_amount": "yes",
            "cancel_url": HOST + "paypal/subscription/cancel",
            "initial_fail_amount_action": "continue",
            "max_fail_attempts": "1",
            "return_url": HOST + "paypal/subscription/execute",
            # "setup_fee": {
            #     "currency": "USD",
            #     "value": "25"
            # }
        },
        "payment_definitions": [
            {
                "amount": {
                    "currency": "EUR",
                    "value": "14.99"
                },
                "charge_models": [
                    {
                        "amount": {
                            "currency": "EUR",
                            "value": "11.84"
                        },
                        "type": "SHIPPING"
                    },
                    {
                        "amount": {
                            "currency": "EUR",
                            "value": "3.15"
                        },
                        "type": "TAX"
                    }
                ],
                "cycles": "0",
                "frequency": "MONTH",
                "frequency_interval": "1",
                "name": "Premium",
                "type": "REGULAR"
            }
        ],
        "type": "INFINITE"
    })

    if billing_plan.create():
        result = billing_plan.id

    billing_plan.activate()

    return result

def create_billing_agreement(plan):
    result = None

    if(plan is not None and plan.paypal_plan_id is not None):
        time_agreement = datetime.datetime.now() + datetime.timedelta(hours=1)
        billing_agreement = BillingAgreement({
            "name": "Fast Speed Agreement",
            "description": "Agreement for Fast Speed Plan",
            "start_date": time_agreement.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "plan": {
                "id": plan.paypal_plan_id
            },
            "payer": {
                "payment_method": "paypal"
            }
            # ,
            # "shipping_address": {
            #     "line1": "StayBr111idge Suites",
            #     "line2": "Cro12ok Street",
            #     "city": "San Jose",
            #     "state": "CA",
            #     "postal_code": "95112",
            #     "country_code": "US"
            # }
        })

        if billing_agreement.create():
            for link in billing_agreement.links:
                if link.rel == "approval_url":
                    result = link.href
                    break;

    return result

def create_payment(importe, description):
    result = None
    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [
            {
                "amount": {
                    "total": importe,
                    "currency": "EUR"
                    # "details": {
                    #     "subtotal": "30.00",
                    #     "tax": "0.07",
                    #     "shipping": "0.03",
                    #     "handling_fee": "1.00",
                    #     "shipping_discount": "-1.00",
                    #     "insurance": "0.00"
                    # }
                },
                "description": "Pago para " + description + " por valor de " + importe + "€",
                # "custom": "EBAY_EMS_90048630024435",
                # "invoice_number": "48787589674",
                "payment_options": {
                    "allowed_payment_method": "INSTANT_FUNDING_SOURCE"
                },
                # "soft_descriptor": "ECHI5786786",
                "item_list": {
                    "items": [
                        {
                            "name": "\"" + description + "\"",
                            # "description": "Brown hat.",
                            "quantity": "1",
                            "price": importe,
                            # "tax": "0.01",
                            # "sku": "1",
                            "currency": "EUR"
                        }
                    ],
                    # "shipping_address": {
                    #     "recipient_name": "Brian Robinson",
                    #     "line1": "4th Floor",
                    #     "line2": "Unit #34",
                    #     "city": "San Jose",
                    #     "country_code": "US",
                    #     "postal_code": "95131",
                    #     "phone": "011862212345678",
                    #     "state": "CA"
                    # }
                }
            }
        ],
        # "note_to_payer": "Contact us for any questions on your order.",
        "redirect_urls": {
            "return_url": "http://www.paypal.com/return",
            "cancel_url": "http://www.paypal.com/cancel"
        }
    })

    if payment.create():
        result = payment.id

    return result


def execute_payment(paypal_payment_id, payer_id):
    result = None
    payment = Payment.find(paypal_payment_id)
    if payment is not None:
        # PayerID is required to approve the payment.
        if payment.execute({"payer_id": payer_id}):  # return True or False
            try:
                result = payment.transactions[0].related_resources[0].sale.id
            except:
                result = None

    return result


def execute_refound(request, dish_id, activity_id):
    result = False
    incoming_payment = IncomingPayment.objects.filter(user_id=request.user.id, dish_id=dish_id, activity_id=activity_id).order_by('-date').first()
    if(incoming_payment is not None and incoming_payment.refund_id is None):
        sale = Sale.find(incoming_payment.paypal_sale_id)
        amount = float(sale['amount']['total'])
        currency = str(sale['amount']['currency'])

        if(amount > 2):
            amount = round(0.8 * (amount - 2), 2)
            amount_format = format(amount, '.2f')
            request = {
              "amount": {
                "total": amount_format,
                "currency": currency
              }
            }
            refund = sale.refund(request)

            if refund.success():
                incoming_payment.refund_id = refund.id
                incoming_payment.save()
                result = True
        else:
            result = True

    return result


def cancel_subscription(user):
    response = {"subscription_canceled": False}
    try:
        user_plan = User_Plan.objects.filter(user_id=user.id).first()
        billing_agreement = BillingAgreement.find(user_plan.paypal_agreement_id)

        cancel_note = {"note": "Suscripción al plan cancelada por el usuario con id: " + str(user.id)}

        if billing_agreement.cancel(cancel_note):
            # Would expect status has changed to Cancelled
            billing_agreement = BillingAgreement.find(user_plan.paypal_agreement_id)
            if billing_agreement.state == "Cancelled":
                response = {"subscription_canceled": True}
                user_plan.is_active = False
                user_plan.save()
        else:
            response["subscription_error"] = billing_agreement.error

    except ResourceNotFound as error:
        response["subscription_error"] = "Billing Agreement Not Found"

    return response

def send_payouts_to_users(users_payments, incoming_payments_not_paid):
    response = False

    sender_batch_id = ''.join(
        random.choice(string.ascii_uppercase) for i in range(12))

    payouts_list = []
    i = 0
    note = "Thank you for be an active part of NetMeals."
    for user_id in users_payments:
        user = User.objects.get(id=user_id)
        outcoming_payment = users_payments[user_id]
        user_payout = {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": outcoming_payment.amount,
                    "currency": "EUR"
                },
                "receiver": user.email,
                "note": note,
                "sender_item_id": str(i)
            }
        i += 1
        payouts_list.append(user_payout)

    payout = Payout({
        "sender_batch_header": {
            "sender_batch_id": sender_batch_id,
            "email_subject": "You have a payment"
        },
        "items": payouts_list
    })

    if payout.create():
        batch_id = payout.batch_header.payout_batch_id
        payout = Payout.find(batch_id)
        for outcoming_payment in users_payments.values():
            outcoming_payment.save()
            payments_service.update_incoming_payments(incoming_payments_not_paid)




    return response