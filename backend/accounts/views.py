"""Accounts and authentication views."""

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.db import transaction
from django.db.models import Q
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserPublicSearchSerializer,
    SharingConsentSerializer,
)
from friendships.models import UserBlock


class RegisterView(generics.CreateAPIView):
    """User registration returning access + refresh JWTs."""

    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """User authentication returning access + refresh JWTs."""

    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        tokens = serializer.validated_data["tokens"]
        user_data = UserProfileSerializer(user).data
        return Response(
            {
                "user": user_data,
                "tokens": tokens,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """Revoke/blacklist the refresh token."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"code": "missing_token", "detail": "Refresh token is required.", "field_errors": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"code": "invalid_token", "detail": "Token is invalid or already expired.", "field_errors": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MeView(APIView):
    """Current user profile and account management."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        display_name = request.data.get("display_name")
        if display_name is not None:
            request.user.display_name = str(display_name).strip()[:100]
            request.user.save(update_fields=["display_name"])
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        password = request.data.get("password")
        if not password or not request.user.check_password(password):
            return Response(
                {"code": "invalid_password", "detail": "Valid password required to delete account.", "field_errors": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = request.user
        with transaction.atomic():
            user.delete()
        return Response({"detail": "Account and associated personal data successfully deleted."}, status=status.HTTP_200_OK)


class SharingConsentView(APIView):
    """Grant or revoke opt-in aggregate score sharing."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SharingConsentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        consent = serializer.update_consent(request.user)
        return Response(
            {
                "enabled": consent.enabled,
                "consent_version": consent.consent_version,
                "changed_at": consent.changed_at.isoformat(),
            },
            status=status.HTTP_200_OK,
        )


class UserSearchView(generics.ListAPIView):
    """Privacy-safe user search for sending friend requests."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    serializer_class = UserPublicSearchSerializer

    def get_queryset(self):
        query = self.request.query_params.get("q", "").strip()
        if not query or len(query) < 2:
            return User.objects.none()

        user = self.request.user
        # Exclude blocked users (in either direction) and self
        blocked_ids = set(
            UserBlock.objects.filter(blocker=user).values_list("blocked_id", flat=True)
        ).union(
            set(UserBlock.objects.filter(blocked=user).values_list("blocker_id", flat=True))
        )
        blocked_ids.add(user.id)

        return User.objects.filter(
            Q(username__icontains=query) | Q(display_name__icontains=query)
        ).exclude(id__in=blocked_ids).order_by("username")[:20]
