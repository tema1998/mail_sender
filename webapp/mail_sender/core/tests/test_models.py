from django.test import TestCase

from core.models import *


class EmailHistory(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='username', email='email@mail.ru', password='password')
        Profile.objects.create(user=user, bio='I like going for a walk', location='Minsk')

    def setUp(self):
        pass

    def test_user_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'User')