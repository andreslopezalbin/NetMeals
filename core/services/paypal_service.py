import datetime

import paypalrestsdk
from paypalrestsdk import BillingAgreement
from paypalrestsdk import BillingPlan
from paypalrestsdk import Payment
from paypalrestsdk import Sale

HOST = "http://192.168.1.99:8000/"
# netmeals
# token = 'access_token$sandbox$s4xv6j5c5hgh3jbw$b6e7603b2a57c2c6915ac51969d330b5'
# CLIENT_ID = 'AcgW36TC9aM9kml9lrKX-_oze10ts4JGIYfsertYZ0DjfoyeqGBTYWVCWg5Cvc2vACl2FyQfASwY_ZPQ'
# SECRET = 'EIoZfr6_3k7AxeeK0ysKaOA9SKLI4EeVo8JL6amppTnRQvj09mu_hvPZhJ2uufrX-74UyDo94nAkPvta'

# Antonio
token = 'access_token$sandbox$s4xv6j5c5hgh3jbw$b6e7603b2a57c2c6915ac51969d330b5'
CLIENT_ID = 'AS6PPPNw9w6jyG1ln2LLyy-aeJNk2yxuD7DEsBLbrUqhOv_fhTRT1hCVfDo67hJnQaVwYiM5mTAb4_hQ'
SECRET = 'EEQF5Alt6vA9i09irdnDmMIFFMpITieZj3y_4VN6P5mMN_5hElDQkw54OptPqWjHJg-jCQ2r4kiy9nzW'


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


def execute_refound(sales_id):
    sale = Sale.find("8TP02835YE0436714")
    amount = float(sale['amount']['total'])
    currency = str(sale['amount']['currency'])
    refund = sale.refund({
      "amount": {
        "total": str(amount),
        "currency": currency
      }
    })

    if refund.success():
        print("Refund[%s] Success" % refund.id)
    else:
        print(refund.error)

# def execute_refound(sale_id):
#     sale = Sale.find(sale_id)
#     currency = str(sale['amount']['currency'])
#
#     amount = sale['amount']['total']
#     # importe = (amount-amount*0.05)
#
#     refund = sale.refund({
#         "amount": {
#             "total": amount,
#             "currency": currency
#         }})
#
#     if refund.success():
#         print("Refund[%s] Success" % refund.id)
#     else:
#         print(refund.error)
