from django.core.mail import send_mail
from mail_sender.celery import app

from .services import send_email
from .models import SingleEmail


@app.task
def send_email_celery(list_of_emails, subject, message):
    send_email(list_of_emails, subject, message)


# @app.task
# def send_beat_email():
#     for contact in SingleEmail.objects.all():
#         # send_mail(
#         #     'Вы подписались',
#         #     'Будем присылать каждую минуту спам!',
#         #     'artemvol1998@gmail.com',
#         #     [contact.email],
#         #     fail_silently=False
#         # )
#         print('123')