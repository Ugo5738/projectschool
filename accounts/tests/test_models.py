from accounts.models import User
from rest_framework.test import APITestCase


class TestModel(APITestCase):
    def test_creates_user(self):
        user = User.objects.create_user(username="test", email="test@test.com", password="testing")
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, "test@test.com")

    def test_raises_error_when_no_username_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username="", email="test@test.com", password="testing")
    
    def test_raises_error_with_message_when_no_username_is_supplied(self):
        with self.assertRaisesMessage(ValueError, "Username field is required"):
            user = User.objects.create_user(username="", email="test@test.com", password="testing")

    def test_raises_error_when_no_email_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username="test", email="", password="testing")
    
    def test_raises_error_with_message_when_no_email_is_supplied(self):
        with self.assertRaisesMessage(ValueError, "Email field is required"):
            user = User.objects.create_user(username="test", email="", password="testing")

    def test_creates_super_user(self):
        user = User.objects.create_superuser(username="test", email="test@test.com", password="testing")
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email, "test@test.com")

    def test_creates_super_user_with_super_user_status(self):
        with self.assertRaisesMessage(ValueError, "Superuser must have is_staff=True."):
            user = User.objects.create_superuser(username="test", email="test@test.com", password="testing", is_staff=False)

    def test_creates_super_user_with_super_user_status(self):
        with self.assertRaisesMessage(ValueError, "Superuser must have is_superuser=True."):
            user = User.objects.create_superuser(username="test", email="test@test.com", password="testing", is_superuser=False)
