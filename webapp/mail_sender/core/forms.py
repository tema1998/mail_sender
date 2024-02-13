from django import forms
from .models import *
from django_celery_beat.models import PeriodicTask


class EmailForm(forms.ModelForm):
    class Meta:
        model = SingleEmail
        fields = ['email', 'subject', 'message']


class MassEmailForm(forms.ModelForm):
    emails_list = forms.CharField()

    class Meta:
        model = MassEmail
        fields = ['subject', 'message']


class CreateTaskForm(forms.ModelForm):
    emails_list = forms.CharField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = PeriodicTask
        fields = ['name', 'interval']
