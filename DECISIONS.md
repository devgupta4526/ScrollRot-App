# Architecture decision records (ADRs)

Append new decisions as `ADR-00X`, with date, choice, alternatives, consequences and reversal conditions. Do not rewrite history.

## ADR-001 — Kotlin/XML Views rather than Compose
- **Date:** 2026-10-20
- **Decision:** use Kotlin, Fragments, XML, ViewBinding, MotionLayout and Canvas/Lottie for native Android UI.
- **Why:** explicit product requirement, animation quality achievable with native Views.
- **Consequence:** agents must not migrate UI stacks without owner approval.

## ADR-002 — Local-first and optional backend
- **Decision:** Room + DataStore hold private counts/goals; no account required for MVP.
- **Why:** privacy, offline reliability and reduced integration risk.
- **Consequence:** friends and purchases deferred; sync must be opt-in with retention policies.

## ADR-003 — Estimates, not exact guarantees
- **Decision:** platform-specific detectors may report estimated accepted transitions with confidence and support status.
- **Why:** third-party UIs and accessibility events do not expose a universal verified reel-view API.
- **Consequence:** no claims of exact 1:1 counting or scientifically measured mental impact.

## ADR-004 — A permission is never a prerequisite for viewing local UI
- **Decision:** deny, revoke, pause and unsupported states remain supported.
- **Why:** user control and Play requirements.
- **Consequence:** live counting gracefully pauses or becomes unavailable.

## ADR-005 — Strict blocker deferred
- **Decision:** implement gentle reminders and opt-in focus interventions before restrictive mechanisms.
- **Why:** platform limits, usability and policy risk; do not assert impossible-to-unlock behavior.

## ADR-006 — Django Backend Skeleton, Custom User Model, and Environment Guardrails
- **Date:** 2026-10-20
- **Decision:** Scaffold Django REST Framework backend with custom `accounts.User` (UUID primary key, normalized email as `USERNAME_FIELD`, public handle) before any database migration. Enforce PostgreSQL via `dj-database-url` in production (`DEBUG=False`) with strict refusal of SQLite on Render. Standardize API error formatting to `{"code": "...", "detail": "...", "field_errors": {}}`.
- **Why:** Adheres to `docs/16_BACKEND_AND_SOCIAL.md` and `docs/24_API_CONTRACT.md`. Defining the user model prior to the first migration prevents irreversible Django auth migration collisions.
- **Consequence:** All future authentication (Milestone 10) and battle features (Milestone 11) inherit the UUID user model and DRF exception contract. SQLite is strictly disallowed in production configurations.

