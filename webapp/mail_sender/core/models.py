from django.contrib.auth.models import User
from django.db import models

from django_celery_beat.models import PeriodicTask
from django_celery_results.models import TaskResult


class EmailHistory(models.Model):
    """
    Model for storage email sending history.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emails = models.JSONField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    task_result = models.ForeignKey(TaskResult, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


class TaskCore(models.Model):
    """
    Model for storage and manage user's tasks.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emails = models.JSONField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    task = models.ForeignKey(PeriodicTask, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


class TaskHistory(models.Model):
    """
    Model for storage email sent by tasks history.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emails = models.JSONField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    task_result = models.ForeignKey(TaskResult, on_delete=models.CASCADE)
