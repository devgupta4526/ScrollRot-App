# 11 — Private group battles with PostgreSQL and Django API

## Goal

Implement opt-in 1v1 and group battles (2–8), consented aggregate score sync, and a multi-friend leaderboard. **No Firebase.**

Read `docs/16_BACKEND_AND_SOCIAL.md`, `docs/24_API_CONTRACT.md`, `docs/14_INSIGHTS_AND_GOALS.md`, `docs/18_TEST_STRATEGY.md`.

1. Implement `Battle`, `BattleMembership`, `DailyBattleScore` tables; UTC interval plus explicit time-zone behavior, safe join codes and member-limited querysets.
2. Add authenticated CRUD/invite/accept/leave/report endpoints and a member-only leaderboard; validate user from JWT, never trust a request body `user_id`.
3. Store and transmit **only** aggregate daily estimated counts after affirmative cloud sharing consent; per-video data remains local. No-data days are not ranked as zero.
4. Implement idempotent score upserts, date and platform bounds, rate limiting, 409 conflicts as appropriate and atomic writes; clients can falsify counts, so avoid anti-cheat claims.
5. Create Kotlin/XML battle screens and Retrofit repository, including denied-access, missing-network, no-data, and revoked-permission states.
6. Poll leaderboard only while battle screen is visible (e.g., refresh/manual or modest 20–60s) for MVP; no always-on sockets. Optionally implement Django Channels/WebSockets **as a separately tested later subphase** with Render Key Value and reconnect logic.
7. Test three accounts: member visibility, non-member 403/404, wrong-user score edits, leave flow, idempotent sync, consent off, offline reconciliation.

Acceptance: [ ] group 3+ shown in one scoreboard [ ] negative auth/privacy tests [ ] no false zero winners [ ] missing-data UX [ ] no content uploads. Stop before billing/QA.
