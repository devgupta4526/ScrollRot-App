# 24 — Scrollrot versioned REST API contract (v1)

Base path: `/api/v1/`, JSON over HTTPS. **All endpoints are planned; the starter Android ZIP does not implement this backend.** Use DRF serializers, authenticated request identity, validated ownership and pagination.

## Response conventions

- UTC ISO-8601 timestamps with offsets, and ISO local dates (`YYYY-MM-DD`) with explicit battle time zone.
- JSON body; return consistent `{"code": "...", "detail": "...", "field_errors": {}}` errors, without leaking user/account existence in sensitive flows.
- `400` invalid data, `401` no/expired access token, `403` insufficient membership, `404` unavailable/not visible, `409` conflict, `429` throttled, `5xx` retryable infrastructure errors.
- Bearer JWT access token; rotate/revoke refresh tokens. Audit mobile-safe token storage; do not send passwords in logs.

| Method | Path | Auth | Purpose |
|---|---|---|---|
| GET | `/health/` | No | Minimal service status, no secrets |
| POST | `/auth/register/` | No | Create opt-in account |
| POST | `/auth/login/` | No | Return access/refresh token pair |
| POST | `/auth/refresh/` | Refresh token | Rotate refresh + access |
| POST | `/auth/logout/` | Yes | Revoke refresh/session where supported |
| GET/PATCH | `/me/` | Yes | Read/update own public-safe profile |
| DELETE | `/me/` | Yes + reauth | Delete account and personal server data |
| GET | `/users/search/?q=...` | Yes | Rate-limited user discovery, privacy-safe |
| POST | `/friend-requests/` | Yes | Request friendship |
| GET | `/friend-requests/` | Yes | Incoming/outgoing private requests |
| POST | `/friend-requests/{id}/accept/` | Yes | Accept addressed request |
| POST | `/friend-requests/{id}/decline/` | Yes | Decline addressed request |
| GET/DELETE | `/friends/{id}/` | Yes | List/remove own friends (use list route) |
| POST | `/blocks/` | Yes | Block a user |
| GET/POST | `/battles/` | Yes | List/create authorized private battle |
| GET | `/battles/{id}/` | Member | Battle metadata and participant list |
| POST | `/battles/{id}/join/` | Yes | Accept invitation or valid join code |
| POST | `/battles/{id}/leave/` | Member | Leave battle |
| GET | `/battles/{id}/leaderboard/` | Member | Member-visible estimates, includes No data |
| PUT | `/battles/{id}/scores/{local_date}/{platform}/` | Member + opt-in | Idempotent **own** aggregate count upsert |
| POST | `/me/sharing-consent/` | Yes | Grant/revoke aggregate sharing |
| POST | `/reports/` | Yes | Report abuse |

## Score request example

```http
PUT /api/v1/battles/af13.../scores/2026-10-20/instagram/
Authorization: Bearer <access-token>
Content-Type: application/json

{"estimated_count": 27, "device_local_date": "2026-10-20", "timezone": "Asia/Kolkata"}
```

Server derives **user ID** from JWT, not client JSON. It validates group membership, consent, date range, platform allowlist, counter bounds, and idempotent concurrency. Score can change within permitted edit window due to delayed local sync; define replacement semantics. Zero is a legitimate reported 0 only if the app tracked successfully for the interval; `null` / `No data` covers missing permissions/unobserved days. The backend **cannot independently certify** watch behavior.

## Android Retrofit repository guidance

- Define a `ScrollrotApi` interface and typed DTOs, wrapped in a repository that exposes `Flow<Result<State>>` or an equivalent explicit state model.
- Use a custom OkHttp interceptor for access tokens, a synchronized refresh mechanism that prevents concurrent refresh storms, and separate network timeouts.
- Keep local Room write path independent. Upload only after account login + social data-sharing opt-in; enqueue retry with WorkManager only for aggregate sync, network/battery constraints and bounded backoff.
- On logout delete local credential data, stop sync jobs, and leave local tracking intact unless user asks to erase it.

## Test matrix (server)

1. Anonymous request denied for private endpoints.
2. User A cannot read User B private profile/requests/group or mutate B score.
3. Stale, forged, missing or revoked tokens do not grant access.
4. Private-group join without invite/code denied; leaving revokes access.
5. Two concurrent score submissions preserve latest valid state without double counting.
6. Offline retry of same upsert remains idempotent.
7. Consent withdrawn blocks sync and deletion removes server-held counts.
8. Zero vs missing-data semantics enforced; valid score bounds and dates.
9. Burst requests return `429` with client backoff.
10. All user-sensitive querysets are scoped server-side.
