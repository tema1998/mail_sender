from django import forms
from .models import SingleEmail


class EmailForm(forms.ModelForm):
    class Meta:
        model = SingleEmail
        fields = ['email', 'subject', 'message']


class MassEmailForm(forms.ModelForm):
    emails_list = forms.CharField()

    class Meta:
        model = SingleEmail
        fields = ['subject', 'message']
        # widgets = {
        #     'emails_list': forms.TextInput(attrs={'placeholder': "'email1@gmail.com', 'email2@mail.ru'"})
        # }
