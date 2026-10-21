"""Views for Friend Requests, Friendships, and User Blocking."""

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from accounts.models import User
from .models import FriendRequest, Friendship, UserBlock
from .serializers import (
    FriendRequestSerializer,
    SendFriendRequestSerializer,
    FriendshipSerializer,
    UserBlockSerializer,
)


class FriendRequestListCreateView(APIView):
    """List incoming/outgoing pending friend requests, or send a new request."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        incoming = FriendRequest.objects.filter(
            receiver=request.user, status=FriendRequest.STATUS_PENDING
        )
        outgoing = FriendRequest.objects.filter(
            sender=request.user, status=FriendRequest.STATUS_PENDING
        )

        return Response(
            {
                "incoming": FriendRequestSerializer(incoming, many=True).data,
                "outgoing": FriendRequestSerializer(outgoing, many=True).data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = SendFriendRequestSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        friend_request = serializer.save()
        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)


class AcceptFriendRequestView(APIView):
    """Accept an addressed friend request and establish bidirectional friendship."""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(
                id=pk, receiver=request.user, status=FriendRequest.STATUS_PENDING
            )
        except FriendRequest.DoesNotExist:
            return Response(
                {"code": "not_found", "detail": "Pending friend request not found.", "field_errors": {}},
                status=status.HTTP_404_NOT_FOUND,
            )

        with transaction.atomic():
            friend_request.status = FriendRequest.STATUS_ACCEPTED
            friend_request.save()
            friendship = Friendship.create_friendship(friend_request.sender, friend_request.receiver)

        return Response(
            {
                "detail": "Friend request accepted.",
                "friendship": FriendshipSerializer(friendship, context={"request": request}).data,
            },
            status=status.HTTP_200_OK,
        )


class DeclineFriendRequestView(APIView):
    """Decline an addressed pending friend request."""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(
                id=pk, receiver=request.user, status=FriendRequest.STATUS_PENDING
            )
        except FriendRequest.DoesNotExist:
            return Response(
                {"code": "not_found", "detail": "Pending friend request not found.", "field_errors": {}},
                status=status.HTTP_404_NOT_FOUND,
            )

        friend_request.status = FriendRequest.STATUS_DECLINED
        friend_request.save()
        return Response({"detail": "Friend request declined."}, status=status.HTTP_200_OK)


class FriendsListView(generics.ListAPIView):
    """List authenticated user's current friends."""

    permission_classes = [IsAuthenticated]
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(Q(user_a=user) | Q(user_b=user)).order_by("-created_at")


class RemoveFriendView(APIView):
    """Remove an established friend connection."""

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        friendship = get_object_or_404(
            Friendship.objects.filter(Q(user_a=request.user) | Q(user_b=request.user)),
            id=pk,
        )
        friendship.delete()
        return Response({"detail": "Friend removed."}, status=status.HTTP_200_OK)


class BlockListCreateView(APIView):
    """List blocked users or block a user."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        blocks = UserBlock.objects.filter(blocker=request.user)
        return Response(UserBlockSerializer(blocks, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserBlockSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        target_id = serializer.validated_data["target_user_id"]
        target_user = User.objects.get(id=target_id)

        with transaction.atomic():
            # Create block
            block, _ = UserBlock.objects.get_or_create(blocker=request.user, blocked=target_user)
            # Remove any active friendship
            u1, u2 = Friendship.get_canonical_pair(request.user, target_user)
            Friendship.objects.filter(user_a=u1, user_b=u2).delete()
            # Cancel any pending friend requests in either direction
            FriendRequest.objects.filter(
                (Q(sender=request.user, receiver=target_user) | Q(sender=target_user, receiver=request.user)),
                status=FriendRequest.STATUS_PENDING,
            ).update(status=FriendRequest.STATUS_DECLINED)

        return Response(UserBlockSerializer(block).data, status=status.HTTP_201_CREATED)


class UnblockUserView(APIView):
    """Unblock a previously blocked user."""

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        block = get_object_or_404(UserBlock, id=pk, blocker=request.user)
        block.delete()
        return Response({"detail": "User unblocked."}, status=status.HTTP_200_OK)
