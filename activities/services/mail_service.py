from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
import os
from netmeals import settings


def send_mail(request, dish):
    subject, to = 'Lugar de reunión', request.user.email
    html_content = render_to_string('dish/suscription_ok.html', {'dish': dish})  # ...

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject=subject, body=html_content, from_email=None, to=[to])

    msg.attach_alternative(html_content, "text/html")

    msg.send()
