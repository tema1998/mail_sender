from core.models import *
from django.test import TestCase
from django_celery_beat.models import IntervalSchedule


class EmailDataModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        EmailData.objects.create(
            emails={"0": "mail@gmail.com"}, subject="subject", message="message"
        )

    def setUp(self):
        pass

    def test_emails_label(self):
        email_data = EmailData.objects.get(id=1)
        field_label = email_data._meta.get_field("emails").verbose_name
        self.assertEquals(field_label, "Email(s)")

    def test_subject_label(self):
        email_data = EmailData.objects.get(id=1)
        field_label = email_data._meta.get_field("subject").verbose_name
        self.assertEquals(field_label, "Subject")

    def test_message_label(self):
        email_data = EmailData.objects.get(id=1)
        field_label = email_data._meta.get_field("message").verbose_name
        self.assertEquals(field_label, "Message")

    def test_verbose_names(self):
        email_data = EmailData.objects.get(id=1)
        verbose_name = email_data._meta.verbose_name
        verbose_name_plural = email_data._meta.verbose_name_plural

        self.assertEquals(verbose_name, "Email data")
        self.assertEquals(verbose_name_plural, "Emails data")


class EmailHistoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="username", email="email@mail.ru", password="password"
        )
        email_data = EmailData.objects.create(
            emails={"0": "mail@gmail.com"}, subject="subject", message="message"
        )
        task_result = TaskResult.objects.create(task_id="123")
        EmailHistory.objects.create(
            user=user, email_data=email_data, task_result=task_result
        )

    def setUp(self):
        pass

    def test_user_label(self):
        email_history = EmailHistory.objects.get(id=1)
        field_label = email_history._meta.get_field("user").verbose_name
        self.assertEquals(field_label, "User")

    def test_email_data_label(self):
        email_history = EmailHistory.objects.get(id=1)
        field_label = email_history._meta.get_field("email_data").verbose_name
        self.assertEquals(field_label, "Email(s)")

    def test_task_result_label(self):
        email_history = EmailHistory.objects.get(id=1)
        field_label = email_history._meta.get_field("task_result").verbose_name
        self.assertEquals(field_label, "Task result")

    def test_verbose_names(self):
        email_history = EmailHistory.objects.get(id=1)
        verbose_name = email_history._meta.verbose_name
        verbose_name_plural = email_history._meta.verbose_name_plural

        self.assertEquals(verbose_name, "History of emails")
        self.assertEquals(verbose_name_plural, "History of emails")


class TaskCoreModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="username", email="email@mail.ru", password="password"
        )
        email_data = EmailData.objects.create(
            emails={"0": "mail@gmail.com"}, subject="subject", message="message"
        )
        interval = IntervalSchedule.objects.create(every="1", period="hour")
        task = PeriodicTask.objects.create(name="name", task="123", interval=interval)
        TaskCore.objects.create(user=user, email_data=email_data, task=task)

    def setUp(self):
        pass

    def test_user_label(self):
        task_core = TaskCore.objects.get(id=1)
        field_label = task_core._meta.get_field("user").verbose_name
        self.assertEquals(field_label, "User")

    def test_email_data_label(self):
        task_core = TaskCore.objects.get(id=1)
        field_label = task_core._meta.get_field("email_data").verbose_name
        self.assertEquals(field_label, "Email(s)")

    def test_task_label(self):
        task_core = TaskCore.objects.get(id=1)
        field_label = task_core._meta.get_field("task").verbose_name
        self.assertEquals(field_label, "Task")

    def test_verbose_names(self):
        task_core = TaskCore.objects.get(id=1)
        verbose_name = task_core._meta.verbose_name
        verbose_name_plural = task_core._meta.verbose_name_plural

        self.assertEquals(verbose_name, "Task management")
        self.assertEquals(verbose_name_plural, "Tasks management")


class TaskHistoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="username", email="email@mail.ru", password="password"
        )
        email_data = EmailData.objects.create(
            emails={"0": "mail@gmail.com"}, subject="subject", message="message"
        )
        task_result = TaskResult.objects.create(task_id="123")
        TaskHistory.objects.create(
            user=user, email_data=email_data, task_result=task_result
        )

    def setUp(self):
        pass

    def test_user_label(self):
        task_history = TaskHistory.objects.get(id=1)
        field_label = task_history._meta.get_field("user").verbose_name
        self.assertEquals(field_label, "User")

    def test_email_data_label(self):
        task_history = TaskHistory.objects.get(id=1)
        field_label = task_history._meta.get_field("email_data").verbose_name
        self.assertEquals(field_label, "Email(s)")

    def test_task_result_label(self):
        task_history = TaskHistory.objects.get(id=1)
        field_label = task_history._meta.get_field("task_result").verbose_name
        self.assertEquals(field_label, "Task result")

    def test_verbose_names(self):
        task_history = TaskHistory.objects.get(id=1)
        verbose_name = task_history._meta.verbose_name
        verbose_name_plural = task_history._meta.verbose_name_plural

        self.assertEquals(verbose_name, "History of emails sent by tasks")
        self.assertEquals(verbose_name_plural, "History of emails sent by tasks")
