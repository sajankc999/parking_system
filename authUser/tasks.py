from django.core.mail import send_mail
from django.conf import settings
from .models import User

from celery import shared_task
@shared_task
def send_welcome_email(email):
    print("zddfa")
    send_mail(
    subject='Welcome to Par-KING',
    message='from our par-KING family we welcome ..blah ..blah ..blah',
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=[email],
    fail_silently=False,
    )