from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import DataSharingConsent

User = get_user_model()


class UserModelTests(TestCase):
    """Verify custom User model and DataSharingConsent behavior per docs/16."""

    def test_create_user_successful(self):
        user = User.objects.create_user(
            email="TEST.User@Example.Com",
            username="TestUser",
            password="StrongPassword123!",
            display_name="Test Display",
        )
        self.assertEqual(user.email, "test.user@example.com")
        self.assertEqual(user.username, "TestUser")
        self.assertEqual(user.display_name, "Test Display")
        self.assertTrue(user.check_password("StrongPassword123!"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNotNone(user.id)

    def test_create_user_missing_email_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", username="User123", password="pwd")

    def test_create_user_missing_username_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="valid@example.com", username="", password="pwd")

    def test_create_superuser_successful(self):
        admin = User.objects.create_superuser(
            email="admin@example.com",
            username="admin_user",
            password="AdminPassword123!",
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active)

    def test_data_sharing_consent_default_disabled(self):
        user = User.objects.create_user(
            email="privacy@example.com",
            username="privacy_user",
            password="Password123!",
        )
        consent = DataSharingConsent.objects.create(user=user)
        self.assertFalse(consent.enabled, "Data sharing consent must default to disabled (privacy-first)")
        self.assertEqual(consent.consent_version, "v1")
