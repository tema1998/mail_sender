from django import forms
from django_celery_beat.models import PeriodicTask

from .models import EmailHistory
from .services import emails_to_json


class SendEmailForm(forms.ModelForm):
    emails_list = forms.CharField()

    class Meta:
        model = EmailHistory
        fields = ['subject', 'message']

    def clean_emails_list(self):
        """
        Method converts emails to JSON and check that we have at least one valid email.
        """
        emails_list = self.cleaned_data['emails_list']
        json_emails_list = emails_to_json(emails_list)
        if len(json_emails_list) == 0:
            raise forms.ValidationError('Required at least one valid email, for example: mail-sender@gmail.com, '
                                        'sender-email@gmail.com')
        return json_emails_list


class CreateTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        self.fields['interval'].required = True

    emails_list = forms.CharField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = PeriodicTask
        fields = ['name', 'interval']

    def clean_emails_list(self):
        """
        Method converts emails to JSON and check that we have at least one valid email.
        """
        emails_list = self.cleaned_data['emails_list']
        json_emails_list = emails_to_json(emails_list)
        if len(json_emails_list) == 0:
            raise forms.ValidationError('Required at least one valid email, for example: mail-sender@gmail.com, '
                                        'sender-email@gmail.com')
        return json_emails_list