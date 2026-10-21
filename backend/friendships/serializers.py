"""Serializers for friend requests, friendships, and user blocks."""

from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserPublicSearchSerializer
from .models import FriendRequest, Friendship, UserBlock


class FriendRequestSerializer(serializers.ModelSerializer):
    """Detail view of a friend request."""

    sender = UserPublicSearchSerializer(read_only=True)
    receiver = UserPublicSearchSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ("id", "sender", "receiver", "status", "created_at")
        read_only_fields = ("id", "sender", "receiver", "status", "created_at")


class SendFriendRequestSerializer(serializers.Serializer):
    """Validate and initiate a friend request by user ID or username."""

    target_user_id = serializers.UUIDField(required=False)
    username = serializers.CharField(required=False)

    def validate(self, attrs):
        user = self.context["request"].user
        target_id = attrs.get("target_user_id")
        username = attrs.get("username")

        if not target_id and not username:
            raise serializers.ValidationError("Either target_user_id or username is required.")

        try:
            if target_id:
                target_user = User.objects.get(id=target_id)
            else:
                target_user = User.objects.get(username__iexact=username.strip())
        except User.DoesNotExist:
            raise serializers.ValidationError("Target user not found.")

        if target_user.id == user.id:
            raise serializers.ValidationError("You cannot send a friend request to yourself.")

        # Check block isolation
        if UserBlock.is_blocked(user, target_user):
            raise serializers.ValidationError("Cannot interact with this user.")

        # Check existing friendship
        if Friendship.are_friends(user, target_user):
            raise serializers.ValidationError("You are already friends with this user.")

        # Check existing pending request in either direction
        if FriendRequest.objects.filter(
            sender=user, receiver=target_user, status=FriendRequest.STATUS_PENDING
        ).exists():
            raise serializers.ValidationError("A friend request is already pending for this user.")

        if FriendRequest.objects.filter(
            sender=target_user, receiver=user, status=FriendRequest.STATUS_PENDING
        ).exists():
            raise serializers.ValidationError(
                "This user has already sent you a friend request. Accept it from your incoming requests."
            )

        attrs["target_user"] = target_user
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        target_user = validated_data["target_user"]
        return FriendRequest.objects.create(sender=user, receiver=target_user)


class FriendshipSerializer(serializers.ModelSerializer):
    """Represents a friend connection with the other user's public profile."""

    friend = serializers.SerializerMethodField()

    class Meta:
        model = Friendship
        fields = ("id", "friend", "created_at")

    def get_friend(self, obj):
        request_user = self.context["request"].user
        other_user = obj.get_other_user(request_user)
        return UserPublicSearchSerializer(other_user).data


class UserBlockSerializer(serializers.ModelSerializer):
    """Serialize blocked user record."""

    blocked_user = UserPublicSearchSerializer(source="blocked", read_only=True)
    target_user_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = UserBlock
        fields = ("id", "blocked_user", "target_user_id", "created_at")
        read_only_fields = ("id", "blocked_user", "created_at")

    def validate_target_user_id(self, value):
        user = self.context["request"].user
        if str(value) == str(user.id):
            raise serializers.ValidationError("You cannot block yourself.")
        try:
            target = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Target user not found.")
        return value
