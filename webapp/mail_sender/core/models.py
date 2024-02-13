from django.contrib.auth.models import User
from django.db import models

from django_celery_beat.models import PeriodicTask


class SingleEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class MassEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emails = models.JSONField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    number_of_valid_emails = models.SmallIntegerField()
    status = models.BooleanField(default=False)

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