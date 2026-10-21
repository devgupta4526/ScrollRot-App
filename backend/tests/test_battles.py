from datetime import timedelta
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import DataSharingConsent
from battles.models import Battle, BattleMembership, DailyBattleScore

User = get_user_model()


class BattleIntegrationTests(TestCase):
    """Integration tests for battle creation, joining, score upserts, and leaderboards."""

    def setUp(self):
        self.client = Client()
        self.alice = User.objects.create_user(email="alice_b@example.com", username="AliceB", password="Password123!")
        self.bob = User.objects.create_user(email="bob_b@example.com", username="BobB", password="Password123!")
        self.charlie = User.objects.create_user(email="charlie_b@example.com", username="CharlieB", password="Password123!")

        self.token_alice = str(RefreshToken.for_user(self.alice).access_token)
        self.token_bob = str(RefreshToken.for_user(self.bob).access_token)
        self.token_charlie = str(RefreshToken.for_user(self.charlie).access_token)

        # Enable sharing consent for Alice and Bob
        DataSharingConsent.objects.create(user=self.alice, enabled=True)
        DataSharingConsent.objects.create(user=self.bob, enabled=True)
        # Charlie has NO consent
        DataSharingConsent.objects.create(user=self.charlie, enabled=False)

    def test_create_and_join_battle(self):
        now = timezone.now()
        payload = {
            "title": "Weekend Doomscroll Detox",
            "starts_at": now.isoformat(),
            "ends_at": (now + timedelta(days=3)).isoformat(),
            "max_participants": 5,
        }
        create_resp = self.client.post(
            "/api/v1/battles/",
            payload,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token_alice}",
        )
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        battle_data = create_resp.json()
        battle_id = battle_data["id"]
        join_code = battle_data["join_code"]

        # Bob joins via code
        join_resp = self.client.post(
            "/api/v1/battles/join/",
            {"join_code": join_code},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token_bob}",
        )
        self.assertEqual(join_resp.status_code, status.HTTP_200_OK)

        # Non-member (Charlie) cannot view battle details
        detail_resp = self.client.get(
            f"/api/v1/battles/{battle_id}/",
            HTTP_AUTHORIZATION=f"Bearer {self.token_charlie}",
        )
        self.assertEqual(detail_resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_idempotent_score_upsert_and_leaderboard(self):
        now = timezone.now()
        battle = Battle.objects.create(
            owner=self.alice,
            title="Shorts Challenge",
            starts_at=now,
            ends_at=now + timedelta(days=7),
        )
        BattleMembership.objects.create(battle=battle, user=self.alice, role=BattleMembership.ROLE_OWNER)
        BattleMembership.objects.create(battle=battle, user=self.bob, role=BattleMembership.ROLE_MEMBER)
        BattleMembership.objects.create(battle=battle, user=self.charlie, role=BattleMembership.ROLE_MEMBER)

        # Alice submits score 42
        score_url = f"/api/v1/battles/{battle.id}/scores/2026-10-20/instagram/"
        score_resp = self.client.put(
            score_url,
            {"estimated_count": 42, "timezone": "UTC"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token_alice}",
        )
        self.assertEqual(score_resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DailyBattleScore.objects.count(), 1)

        # Alice updates same score to 50 (idempotent upsert)
        update_resp = self.client.put(
            score_url,
            {"estimated_count": 50, "timezone": "UTC"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token_alice}",
        )
        self.assertEqual(update_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(DailyBattleScore.objects.count(), 1)
        self.assertEqual(DailyBattleScore.objects.first().estimated_count, 50)

        # Bob submits legitimate 0
        bob_resp = self.client.put(
            f"/api/v1/battles/{battle.id}/scores/2026-10-20/instagram/",
            {"estimated_count": 0, "timezone": "UTC"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token_bob}",
        )
        self.assertEqual(bob_resp.status_code, status.HTTP_201_CREATED)

        # Charlie (consent=False) fails to submit score
        charlie_resp = self.client.put(
            f"/api/v1/battles/{battle.id}/scores/2026-10-20/instagram/",
            {"estimated_count": 10, "timezone": "UTC"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token_charlie}",
        )
        self.assertEqual(charlie_resp.status_code, status.HTTP_400_BAD_REQUEST)

        # Check Leaderboard: Bob has 0 (winner), Alice has 50, Charlie has NO DATA (null)
        lb_resp = self.client.get(
            f"/api/v1/battles/{battle.id}/leaderboard/",
            HTTP_AUTHORIZATION=f"Bearer {self.token_alice}",
        )
        self.assertEqual(lb_resp.status_code, status.HTTP_200_OK)
        lb = lb_resp.json()["leaderboard"]
        self.assertEqual(len(lb), 3)

        bob_entry = next(e for e in lb if e["username"] == "BobB")
        alice_entry = next(e for e in lb if e["username"] == "AliceB")
        charlie_entry = next(e for e in lb if e["username"] == "CharlieB")

        self.assertTrue(bob_entry["has_data"])
        self.assertEqual(bob_entry["total_estimated_count"], 0)

        self.assertTrue(alice_entry["has_data"])
        self.assertEqual(alice_entry["total_estimated_count"], 50)

        self.assertFalse(charlie_entry["has_data"])
        self.assertIsNone(charlie_entry["total_estimated_count"])
