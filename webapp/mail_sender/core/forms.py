from django import forms
from .models import SingleEmail


class EmailForm(forms.ModelForm):
    class Meta:
        model = SingleEmail
        fields = ['email', 'subject', 'message']

