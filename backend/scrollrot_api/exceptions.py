"""Custom exception handler for Scrollrot REST API.

Enforces docs/24_API_CONTRACT.md response format:
{"code": "...", "detail": "...", "field_errors": {}}
"""

import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Transform DRF and unhandled exceptions into the standard API error contract."""
    response = exception_handler(exc, context)

    if response is not None:
        data = response.data
        code = getattr(exc, "default_code", "error")
        detail = "An error occurred."
        field_errors = {}

        if isinstance(data, dict):
            if "detail" in data:
                detail = str(data["detail"])
                if hasattr(data["detail"], "code"):
                    code = str(data["detail"].code)
            else:
                detail = "Request validation failed."
                code = "validation_error"
                field_errors = {
                    key: val if isinstance(val, list) else [str(val)]
                    for key, val in data.items()
                }
        elif isinstance(data, list):
            detail = "; ".join(str(d) for d in data)
            code = "validation_error"
        else:
            detail = str(data)

        response.data = {
            "code": str(code),
            "detail": detail,
            "field_errors": field_errors,
        }
        return response

    # Unhandled server exception
    logger.exception("Unhandled server exception: %s", exc)
    return Response(
        {
            "code": "internal_error",
            "detail": "An unexpected server error occurred.",
            "field_errors": {},
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
