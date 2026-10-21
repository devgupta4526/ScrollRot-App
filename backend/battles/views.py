"""Views for Battle management, joining, score upserts, and leaderboards."""

from datetime import datetime
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from .models import Battle, BattleMembership, DailyBattleScore
from .serializers import (
    BattleSerializer,
    BattleDetailSerializer,
    BattleJoinSerializer,
    DailyScoreUpsertSerializer,
)


class BattleListCreateView(APIView):
    """List joined battles or create a new battle room."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        battles = Battle.objects.filter(memberships__user=user).distinct().order_by("-created_at")
        serializer = BattleSerializer(battles, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BattleSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        battle = serializer.save()
        return Response(
            BattleDetailSerializer(battle, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class BattleDetailView(APIView):
    """Retrieve battle details and participant list. Member-only access."""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        battle = get_object_or_404(Battle, id=pk)
        if not battle.memberships.filter(user=request.user).exists():
            return Response(
                {"code": "permission_denied", "detail": "You are not a member of this battle.", "field_errors": {}},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = BattleDetailSerializer(battle, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BattleJoinView(APIView):
    """Join a battle using its unique join code."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BattleJoinSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        battle = serializer.battle

        with transaction.atomic():
            membership = BattleMembership.objects.create(
                battle=battle, user=request.user, role=BattleMembership.ROLE_MEMBER
            )

        return Response(
            {
                "detail": "Successfully joined battle.",
                "battle": BattleDetailSerializer(battle, context={"request": request}).data,
            },
            status=status.HTTP_200_OK,
        )


class BattleLeaveView(APIView):
    """Leave a battle room."""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        battle = get_object_or_404(Battle, id=pk)
        membership = battle.memberships.filter(user=request.user).first()
        if not membership:
            return Response(
                {"code": "not_member", "detail": "You are not a member of this battle.", "field_errors": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            membership.delete()
            # If owner leaves, assign oldest member as owner or delete battle if empty
            if membership.role == BattleMembership.ROLE_OWNER:
                next_member = battle.memberships.first()
                if next_member:
                    next_member.role = BattleMembership.ROLE_OWNER
                    next_member.save(update_fields=["role"])
                    battle.owner = next_member.user
                    battle.save(update_fields=["owner"])
                else:
                    battle.delete()

        return Response({"detail": "Successfully left battle."}, status=status.HTTP_200_OK)


class BattleLeaderboardView(APIView):
    """Aggregated leaderboard for battle participants.

    Differentiates between legitimate reported 0 and missing data days.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        battle = get_object_or_404(Battle, id=pk)
        if not battle.memberships.filter(user=request.user).exists():
            return Response(
                {"code": "permission_denied", "detail": "You must be a member to view the leaderboard.", "field_errors": {}},
                status=status.HTTP_403_FORBIDDEN,
            )

        members = battle.memberships.select_related("user").all()
        leaderboard = []

        for m in members:
            scores_qs = DailyBattleScore.objects.filter(battle=battle, user=m.user)
            has_data = scores_qs.exists()
            total = scores_qs.aggregate(total=Sum("estimated_count"))["total"] if has_data else None

            leaderboard.append(
                {
                    "user_id": str(m.user.id),
                    "username": m.user.username,
                    "display_name": m.user.display_name or m.user.username,
                    "role": m.role,
                    "has_data": has_data,
                    "total_estimated_count": total,
                }
            )

        # Sort: members with data by lowest count (least scroll rot wins!), then no-data members at end
        leaderboard.sort(
            key=lambda x: (
                0 if x["has_data"] else 1,
                x["total_estimated_count"] if x["has_data"] else 999999999,
            )
        )

        return Response(
            {
                "battle_id": str(battle.id),
                "title": battle.title,
                "is_active": battle.is_active(),
                "leaderboard": leaderboard,
            },
            status=status.HTTP_200_OK,
        )


class ScoreUpsertView(APIView):
    """Idempotently upsert own daily aggregate score per platform and date.

    Identity is derived strictly from request.user (verified JWT token).
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, pk, local_date, platform):
        battle = get_object_or_404(Battle, id=pk)
        if not battle.memberships.filter(user=request.user).exists():
            return Response(
                {"code": "permission_denied", "detail": "You are not a member of this battle.", "field_errors": {}},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Validate date format YYYY-MM-DD
        try:
            parsed_date = datetime.strptime(local_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"code": "invalid_date", "detail": "Date must be formatted as YYYY-MM-DD.", "field_errors": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = DailyScoreUpsertSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        estimated_count = serializer.validated_data["estimated_count"]
        device_timezone = serializer.validated_data.get("timezone", "UTC")

        with transaction.atomic():
            score, created = DailyBattleScore.objects.update_or_create(
                battle=battle,
                user=request.user,
                local_date=parsed_date,
                platform=platform.lower().strip(),
                defaults={
                    "estimated_count": estimated_count,
                    "device_timezone": device_timezone,
                },
            )

        return Response(
            {
                "status": "created" if created else "updated",
                "battle_id": str(battle.id),
                "local_date": str(score.local_date),
                "platform": score.platform,
                "estimated_count": score.estimated_count,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )
