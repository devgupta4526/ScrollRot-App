"""Serializers for User authentication, profile, search, and sharing consent."""

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, DataSharingConsent


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Registration serializer creating user and returning JWT tokens."""

    password = serializers.CharField(write_only=True, min_length=8)
    tokens = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "username", "display_name", "password", "tokens")
        read_only_fields = ("id", "tokens")

    def validate_email(self, value):
        normalized = value.strip().lower()
        if User.objects.filter(email=normalized).exists():
            raise serializers.ValidationError("An account with this email address already exists.")
        return normalized

    def validate_username(self, value):
        cleaned = value.strip()
        if len(cleaned) < 3:
            raise serializers.ValidationError("Username handle must be at least 3 characters.")
        if User.objects.filter(username__iexact=cleaned).exists():
            raise serializers.ValidationError("This username handle is already taken.")
        return cleaned

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
            display_name=validated_data.get("display_name", ""),
        )
        # Create default disabled sharing consent (privacy-first)
        DataSharingConsent.objects.get_or_create(user=user, defaults={"enabled": False})
        return user

    def get_tokens(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class UserLoginSerializer(serializers.Serializer):
    """Authenticate with normalized email and password."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email", "").strip().lower()
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "Invalid credentials."})

        if not user.check_password(password):
            raise serializers.ValidationError({"detail": "Invalid credentials."})

        if not user.is_active:
            raise serializers.ValidationError({"detail": "User account is disabled."})

        refresh = RefreshToken.for_user(user)
        return {
            "user": user,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
        }


class UserProfileSerializer(serializers.ModelSerializer):
    """Full authenticated user profile."""

    sharing_consent = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "username", "display_name", "date_joined", "sharing_consent")
        read_only_fields = ("id", "email", "username", "date_joined", "sharing_consent")

    def get_sharing_consent(self, obj):
        consent = getattr(obj, "sharing_consent", None)
        return {
            "enabled": consent.enabled if consent else False,
            "consent_version": consent.consent_version if consent else "v1",
        }


class UserPublicSearchSerializer(serializers.ModelSerializer):
    """Privacy-safe public profile for user discovery (no email exposed)."""

    class Meta:
        model = User
        fields = ("id", "username", "display_name")


class SharingConsentSerializer(serializers.Serializer):
    """Toggle aggregate battle score sharing consent."""

    enabled = serializers.BooleanField()
    consent_version = serializers.CharField(required=False, default="v1")

    def update_consent(self, user):
        enabled = self.validated_data["enabled"]
        version = self.validated_data.get("consent_version", "v1")
        consent, _ = DataSharingConsent.objects.get_or_create(user=user)
        consent.enabled = enabled
        consent.consent_version = version
        consent.save()
        return consent
