from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
import os
from netmeals import settings

def send_mail(request, dish):
    subject, to = 'Lugar de reunión', 'netmeals.dev@gmail.com'
    html_content = render_to_string('dish/suscription_ok.html', {'dish': dish})  # ...

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject=subject, body=html_content, from_email=None, to=[to])

    msg.attach_alternative(html_content, "text/html")
    msg.mixed_subtype = 'related'

    file_path = os.path.join(settings.STATICFILES_DIRS, 'images/logo-gris.png')

    fp = open(file_path, 'rb')

    msg_img = MIMEImage(fp.read())
    fp.close()
    msg_img.add_header('Content-ID', '<{}>'.format('logo-gris.png'))
    msg.attach(msg_img)

    msg.send()
