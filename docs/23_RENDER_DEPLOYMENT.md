# 23 — Render deployment (Django REST API + PostgreSQL)

## Render services and constraints

- One Python Django **Web Service**, one **PostgreSQL** database. Use the same region, internal DATABASE_URL, TLS public URL.
- Free web services are for experiments: they can spin down after **15 minutes** of no inbound traffic, with roughly **one-minute cold starts**.
- Free Render PostgreSQL expires after **30 days**, has **no backups** and is **not appropriate for permanent user data or production**. Plan paid Postgres and web hosting before beta with real users.
- Local service files are ephemeral. Never keep uploaded avatars, SQLite, database dumps, screenshots or secrets on the service filesystem. Store state in PostgreSQL, and optional future media in object storage with appropriate privacy controls.
- WebSockets are available on Render but can disconnect during deploys/restarts; add reconnect/backoff. If scaling Django Channels to multiple workers, use supported shared layer like Render Key Value (Redis/Valkey-compatible); free Key Value is **not persistent**.

Current authoritative documentation: https://render.com/docs/deploy-django ; https://render.com/docs/free ; https://render.com/docs/websocket ; https://render.com/docs/key-value

## Suggested monorepo

```text
Scrollrot/
  app/                      # Existing Kotlin/XML Android app
  backend/
    manage.py
    requirements.txt        # versions pinned after tested resolution
    build.sh
    .env.example
    scrollrot_api/
      settings.py
      urls.py
      asgi.py
      wsgi.py
    accounts/               # Django app
    friendships/            # Django app
    battles/                # Django app
    tests/
  docs/
  prompts/
  render.yaml               # Render Blueprint for API + database
```

## Local setup

1. Install Python (version supported by chosen Django/DRF) and PostgreSQL. Create a virtual environment under `backend/.venv`.
2. Install Django, DRF, `djangorestframework-simplejwt`, `psycopg[binary]` (or compatible `psycopg2-binary`), `dj-database-url`, `gunicorn`, `uvicorn`, `whitenoise`, and testing libraries; pin compatible versions.
3. Use `django-admin startproject scrollrot_api .`, then create `accounts`, `friendships`, `battles` apps. Define custom user model **before the first migration**, if needed.
4. Configure local `.env` (never commit it): `DATABASE_URL`, `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, email configuration, `CORS_ALLOWED_ORIGINS` only if a browser frontend/admin integration is used. Android native networking does not require browser CORS.
5. Run `python manage.py check`, `python manage.py makemigrations`, `python manage.py migrate`, `python manage.py test` (or pytest).
6. Confirm authenticated calls via `curl` or Postman before Android Retrofit integration.

## Minimal deployment files (examples; adapt to real repo)

`backend/build.sh`:

```bash
#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
```

`render.yaml` in root (free **prototype**, NOT production):

```yaml
databases:
  - name: scrollrot-db
    plan: free
    databaseName: scrollrot
    user: scrollrot
services:
  - type: web
    name: scrollrot-api
    runtime: python
    plan: free
    rootDir: backend
    buildCommand: bash build.sh
    startCommand: python -m gunicorn scrollrot_api.asgi:application -k uvicorn.workers.UvicornWorker
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: scrollrot-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: 'False'
      - key: PYTHON_VERSION
        value: '3.12.10'
```

Use only a Python runtime version your app and Render support at deployment. The `startCommand` assumes a compatible Uvicorn worker is installed; validate the installed Gunicorn/Uvicorn pairing or use supported equivalent ASGI startup.

**Environment checklist (Render dashboard):** `SECRET_KEY`, `DATABASE_URL` from database, `DEBUG=False`, correct `ALLOWED_HOSTS` including Render hostname, secure-cookie/CSRF settings if admin/browser auth enabled, email provider secrets for verification/password reset, and optional monitoring secrets. No secrets in Git or Android APK.

## Deploy sequence

1. Push repo to GitHub. Render Dashboard → **New Blueprint** → connect repo and apply `render.yaml` (or create Postgres and a Web Service manually).
2. Watch build logs. Fail fast on migrations/staticfiles errors.
3. Verify `GET https://<your-service>.onrender.com/api/v1/health/` returns `200` after cold start.
4. Verify failed/unauthorized cases with external Postman/curl. Never expose Django Admin publicly without hardening.
5. Set Android `BuildConfig.API_BASE_URL` to deployed HTTPS API URL; create Retrofit client with timeouts, network errors and exponential backoff. Never call HTTP on production.
6. Upgrade database and web instance to production-safe plans, configure backups, alerts, and account deletion before inviting real users.

## Production deployment gate

- [ ] Production environment variables and HTTPS configured, `DEBUG=False`, checked `ALLOWED_HOSTS`
- [ ] Server tests pass (including non-member read and spoofed-score attempts)
- [ ] Migration/check/collectstatic/deploy success observed; healthcheck succeeds
- [ ] Paid production-grade DB with backups and restore exercise
- [ ] Permission and token revocation tests pass; secret redaction in logs
- [ ] Mobile offline + 401/429/retry tests pass
- [ ] GDPR/India privacy obligations assessed as applicable; published privacy/deletion policy matches behavior
