"""Scrollrot Accounts Models.

Implements custom User model with UUID primary key, unique normalized email,
and public display handle before the first migration per docs/16_BACKEND_AND_SOCIAL.md.
"""

import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom user manager supporting email-as-username and unique display handles."""

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("An email address is required.")
        if not username:
            raise ValueError("A username handle is required.")

        email = self.normalize_email(email).lower()
        username = username.strip()

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(email=email, username=username, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model for Scrollrot.

    Uses UUID primary key, lowercase normalized email for authentication,
    and a public display handle.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name="Email address",
        max_length=255,
        unique=True,
        db_index=True,
    )
    username = models.CharField(
        verbose_name="Display handle",
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Public handle for friend requests and battles (e.g. alex_scrolls)",
    )
    display_name = models.CharField(
        verbose_name="Display name",
        max_length=100,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user account is active.",
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into Django admin.",
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]

    def __str__(self):
        return f"@{self.username} ({self.email})"

    def clean(self):
        super().clean()
        if self.email:
            self.email = self.email.strip().lower()


class DataSharingConsent(models.Model):
    """Audit record for user consent to share aggregate battle scores.

    Local device tracks offline; backend only receives opt-in aggregates when consent is granted.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="sharing_consent",
    )
    consent_version = models.CharField(max_length=20, default="v1")
    enabled = models.BooleanField(default=False)
    changed_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Data Sharing Consent"
        verbose_name_plural = "Data Sharing Consents"

    def __str__(self):
        state = "Enabled" if self.enabled else "Disabled"
        return f"{self.user.username} consent: {state} ({self.consent_version})"
