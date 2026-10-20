# 10 — Authentication, privacy-safe friend requests and Android API client

## Goal

Use **Django REST Framework + PostgreSQL + JWT** instead of Firebase Auth/Firestore. Implement email/password or similarly consented opt-in account flow, friendships and secure Kotlin Retrofit integration.

Read `docs/16_BACKEND_AND_SOCIAL.md`, `docs/24_API_CONTRACT.md`, `docs/13_PRIVACY_AND_SECURITY.md`, `docs/18_TEST_STRATEGY.md` first.

1. Implement registration/login/refresh/logout, short-lived JWT access and rotated/revoked refresh tokens, account deletion, sensible throttling and test fixtures for at least two users.
2. Add Django models/serializers/querysets for friend requests, friendship, block/report; validate sender/receiver, object-level authorization and privacy-safe user search.
3. Implement Android Retrofit/OkHttp, auth manager, token persistence using a Keystore-backed approach, login/register UI in XML, server error/offline states and user-controlled social sync consent.
4. Ensure anonymous users retain all local tracker features; no cloud request before signup/opt-in for social.
5. Unit/integration tests: cross-user read/write isolation, revoked token rejection, duplicate friend request suppression, invite throttling, delete-account cascading behavior.
6. Record commands actually run, Test PASS/FAIL/NOT RUN, and update status. No mock success screen.

Acceptance: [ ] two-account integration tests [ ] denial and privacy tests [ ] token revocation [ ] Android offline UI [ ] user delete path. Stop before group battles.
