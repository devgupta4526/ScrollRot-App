from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AuthEndpointIntegrationTests(TestCase):
    """Integration tests for registration, login, refresh, logout, and profile management."""

    def setUp(self):
        self.client = Client()

    def test_register_creates_user_and_returns_tokens(self):
        payload = {
            "email": "NEW.User@example.com",
            "username": "NewScroller",
            "password": "Password123!",
            "display_name": "New Scroller",
        }
        response = self.client.post("/api/v1/auth/register/", payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEqual(data["email"], "new.user@example.com")
        self.assertIn("tokens", data)
        self.assertIn("access", data["tokens"])
        self.assertIn("refresh", data["tokens"])
        self.assertTrue(User.objects.filter(email="new.user@example.com").exists())

    def test_register_duplicate_email_rejected(self):
        User.objects.create_user(email="dup@example.com", username="User1", password="Password123!")
        payload = {
            "email": "dup@example.com",
            "username": "User2",
            "password": "Password123!",
        }
        response = self.client.post("/api/v1/auth/register/", payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success_and_token_authentication(self):
        user = User.objects.create_user(
            email="login@example.com", username="LoginUser", password="SecurePassword123!"
        )
        payload = {"email": "LOGIN@example.com", "password": "SecurePassword123!"}
        response = self.client.post("/api/v1/auth/login/", payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        access_token = data["tokens"]["access"]
        refresh_token = data["tokens"]["refresh"]

        # Call authenticated /me/ endpoint
        me_resp = self.client.get(
            "/api/v1/me/",
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(me_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(me_resp.json()["username"], "LoginUser")

        # Test refresh
        refresh_resp = self.client.post(
            "/api/v1/auth/refresh/",
            {"refresh": refresh_token},
            content_type="application/json",
        )
        self.assertEqual(refresh_resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_resp.json())
        active_refresh = refresh_resp.json().get("refresh", refresh_token)

        # Test logout blacklisting with active token
        logout_resp = self.client.post(
            "/api/v1/auth/logout/",
            {"refresh": active_refresh},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(logout_resp.status_code, status.HTTP_200_OK)


    def test_sharing_consent_toggle(self):
        user = User.objects.create_user(
            email="consent@example.com", username="ConsentUser", password="Password123!"
        )
        token = str(RefreshToken.for_user(user).access_token)

        # Initially false
        me_resp = self.client.get("/api/v1/me/", HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertFalse(me_resp.json()["sharing_consent"]["enabled"])

        # Enable consent
        update_resp = self.client.post(
            "/api/v1/me/sharing-consent/",
            {"enabled": True, "consent_version": "v1"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(update_resp.status_code, status.HTTP_200_OK)
        self.assertTrue(update_resp.json()["enabled"])

    def test_delete_account_removes_user(self):
        user = User.objects.create_user(
            email="del@example.com", username="DelUser", password="DeleteMe123!"
        )
        token = str(RefreshToken.for_user(user).access_token)

        # Wrong password fails
        fail_resp = self.client.delete(
            "/api/v1/me/",
            {"password": "wrong"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(fail_resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(User.objects.filter(email="del@example.com").exists())

        # Correct password succeeds
        del_resp = self.client.delete(
            "/api/v1/me/",
            {"password": "DeleteMe123!"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(del_resp.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(email="del@example.com").exists())
