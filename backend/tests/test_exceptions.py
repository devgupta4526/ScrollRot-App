from django.test import SimpleTestCase
from rest_framework.exceptions import ValidationError, AuthenticationFailed, PermissionDenied
from scrollrot_api.exceptions import custom_exception_handler


class ExceptionHandlerContractTests(SimpleTestCase):
    """Verify that custom_exception_handler conforms to docs/24_API_CONTRACT.md format:
    {"code": "...", "detail": "...", "field_errors": {}}
    """

    def test_validation_error_formatting(self):
        exc = ValidationError({"email": ["Enter a valid email address."]})
        response = custom_exception_handler(exc, context={})
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)
        data = response.data
        self.assertEqual(data.get("code"), "validation_error")
        self.assertIn("field_errors", data)
        self.assertIn("email", data["field_errors"])
        self.assertEqual(data["field_errors"]["email"], ["Enter a valid email address."])

    def test_authentication_failed_formatting(self):
        exc = AuthenticationFailed("Invalid or expired token.")
        response = custom_exception_handler(exc, context={})
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 401)
        data = response.data
        self.assertIn("code", data)
        self.assertEqual(data.get("detail"), "Invalid or expired token.")
        self.assertEqual(data.get("field_errors"), {})

    def test_permission_denied_formatting(self):
        exc = PermissionDenied("You do not have permission to access this resource.")
        response = custom_exception_handler(exc, context={})
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 403)
        data = response.data
        self.assertEqual(data.get("code"), "permission_denied")
        self.assertEqual(data.get("detail"), "You do not have permission to access this resource.")
        self.assertEqual(data.get("field_errors"), {})

    def test_unhandled_exception_returns_500_with_safe_message(self):
        exc = Exception("Internal database crash with credentials")
        response = custom_exception_handler(exc, context={})
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 500)
        data = response.data
        self.assertEqual(data.get("code"), "internal_error")
        self.assertEqual(data.get("detail"), "An unexpected server error occurred.")
        self.assertNotIn("Internal database crash", data.get("detail"))
