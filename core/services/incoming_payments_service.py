import datetime

from core.models import IncomingPayment

EVENT_TYPE_DISH = "dish"
EVENT_TYPE_ACTIVITY = "activity"

def create_incoming_payment(amount, event_id, event_type, user, paypal_payment_id):
    if(event_id is not None):
        activity_id = None
        dish_id = None
        if(event_type == EVENT_TYPE_DISH):
            dish_id = int(event_id)
        else:
            activity_id = int(event_id)

        incoming_payment = IncomingPayment(
            paypal_payment_id= paypal_payment_id,
            user_id = user.id,
            dish_id = dish_id,
            activity_id = activity_id,
            date = datetime.datetime.now(),
            amount = float(amount)
        )

        return incoming_payment

def update_executed_payment(paypal_payment_id):
    incoming_payment = IncomingPayment.objects.filter(paypal_payment_id=paypal_payment_id).first()
    incoming_payment.executed_incoming = True
    incoming_payment.save()

    return incoming_payment