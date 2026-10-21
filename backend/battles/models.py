"""Group Battles, Memberships, and Daily Score Aggregates Models.

Implements private challenge rooms per docs/16_BACKEND_AND_SOCIAL.md and docs/24_API_CONTRACT.md.
"""

import uuid
import secrets
import string
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


def generate_join_code():
    """Generate a random 8-character uppercase alphanumeric join code."""
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(8))


class Battle(models.Model):
    """Private group battle for comparing daily aggregate short-video scroll estimates."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_battles",
    )
    title = models.CharField(max_length=100)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    time_zone = models.CharField(max_length=50, default="UTC")
    join_code = models.CharField(
        max_length=12,
        unique=True,
        default=generate_join_code,
        db_index=True,
    )
    max_participants = models.PositiveSmallIntegerField(default=8)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Battle"
        verbose_name_plural = "Battles"
        ordering = ["-created_at"]

    def clean(self):
        if self.starts_at and self.ends_at and self.starts_at >= self.ends_at:
            raise ValidationError("Battle end time must be after start time.")
        if self.max_participants < 2 or self.max_participants > 16:
            raise ValidationError("Participant count must be between 2 and 16.")

    def is_active(self):
        now = timezone.now()
        return self.starts_at <= now <= self.ends_at

    def __str__(self):
        return f"{self.title} (Code: {self.join_code})"


class BattleMembership(models.Model):
    """Membership record linking a User to a Battle."""

    ROLE_OWNER = "OWNER"
    ROLE_MEMBER = "MEMBER"
    ROLE_CHOICES = [(ROLE_OWNER, "Owner"), (ROLE_MEMBER, "Member")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    battle = models.ForeignKey(
        Battle,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="battle_memberships",
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Battle Membership"
        verbose_name_plural = "Battle Memberships"
        ordering = ["joined_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["battle", "user"],
                name="unique_battle_membership",
            )
        ]

    def __str__(self):
        return f"{self.user.username} in {self.battle.title} ({self.role})"


class DailyBattleScore(models.Model):
    """Idempotent daily self-reported aggregate count for a specific platform and date.

    Contains ONLY daily aggregate estimates. Never raw accessibility events or video IDs.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    battle = models.ForeignKey(
        Battle,
        on_delete=models.CASCADE,
        related_name="scores",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="battle_scores",
    )
    local_date = models.DateField(db_index=True)
    platform = models.CharField(max_length=50, db_index=True)
    estimated_count = models.PositiveIntegerField()
    device_timezone = models.CharField(max_length=50, blank=True, default="UTC")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Daily Battle Score"
        verbose_name_plural = "Daily Battle Scores"
        ordering = ["-local_date", "user"]
        constraints = [
            models.UniqueConstraint(
                fields=["battle", "user", "local_date", "platform"],
                name="unique_battle_daily_score_upsert",
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.platform} on {self.local_date}: {self.estimated_count}"
