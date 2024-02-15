from django import forms
from django_celery_beat.models import PeriodicTask

from .models import EmailHistory


class SendEmailForm(forms.ModelForm):
    emails_list = forms.CharField()

    class Meta:
        model = EmailHistory
        fields = ['subject', 'message']


class CreateTaskForm(forms.ModelForm):
    emails_list = forms.CharField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = PeriodicTask
        fields = ['name', 'interval']
