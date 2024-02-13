from django import forms
from .models import *


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

    class Meta:
        model = Task
        fields = ['day', 'hour', 'subject', 'message']