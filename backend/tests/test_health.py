from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status


class HealthEndpointTests(TestCase):
    """Verify health endpoint behavior according to docs/24_API_CONTRACT.md."""

    def setUp(self):
        self.client = Client()

    def test_health_endpoint_returns_200_when_healthy(self):
        response = self.client.get("/api/v1/health/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get("status"), "healthy")
        self.assertEqual(data.get("database"), "connected")
        self.assertEqual(data.get("version"), "1.0.0")
        self.assertIn("timestamp", data)
        # Ensure no secret or internal path is leaked
        self.assertNotIn("password", str(data).lower())
        self.assertNotIn("secret", str(data).lower())

    def test_top_level_health_alias_returns_200(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get("status"), "healthy")

    def test_api_root_endpoint_returns_200(self):
        response = self.client.get("/api/v1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get("version"), "v1")
        self.assertIn("endpoints", data)

    @patch("django.db.connection.cursor")
    def test_health_endpoint_returns_503_when_database_fails(self, mock_cursor):
        mock_cursor.side_effect = Exception("Simulated DB connection failure")
        response = self.client.get("/api/v1/health/")
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        data = response.json()
        self.assertEqual(data.get("status"), "unhealthy")
        self.assertEqual(data.get("database"), "disconnected")
        # Ensure raw DB exception detail is never exposed in the response
        self.assertNotIn("Simulated DB connection failure", str(data))
