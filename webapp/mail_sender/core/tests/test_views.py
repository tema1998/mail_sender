import unittest

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from unittest.mock import patch, Mock

from celery.app import task
from django.urls import reverse
from django_celery_beat.models import IntervalSchedule, PeriodicTask

import core
from core.models import EmailData, TaskCore


class IndexTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_use_correct_template_GET(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')


class SendEmailTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='ivan', password='ivan', email="ivan@ma.ru")
        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_redirect_if_not_logged_in_GET(self):
        response = self.client.get(reverse('send-email'))
        self.assertRedirects(response, '/signin?next=/send-email')

    def test_auth_user_use_correct_template_GET(self):
        response = self.authorized_client.get(reverse('send-email'))

        self.assertEqual(str(response.context['user']), 'ivan')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/send_email.html')

    @patch('core.tasks.send_email_celery.delay')
    def test_sending_email_valid_form_POST(self, mock_send_email_celery):
        response = self.authorized_client.post(path=reverse('send-email'), data={
            'emails_list': 'v@mail.ru',
            'subject': 'subject1',
            'message': 'message1',
        })
        mock_send_email_celery.assert_called_with(1, {0: 'v@mail.ru'}, 'subject1', 'message1')

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/history')

    def test_sending_email_not_valid_form_POST(self):
        response = self.authorized_client.post(path=reverse('send-email'), data={
            'emails_list': 'v@mail.ru',
            'subject': '',
            'message': 'message1',
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/send_email.html')


class HistoryTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='ivan', password='ivan', email="ivan@ma.ru")
        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_redirect_if_not_logged_in_GET(self):
        response = self.client.get(reverse('history'))
        self.assertRedirects(response, '/signin?next=/history')

    def test_auth_user_use_correct_template_GET(self):
        response = self.authorized_client.get(reverse('history'))

        self.assertEqual(str(response.context['user']), 'ivan')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/history.html')


class CreateTaskTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='ivan', password='ivan', email="ivan@ma.ru")
        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.interval = IntervalSchedule.objects.create(every='1', period='hour')

    def test_redirect_if_not_logged_in_GET(self):
        response = self.client.get(reverse('create-task'))
        self.assertRedirects(response, '/signin?next=/create-task')

    def test_auth_user_use_correct_template_GET(self):
        response = self.authorized_client.get(reverse('create-task'))

        self.assertEqual(str(response.context['user']), 'ivan')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/create_task.html')

    def test_creating_task_valid_form_POST(self):
        response = self.authorized_client.post(path=reverse('create-task'), data={
            'emails_list': 'v1@mail.ru, v2@mail.ru',
            'subject': 'subject1',
            'message': 'message1',
            'name': 'name1',
            'interval': '1',
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(PeriodicTask.objects.count(), 1)
        self.assertEquals(EmailData.objects.count(), 1)
        self.assertEquals(TaskCore.objects.count(), 1)
        self.assertRedirects(response, '/tasks')

    def test_creating_task_not_valid_form_POST(self):
        response = self.authorized_client.post(path=reverse('create-task'), data={
            'emails_list': 'v1@mail.ru, v2@mail.ru',
            'subject': 'subject1',
            'message': 'message1',
            'name': 'name1',
            'interval': '',
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/create_task.html')


class TasksTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='ivan', password='ivan', email="ivan@ma.ru")
        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_redirect_if_not_logged_in_GET(self):
        response = self.client.get(reverse('tasks'))
        self.assertRedirects(response, '/signin?next=/tasks')

    def test_auth_user_use_correct_template_GET(self):
        response = self.authorized_client.get(reverse('tasks'))

        self.assertEqual(str(response.context['user']), 'ivan')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/tasks.html')


class EnableDisableTaskTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='ivan', password='ivan', email="ivan@ma.ru")
        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.interval = IntervalSchedule.objects.create(every='1', period='hour')
        self.periodic_task_enabled = PeriodicTask.objects.create(name='name', task='123', interval=self.interval,
                                                                 enabled=True)
        self.periodic_task_disabled = PeriodicTask.objects.create(name='name1', task='123', interval=self.interval,
                                                                  enabled=False)

    def test_disable_task_POST(self):
        redirect_url = reverse('tasks')
        response = self.authorized_client.post(path=reverse('enable-disable-task'), data={
            'beat_task_id': self.periodic_task_enabled.id,
        }, HTTP_REFERER=redirect_url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/tasks')
        self.assertEquals(PeriodicTask.objects.get(id=self.periodic_task_enabled.id).enabled, False)

    def test_enable_task_POST(self):
        redirect_url = reverse('tasks')
        response = self.authorized_client.post(path=reverse('enable-disable-task'), data={
            'beat_task_id': self.periodic_task_disabled.id,
        }, HTTP_REFERER=redirect_url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/tasks')
        self.assertEquals(PeriodicTask.objects.get(id=self.periodic_task_disabled.id).enabled, True)


class DeleteTaskTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='ivan', password='ivan', email="ivan@ma.ru")
        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.email_data = EmailData.objects.create(emails={'0': 'v@mail.ru'}, subject='subject1', message='message1')
        self.interval = IntervalSchedule.objects.create(every='1', period='hour')
        self.first_periodic_task = PeriodicTask.objects.create(name='name', task='123', interval=self.interval,
                                                               enabled=True)
        self.first_core_task = TaskCore.objects.create(user=self.user, email_data=self.email_data,
                                                       task=self.first_periodic_task)

    def test_delete_periodic_and_core_task_POST(self):
        redirect_url = reverse('tasks')
        response = self.authorized_client.post(path=reverse('delete-task'), data={
            'beat_task_id': self.first_periodic_task.id,
        }, HTTP_REFERER=redirect_url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/tasks')
        self.assertEquals(PeriodicTask.objects.count(), 0)
        self.assertEquals(TaskCore.objects.count(), 0)


class SignupTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='ivan', email="ivan@ma.ru")

        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

        self.user2 = User.objects.create_user(username='user2', password='ivan', email="ivan@ma.ru")

    def test_if_user_logged_in_GET(self):
        response = self.authorized_client.get(reverse('signup'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_if_user_not_logged_in_GET(self):
        response = self.client.get(reverse('signup'))
        self.assertEquals(response.status_code, 200)

    def test_signup_uses_correct_template_GET(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'core/signup.html')

    def test_if_user_logged_in_POST(self):

        response = self.authorized_client.post(path=reverse('signup'), data={
            'username': 'user3',
            'email': 'user3@mail.ru',
            'password': 'user3',
            'password2': 'user3',
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(User.objects.count(), 2)
        self.assertRedirects(response, '/')

    def test_sign_up_POST(self):

        response = self.client.post(path=reverse('signup'), data={
            'username': 'user3',
            'email': 'user3@mail.ru',
            'password': 'user3',
            'password2': 'user3',
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(User.objects.count(), 3)
        self.assertRedirects(response, '/')

    def test_sign_up_check_data_POST(self):

        response = self.client.post(path=reverse('signup'), data={
            'username': 'user3',
            'email': 'user3@mail.ru',
            'password': 'user3',
            'password2': 'user3',
        })
        self.assertEquals(User.objects.get(id=3).username, 'user3')
        self.assertEquals(User.objects.get(id=3).email, 'user3@mail.ru')
        self.assertEquals(User.objects.get(id=3).username, 'user3')

    def test_if_passwords_are_not_equal_POST(self):

        response = self.client.post(path=reverse('signup'), data={
            'username': 'user3',
            'email': 'user3@mail.ru',
            'password': 'user3',
            'password2': 'user4',
        })
        self.assertEquals(User.objects.count(), 2)


class SigninTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='user1', email="ivan@ma.ru")

        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

        self.user2 = User.objects.create_user(username='user2', password='user2', email="ivan@ma.ru")

    def test_if_user_already_logged_in_GET(self):
        response = self.authorized_client.get(reverse('signin'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_if_user_not_logged_in_GET(self):
        response = self.client.get(reverse('signin'))
        self.assertEquals(response.status_code, 200)

    def test_signin_uses_correct_template_GET(self):
        response = self.client.get(reverse('signin'))

        self.assertTemplateUsed(response, 'core/signin.html')

    def test_if_data_incorrect_password_POST(self):
        response = self.client.post(path=reverse('signin'), data={
            'username': 'username',
            'password': 'incorrect_password',
        })
        messages = [m.message for m in get_messages(response.wsgi_request)]

        self.assertIn('Invalid username or password', messages)
        self.assertEquals(response.status_code, 200)

    def test_if_not_data_POST(self):
        response = self.client.post(path=reverse('signin'), data={
            'username': '',
            'password': '',
        })
        messages = [m.message for m in get_messages(response.wsgi_request)]

        self.assertIn('Invalid username or password', messages)
        self.assertEquals(response.status_code, 200)

    def test_if_correct_data_POST(self):
        response = self.client.post(path=reverse('signin'), data={
            'username': 'user1',
            'password': 'user1',
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))


class LogoutTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='user1', email="ivan@ma.ru")

        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

        self.user2 = User.objects.create_user(username='user2', password='user2', email="ivan@ma.ru")

    def test_logged_user_logout_POST(self):
        response = self.authorized_client.post(path=reverse('logout'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('signin'))