# Scrollrot — Render migration handoff

**Decision:** Remove Firebase entirely. Build a custom Python Django REST API with PostgreSQL hosted on Render. This document supersedes any old Firebase references in prior external copies of the Scrollrot starter.

## First three AI prompts (separate sessions)

1. After the offline Android app runs, execute [`prompts/09_RENDER_BACKEND_SETUP.md`](prompts/09_RENDER_BACKEND_SETUP.md) to scaffold Django/DRF/PostgreSQL and a real health endpoint.
2. Test/prepare Render deployment per [`docs/23_RENDER_DEPLOYMENT.md`](docs/23_RENDER_DEPLOYMENT.md); only claim cloud deployment after you actually run/verify it.
3. Execute [`prompts/10_AUTH_AND_FRIENDS.md`](prompts/10_AUTH_AND_FRIENDS.md), then [`prompts/11_GROUP_BATTLES.md`](prompts/11_GROUP_BATTLES.md).

## Non-negotiables

- Android native: Kotlin + XML Views, offline-first Room and DataStore.
- Backend: Django REST Framework + PostgreSQL + JWT, with Retrofit/OkHttp on Android.
- No Firebase SDK, Firestore, Cloud Functions, Firebase Auth or Firestore security rules.
- Optional v1 group live updates are simple refresh/polling; Django Channels/WebSockets + Key Value may be added later.
- No raw accessibility data to cloud, only opt-in aggregate daily estimates.
- Free Render Postgres expires after 30 days; production app requires durable paid storage, backups and operations plan.

**Start by reading** [`MASTER_PROMPT.md`](MASTER_PROMPT.md), [`AGENTS.md`](AGENTS.md) and [`prompts/README.md`](prompts/README.md).
