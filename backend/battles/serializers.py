"""Serializers for Battle rooms, memberships, scores, and leaderboards."""

from rest_framework import serializers
from django.utils import timezone
from accounts.serializers import UserPublicSearchSerializer
from accounts.models import DataSharingConsent
from .models import Battle, BattleMembership, DailyBattleScore


class BattleMemberSerializer(serializers.ModelSerializer):
    user = UserPublicSearchSerializer(read_only=True)

    class Meta:
        model = BattleMembership
        fields = ("user", "role", "joined_at")


class BattleSerializer(serializers.ModelSerializer):
    owner = UserPublicSearchSerializer(read_only=True)
    members_count = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Battle
        fields = (
            "id",
            "title",
            "owner",
            "starts_at",
            "ends_at",
            "time_zone",
            "join_code",
            "max_participants",
            "members_count",
            "is_active",
            "created_at",
        )
        read_only_fields = ("id", "owner", "join_code", "created_at")

    def get_members_count(self, obj):
        return obj.memberships.count()

    def get_is_active(self, obj):
        return obj.is_active()

    def validate(self, attrs):
        starts_at = attrs.get("starts_at")
        ends_at = attrs.get("ends_at")
        if starts_at and ends_at and starts_at >= ends_at:
            raise serializers.ValidationError("Battle ends_at must be strictly after starts_at.")
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["owner"] = user
        battle = Battle.objects.create(**validated_data)
        BattleMembership.objects.create(battle=battle, user=user, role=BattleMembership.ROLE_OWNER)
        return battle


class BattleDetailSerializer(BattleSerializer):
    members = BattleMemberSerializer(source="memberships", many=True, read_only=True)

    class Meta(BattleSerializer.Meta):
        fields = BattleSerializer.Meta.fields + ("members",)


class BattleJoinSerializer(serializers.Serializer):
    join_code = serializers.CharField(max_length=12)

    def validate_join_code(self, value):
        code = value.strip().upper()
        try:
            battle = Battle.objects.get(join_code=code)
        except Battle.DoesNotExist:
            raise serializers.ValidationError("Invalid battle join code.")

        user = self.context["request"].user
        if BattleMembership.objects.filter(battle=battle, user=user).exists():
            raise serializers.ValidationError("You are already a member of this battle.")

        if battle.memberships.count() >= battle.max_participants:
            raise serializers.ValidationError("This battle has reached maximum participant capacity.")

        self.battle = battle
        return code


class DailyScoreUpsertSerializer(serializers.Serializer):
    """Validate score payload for idempotent upsert per docs/24_API_CONTRACT.md."""

    estimated_count = serializers.IntegerField(min_value=0, max_value=100000)
    device_local_date = serializers.DateField(required=False)
    timezone = serializers.CharField(required=False, default="UTC")

    def validate(self, attrs):
        user = self.context["request"].user
        # Verify user has granted aggregate sharing consent
        consent = getattr(user, "sharing_consent", None)
        if not consent or not consent.enabled:
            raise serializers.ValidationError(
                {"detail": "Data sharing consent must be enabled before syncing scores.", "code": "consent_required"}
            )
        return attrs
