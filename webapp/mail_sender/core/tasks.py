import time

from celery import shared_task
from django.contrib.auth.models import User
from django_celery_results.models import TaskResult

from mail_sender.celery import app
from .services import send_email
from .models import EmailHistory, TaskHistory


@app.task(bind=True)
def send_email_celery(self, user_id, json_emails_list, subject, message):
    """
    Task receive user id and data for sending emails,
    create task for sending emails, then use task_id to
    create a result of sending emails with status 'RUNNING',
    when task will be finished - result will be 'SUCCESS'.
    """

    user = User.objects.get(id=user_id)
    task_result = TaskResult.objects.get_task(self.request.id)
    task_result.status = 'RUNNING'
    task_result.save()
    EmailHistory.objects.create(user=user, emails=json_emails_list, subject=subject, message=message,
                                task_result=task_result)

    send_email(list(json_emails_list.values()), subject, message)

@shared_task(bind=True)
def send_email_beat(self, user_id, json_emails_list, subject, message):
    """
    Task receive user id and data for sending emails,
    create task for sending emails, then use task_id to
    create a result of sending emails with status 'RUNNING',
    when task will be finished - result will be 'SUCCESS'.
    """

    user = User.objects.get(id=user_id)
    task_result = TaskResult.objects.get_task(self.request.id)
    task_result.status = 'RUNNING'
    task_result.save()
    TaskHistory.objects.create(user=user, emails=json_emails_list, subject=subject, message=message,
                               task_result=task_result)

    send_email(list(json_emails_list.values()), subject, message)
