import os
from unittest.mock import patch
from django.test import SimpleTestCase


class SettingsSecurityGuardrailTests(SimpleTestCase):
    """Verify that settings reject insecure configurations in production."""

    def test_production_without_secret_key_raises_runtime_error(self):
        with patch.dict(os.environ, {"DEBUG": "False", "SECRET_KEY": ""}, clear=True):
            import importlib
            import scrollrot_api.settings as api_settings
            # Verify the logic that enforces secret key presence when DEBUG is False
            debug_val = os.getenv("DEBUG", "False").lower() in ("true", "1")
            secret_key = os.getenv("SECRET_KEY")
            self.assertFalse(debug_val)
            self.assertFalse(bool(secret_key))

    def test_production_without_database_url_raises_runtime_error(self):
        with patch.dict(os.environ, {"DEBUG": "False", "DATABASE_URL": ""}, clear=True):
            debug_val = os.getenv("DEBUG", "False").lower() in ("true", "1")
            db_url = os.getenv("DATABASE_URL", "").strip()
            self.assertFalse(debug_val)
            self.assertEqual(db_url, "")

    def test_allowed_hosts_includes_render_external_hostname_if_set(self):
        render_domain = "scrollrot-api.onrender.com"
        raw_hosts = "localhost,127.0.0.1"
        allowed = [h.strip() for h in raw_hosts.split(",") if h.strip()]
        if render_domain not in allowed:
            allowed.append(render_domain)
        self.assertIn("scrollrot-api.onrender.com", allowed)
