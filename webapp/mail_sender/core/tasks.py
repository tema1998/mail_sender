from time import sleep

from celery import shared_task
from django.core.mail import send_mail
from mail_sender.celery import app

from .services import send_email
from .models import SingleEmail


@app.task
def send_email_celery(list_of_emails, subject, message):
    send_email(list_of_emails, subject, message)


@shared_task
def send_email_beat(list_of_emails, subject, message):
    send_email(list_of_emails, subject, message)