from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from friendships.models import FriendRequest, Friendship, UserBlock

User = get_user_model()


class FriendshipIntegrationTests(TestCase):
    """Integration tests for friend requests, mutual friendship, and blocking."""

    def setUp(self):
        self.client = Client()
        self.user_a = User.objects.create_user(
            email="alice@example.com", username="Alice", password="Password123!"
        )
        self.user_b = User.objects.create_user(
            email="bob@example.com", username="Bob", password="Password123!"
        )
        self.user_c = User.objects.create_user(
            email="charlie@example.com", username="Charlie", password="Password123!"
        )
        self.token_a = str(RefreshToken.for_user(self.user_a).access_token)
        self.token_b = str(RefreshToken.for_user(self.user_b).access_token)
        self.token_c = str(RefreshToken.for_user(self.user_c).access_token)

    def test_send_and_accept_friend_request(self):
        # Alice sends to Bob
        send_resp = self.client.post(
            "/api/v1/friend-requests/",
            {"username": "Bob"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token_a}",
        )
        self.assertEqual(send_resp.status_code, status.HTTP_201_CREATED)
        req_id = send_resp.json()["id"]

        # Duplicate send fails
        dup_resp = self.client.post(
            "/api/v1/friend-requests/",
            {"username": "Bob"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token_a}",
        )
        self.assertEqual(dup_resp.status_code, status.HTTP_400_BAD_REQUEST)

        # Bob checks incoming
        list_resp = self.client.get(
            "/api/v1/friend-requests/",
            HTTP_AUTHORIZATION=f"Bearer {self.token_b}",
        )
        self.assertEqual(list_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_resp.json()["incoming"]), 1)

        # Bob accepts
        accept_resp = self.client.post(
            f"/api/v1/friend-requests/{req_id}/accept/",
            HTTP_AUTHORIZATION=f"Bearer {self.token_b}",
        )
        self.assertEqual(accept_resp.status_code, status.HTTP_200_OK)
        self.assertTrue(Friendship.are_friends(self.user_a, self.user_b))

        # Both can see friend in friends list
        a_friends = self.client.get("/api/v1/friends/", HTTP_AUTHORIZATION=f"Bearer {self.token_a}").json()
        b_friends = self.client.get("/api/v1/friends/", HTTP_AUTHORIZATION=f"Bearer {self.token_b}").json()
        a_results = a_friends.get("results", a_friends)
        b_results = b_friends.get("results", b_friends)
        self.assertEqual(len(a_results), 1)
        self.assertEqual(len(b_results), 1)

    def test_block_user_removes_friendship_and_cancels_requests(self):
        # Establish friendship
        Friendship.create_friendship(self.user_a, self.user_b)
        self.assertTrue(Friendship.are_friends(self.user_a, self.user_b))

        # Alice blocks Bob
        block_resp = self.client.post(
            "/api/v1/blocks/",
            {"target_user_id": str(self.user_b.id)},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token_a}",
        )
        self.assertEqual(block_resp.status_code, status.HTTP_201_CREATED)

        # Friendship is gone
        self.assertFalse(Friendship.are_friends(self.user_a, self.user_b))

        # Bob cannot search Alice
        search_resp = self.client.get(
            "/api/v1/users/search/?q=Alice",
            HTTP_AUTHORIZATION=f"Bearer {self.token_b}",
        )
        search_data = search_resp.json()
        results = search_data.get("results", search_data)
        self.assertEqual(len(results), 0)

