from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='kamal', password='pass123')
        self.assertTrue(user.is_authenticated)
        self.assertFalse(user.is_staff)
