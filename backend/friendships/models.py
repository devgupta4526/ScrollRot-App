"""Friendships, Friend Requests, and User Blocking Models.

Implements relational social graph per docs/16_BACKEND_AND_SOCIAL.md:
- Canonical ordering on Friendship (user_a.id < user_b.id)
- Distinct FriendRequest status lifecycle
- Mutual UserBlock isolation
"""

import uuid
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class FriendRequest(models.Model):
    """Pending, accepted, or declined friend request."""

    STATUS_PENDING = "PENDING"
    STATUS_ACCEPTED = "ACCEPTED"
    STATUS_DECLINED = "DECLINED"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_DECLINED, "Declined"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_friend_requests",
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_friend_requests",
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Friend Request"
        verbose_name_plural = "Friend Requests"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "receiver"],
                condition=models.Q(status="PENDING"),
                name="unique_pending_friend_request",
            )
        ]

    def clean(self):
        if self.sender_id == self.receiver_id:
            raise ValidationError("Users cannot send friend requests to themselves.")

    def __str__(self):
        return f"Request from {self.sender.username} to {self.receiver.username} ({self.status})"


class Friendship(models.Model):
    """Canonical bidirectional friendship pair (user_a.id < user_b.id)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_a = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendships_as_a",
    )
    user_b = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendships_as_b",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Friendship"
        verbose_name_plural = "Friendships"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user_a", "user_b"],
                name="unique_canonical_friendship",
            )
        ]

    @classmethod
    def get_canonical_pair(cls, u1, u2):
        u1_id = str(u1.id if hasattr(u1, "id") else u1)
        u2_id = str(u2.id if hasattr(u2, "id") else u2)
        if u1_id == u2_id:
            raise ValidationError("Cannot create friendship with oneself.")
        return (u1, u2) if u1_id < u2_id else (u2, u1)

    @classmethod
    def are_friends(cls, u1, u2):
        first, second = cls.get_canonical_pair(u1, u2)
        return cls.objects.filter(user_a=first, user_b=second).exists()

    @classmethod
    def create_friendship(cls, u1, u2):
        first, second = cls.get_canonical_pair(u1, u2)
        friendship, _ = cls.objects.get_or_create(user_a=first, user_b=second)
        return friendship

    @classmethod
    def get_friends_for_user(cls, user):
        from accounts.models import User
        friends_a = cls.objects.filter(user_b=user).values_list("user_a", flat=True)
        friends_b = cls.objects.filter(user_a=user).values_list("user_b", flat=True)
        friend_ids = set(friends_a).union(set(friends_b))
        return User.objects.filter(id__in=friend_ids)

    def get_other_user(self, user):
        return self.user_b if self.user_a_id == user.id else self.user_a

    def __str__(self):
        return f"Friendship: {self.user_a.username} <-> {self.user_b.username}"


class UserBlock(models.Model):
    """Directed block record between users.

    Both directions are honored for user discovery and invitations.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blocker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocked_users",
    )
    blocked = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocked_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Block"
        verbose_name_plural = "User Blocks"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["blocker", "blocked"],
                name="unique_user_block",
            )
        ]

    @classmethod
    def is_blocked(cls, u1, u2):
        """Returns True if either user has blocked the other."""
        return cls.objects.filter(
            models.Q(blocker=u1, blocked=u2) | models.Q(blocker=u2, blocked=u1)
        ).exists()

    def __str__(self):
        return f"{self.blocker.username} blocked {self.blocked.username}"
