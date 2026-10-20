# 16 — Custom Django / Render backend and private social features

**Architecture decision:** No Firebase anywhere in Scrollrot. Backend: Django + Django REST Framework (DRF), PostgreSQL hosted on Render; Android remains Kotlin/XML, offline-first with Room and Retrofit/OkHttp. Prefer a modular monolith over premature microservices.

## Scope and data boundary

- Local device, not cloud, does opt-in AccessibilityService-based estimates. Backend **never** receives raw accessibility events, captions, screenshots, view trees, watched-video IDs, or private app content.
- The core tracker runs offline with no account. Email/password account creation is required only for opt-in social features; no mandatory cloud sign-in.
- Once an account signs in and explicitly enables sharing, Android may send daily aggregate counts by app/category to private challenges. If consent is withdrawn, stop transfers immediately and offer deletion of previously synced scores.
- Treat scores as **self-reported estimates**, not proof of how many reels somebody actually watched. Never reward a missing-data day as a genuine zero.

## Components

| Component | Choice | Purpose |
|---|---|---|
| API framework | Django + Django REST Framework | Versioned REST endpoints, validation and permissions |
| Database | PostgreSQL | Persistent users, friendships, groups, score aggregates |
| Authentication | Django user model + Simple JWT | Access/refresh tokens, sign-up, sign-in, logout |
| Android HTTP | Retrofit + OkHttp + kotlinx.serialization/Moshi | Typed DTOs, TLS, retry policies, auth interceptor |
| Realtime v1 | Conditional GET/polling on group screen | Avoid Redis/Channels cost and complexity initially |
| Realtime v2 | Django Channels + ASGI/WebSockets + Render Key Value | Add only when demand and paid resources justify it |
| Admin | Django Admin (staff only) | Abuse reports and user support |
| Hosting | Render web service + Render Postgres | Git-driven deployment |

## Relational database schema (Django models)

- `User` (UUID pk or Django internal ID; unique normalized email, public display handle; create a custom user model **before the first migration** if email-as-login is desired).
- `RefreshTokenSession` / blacklist with token rotation and revocation where appropriate.
- `FriendRequest` (sender, receiver, status, created_at; unique pending pair; blocked recipients cannot be invited).
- `Friendship` (canonical pair; `user_a < user_b` ordering; created_at).
- `UserBlock` (actor, target; uniqueness; both directions honored for discovery/invites).
- `Battle` (id, owner, title, privacy, starts_at, ends_at, time_zone, status, join_code_hash/expiration).
- `BattleMembership` (battle, user, role, join_state, joined_at; unique per battle/user).
- `DailyBattleScore` (battle, user, date, platform, estimated_count, updated_at; unique composite key; only submit self-owned aggregates).
- `Report` (reporter, target, category, sanitized details, status).
- `DataSharingConsent` (user, consent_version, enabled, changed_at; server audit metadata without content logs).

### Invariants and anti-abuse

- Deny by default. Check membership at query AND object-permission layer. Never rely on Android UI hiding links for authorization.
- Login endpoints throttled; friend requests invited/sent with rate limits; group join codes short-lived, hashed or sufficiently unpredictable.
- Score updates are idempotent per authenticated user, battle, date and platform. Prevent negative/out-of-range counts; enforce date interval and submitter identity. Understand clients can falsify counts.
- No API accepts `user_id` as an authority to write someone else's scores; identity always comes from the verified token.
- Paginate list endpoints; redact private data from error responses; use atomic DB transactions for membership and score upserts.
- Delete account: revoke tokens, remove friendships/invitations/memberships/scores as defined by retention and privacy policy, and ensure repeated deletion is safe. Avoid orphan personal data.

## Android boundaries

Keep the application modular:

```text
app/src/main/java/com/scrollrot/app/
  data/local/                  # Room: count evidence and aggregates stay on device
  data/remote/api/             # Retrofit endpoints/DTOs only
  data/remote/auth/            # token/session management
  data/repository/             # offline-first repositories, explicit sync
  feature/friends/             # Fragments, ViewModels, adapters
  feature/battles/
```

- `INTERNET`/`ACCESS_NETWORK_STATE` only when network features are enabled; **no** `google-services` Gradle plugin or Firebase SDK.
- Prefer HTTPS `https://<your-service>.onrender.com/api/v1/`. Keep base URL in `BuildConfig`, not string resources with credentials.
- Keep users logged out after local-first onboarding unless they choose to sign up; handle 401, offline, expired/rotated tokens, 409 conflicts and 429 backoff.
- Never store the refresh token as a plain text DataStore value. Use an Android Keystore-backed encryption strategy and threat-model device compromise.

## Implementation sequence

1. Implement server bootstrap + PostgreSQL migration + healthcheck. Deploy to Render.
2. Introduce Django auth endpoints and JWT rotation + account deletion, test auth boundaries.
3. Introduce friendship invites and moderation, test two-user isolation.
4. Introduce battles + participant authorization + opt-in daily score sync. Add 3-account integration tests.
5. Add optional WebSockets/Channels/Key Value only when REST refresh is insufficient.

Read: [`23_RENDER_DEPLOYMENT.md`](23_RENDER_DEPLOYMENT.md), [`24_API_CONTRACT.md`](24_API_CONTRACT.md), prompts `09`–`11`.
