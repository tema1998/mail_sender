from django.test import TestCase

from django_celery_beat.models import IntervalSchedule

from core.forms import *


class SendEmailFormTest(TestCase):
    def test_clean_email_list(self):
        form_data = {
            'subject': 'subject',
            'message': 'message',
            'emails_list': 'a1@mail.ru, a2@mail.ru, "a3@mail.ru", a@.ru, a1, @mail.ru'
        }
        form = SendEmailForm(data=form_data)
        cd = {}
        if form.is_valid():
            cd = form.cleaned_data
        self.assertEqual(len(cd['emails_list']), 3)


class CreateTaskFormTest(TestCase):
    def test_clean_email_list(self):
        interval = IntervalSchedule.objects.create(every=1, period='minutes')
        form_data = {
            'name': 'name',
            'interval': interval,
            'subject': 'subject',
            'message': 'message',
            'emails_list': 'a1@mail.ru, a2@mail.ru, "a3@mail.ru", a@.ru, a1, @mail.ru'
        }
        form = CreateTaskForm(data=form_data)
        cd = {}
        if form.is_valid():
            cd = form.cleaned_data
        self.assertEqual(len(cd['emails_list']), 3)


class SignupFormTest(TestCase):

    def test_signup_form_field_labels(self):
        form = SignupForm()
        self.assertTrue(form.fields['password'].label == 'Password')
        self.assertTrue(form.fields['password2'].label == 'Repeat password')

    def test_signup_form_passwords_are_not_equal(self):
        form_data = {'username': 'user1',
                     'password': 'pass123',
                     'password2': 'pass321',
                     'email': 'email@mail.ru'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_signup_form_passwords_are_equal(self):
        form_data = {'username': 'user1',
                     'password': 'pass123',
                     'password2': 'pass123',
                     'email': 'email@mail.ru'}
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())
