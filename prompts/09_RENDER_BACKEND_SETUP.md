# 09 — Build and deploy the custom Django backend on Render

## Goal

Create a **real deployable Django REST API** and PostgreSQL-backed skeleton. Do not add Firebase. Keep Scrollrot's Android dashboard completely usable offline.

## Read first

- `AGENTS.md`, `PROJECT_STATUS.md`
- `docs/16_BACKEND_AND_SOCIAL.md`
- `docs/23_RENDER_DEPLOYMENT.md`
- `docs/24_API_CONTRACT.md`

## Implement, one vertical slice at a time

1. Inspect repo structure and build an isolated `backend/` Django project with pinned compatible requirements, `.env.example`, `.gitignore`, `build.sh`, env-driven production settings, WhiteNoise and a public `/api/v1/health/` endpoint.
2. Define/customize the user model **before** initial Django migrations as required by auth design.
3. Configure PostgreSQL from `DATABASE_URL`; tests must use reproducible isolated database settings. Do not persist production user data in SQLite on Render.
4. Add `render.yaml` for Render Web Service + PostgreSQL. Choose an appropriate plan knowingly; free plans are development only because web spin-down and free database expiration.
5. Implement a health endpoint, `/api/v1/` routes, authenticated placeholder architecture, environment guardrails, secure allowed-hosts and HTTPS defaults.
6. Run `python manage.py check`, migration/test commands, and deploy through Render **only with user-authorized connection/action**. Otherwise provide exact manual steps and don't claim it is deployed.
7. Record the actual public API URL after a successful deployment; never invent one.

## Verification

- [ ] Backend boots locally against PostgreSQL.
- [ ] Migration and Django tests pass; actual stdout recorded.
- [ ] Production config refuses insecure defaults.
- [ ] Health endpoint returns 200 locally (and on Render only if deployed).
- [ ] No secrets in source/Android APK; no Firebase SDK/config.
- [ ] `PROJECT_STATUS.md` updated with actual evidence.

Stop before implementing auth/friends. Next task: `prompts/10_AUTH_AND_FRIENDS.md`.
