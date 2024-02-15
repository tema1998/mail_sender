import time

from celery import shared_task
from django.contrib.auth.models import User
from django_celery_results.models import TaskResult
from mail_sender.celery import app

from .services import send_email


from .models import TaskHistory


@app.task
def send_email_celery(list_of_emails, subject, message):
    send_email(list_of_emails, subject, message)


@shared_task(bind=True)
def send_email_beat(self, user_id, json_emails_list, subject, message):
    # send_email(list(json_emails_list.values()), subject, message)

    user = User.objects.get(id=user_id)
    task_result = TaskResult.objects.get_task(self.request.id)
    task_result.status = 'RUNNING'
    task_result.save()
    TaskHistory.objects.create(user=user, emails=json_emails_list, subject=subject, message=message,
                               task_result=task_result)
    time.sleep(15)


@shared_task
def print_smth():
    print('123')
    return '456'