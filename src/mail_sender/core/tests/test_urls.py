from core.views import *
from django.test import SimpleTestCase
from django.urls import resolve, reverse


class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse("index")
        self.assertEqual(resolve(url).func.view_class, Index)

    def test_send_email_url_resolves(self):
        url = reverse("send-email")
        self.assertEqual(resolve(url).func.view_class, SendEmail)

    def test_history_url_resolves(self):
        url = reverse("history")
        self.assertEqual(resolve(url).func.view_class, History)

    def test_create_task_url_resolves(self):
        url = reverse("create-task")
        self.assertEqual(resolve(url).func.view_class, CreateTask)

    def test_tasks_url_resolves(self):
        url = reverse("tasks")
        self.assertEqual(resolve(url).func.view_class, Tasks)

    def test_enable_disable_task_url_resolves(self):
        url = reverse("enable-disable-task")
        self.assertEqual(resolve(url).func.view_class, EnableDisableTask)

    def test_delete_task_url_resolves(self):
        url = reverse("delete-task")
        self.assertEqual(resolve(url).func.view_class, DeleteTask)

    def test_signup_url_resolves(self):
        url = reverse("signup")
        self.assertEqual(resolve(url).func.view_class, Signup)

    def test_signin_url_resolves(self):
        url = reverse("signin")
        self.assertEqual(resolve(url).func.view_class, Signin)

    def test_logout_url_resolves(self):
        url = reverse("logout")
        self.assertEqual(resolve(url).func.view_class, Logout)
