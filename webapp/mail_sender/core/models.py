from django.contrib.auth.models import User
from django.db import models

from django_celery_beat.models import PeriodicTask
from django_celery_results.models import TaskResult


class EmailHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emails = models.JSONField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    task_result = models.ForeignKey(TaskResult, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


class TaskCore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emails = models.JSONField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    task = models.ForeignKey(PeriodicTask, on_delete=models.CASCADE)
    number_of_valid_emails = models.SmallIntegerField()

    def __str__(self):
        return self.subject


class TaskHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emails = models.JSONField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    task_result = models.ForeignKey(TaskResult, on_delete=models.CASCADE)

    # def __str__(self):
    #     return str(self.id)