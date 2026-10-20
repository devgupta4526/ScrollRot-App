"""Views for Scrollrot API core endpoints (health check and API root)."""

import logging
from django.db import connection
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

logger = logging.getLogger(__name__)


class HealthCheckView(APIView):
    """Health check endpoint.

    Accessible without authentication.
    Returns 200 OK when service and database are operational.
    Returns 503 Service Unavailable if database is unreachable.
    Never exposes internal credentials, connection strings, or sensitive data.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        db_status = "connected"
        is_healthy = True

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                row = cursor.fetchone()
                if not row or row[0] != 1:
                    db_status = "unresponsive"
                    is_healthy = False
        except Exception as exc:
            logger.warning("Database health check failed: %s", exc)
            db_status = "disconnected"
            is_healthy = False

        payload = {
            "status": "healthy" if is_healthy else "unhealthy",
            "database": db_status,
            "timestamp": timezone.now().isoformat(),
            "version": "1.0.0",
        }

        http_status = status.HTTP_200_OK if is_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response(payload, status=http_status)


class APIRootView(APIView):
    """API v1 root providing discovery and documentation pointers."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "name": "Scrollrot REST API",
                "version": "v1",
                "endpoints": {
                    "health": "/api/v1/health/",
                    "auth_register": "/api/v1/auth/register/ [Milestone 10]",
                    "auth_login": "/api/v1/auth/login/ [Milestone 10]",
                    "auth_refresh": "/api/v1/auth/refresh/ [Milestone 10]",
                    "friend_requests": "/api/v1/friend-requests/ [Milestone 10]",
                    "friends": "/api/v1/friends/ [Milestone 10]",
                    "battles": "/api/v1/battles/ [Milestone 11]",
                },
            },
            status=status.HTTP_200_OK,
        )
