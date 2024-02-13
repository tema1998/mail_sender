from django.contrib.auth.models import User
from django.db import models


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


class Task(models.Model):
    day_choices = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    )

    hour_choices = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
                    ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'),
                    ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'),
                    ('23', '23'), ('24', '24(0)'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=9, choices=day_choices)
    hour = models.CharField(max_length=2, choices=hour_choices)
    emails = models.JSONField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    number_of_valid_emails = models.SmallIntegerField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
