from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateProfileSiginalTestCase(TestCase):
    def test_create_profile_from_user_creation(self):
        user = User.objects.create_user(username="user_tester", password="1234567")
        self.assertTrue(user.profile)
