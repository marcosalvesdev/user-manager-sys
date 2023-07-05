from django.test import TestCase
from manager.models import CustomUserModel


class CreateProfileSiginalTestCase(TestCase):
    def test_create_profile_from_user_creation(self):
        user = CustomUserModel.objects.create_user(
            username="user_tester", password="1234567"
        )
        self.assertTrue(user.profile)
