import datetime

from core.models import IncomingPayment, OutcomingPayment

NETMEALS_FEE = 0.2

def generate_pending_payments():
    incoming_payments_not_paid = IncomingPayment.objects.filter(executed_incoming=True, executed_outcoming=False, refund_id=None)

    users_payments = {}
    for incoming_payment in incoming_payments_not_paid:
        user = incoming_payment.activity.activity.owner.id
        outcoming_payment = None
        if user in users_payments:
            outcoming_payment = users_payments[user.id]
            outcoming_payment.amount = outcoming_payment.amount + get_amount_with_fee_applied(incoming_payment.amount)
        else:
            outcoming_payment = generate_outcoming_payment(incoming_payment, user)
            users_payments[user] = outcoming_payment

        incoming_payment.outcoming_payment = outcoming_payment


    return users_payments, incoming_payments_not_paid

def update_incoming_payments(incoming_payments):

    for incoming_payment in incoming_payments:
        IncomingPayment.objects.filter(id=incoming_payment.id).update(
            executed_outcoming=True
        )

    incoming_refund_payments_not_paid = IncomingPayment.objects.filter(executed_incoming=True, executed_outcoming=False,
                                                                       refund_id=not None)

    for incoming_payment in incoming_refund_payments_not_paid:
        IncomingPayment.objects.filter(id=incoming_payment.id).update(
            executed_outcoming=True
        )




def get_amount_with_fee_applied(amount):
    return (1 - NETMEALS_FEE) * float(amount)

def generate_outcoming_payment(incoming_payment, user):
    user_payment = get_amount_with_fee_applied(incoming_payment.amount)
    outcoming_payment = OutcomingPayment(
        user_id=user,
        creation_date = datetime.datetime.now(),
        is_executed = False,
        amount = user_payment
    )

    return outcoming_payment