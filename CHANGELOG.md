# Scrollrot changelog

All changes should be appended by the coding agent when code/tests are actually modified. Do **not** list planned features as released.

## Unreleased
- Created an initial Kotlin/XML experimental source starter separately from this documentation pack (build not independently verified here).
- Added a structured product/technical/QA/permissions documentation pack and milestone-based AI prompts.

### 2026-10-20 — Milestone 09: Django REST Framework & PostgreSQL Backend Skeleton
- Implemented: Isolated Django 5/6 backend in `backend/` with DRF, SimpleJWT, `dj-database-url`, `psycopg[binary]`, WhiteNoise static file compression, and custom exception handler matching `docs/24_API_CONTRACT.md`.
- Implemented: Custom User model with UUID primary key, normalized email (`USERNAME_FIELD`), public display handle, and `DataSharingConsent` audit model before initial migration per `docs/16_BACKEND_AND_SOCIAL.md`.
- Implemented: Health endpoints (`/api/v1/health/` and `/health/`) returning service and database connectivity status with zero sensitive information leakage.
- Implemented: Render deployment configuration (`render.yaml` Blueprint for Web Service + Postgres, `backend/build.sh`, `.env.example`).
- Tested: `python manage.py check` (0 issues), `python manage.py makemigrations` (accounts initial migration generated), `python manage.py migrate` (applied cleanly), `python manage.py collectstatic --noinput` (157 files collected), `python manage.py test tests` (16 passed in 7.59s), `pytest` (16 passed in 8.30s), live HTTP GET to `http://127.0.0.1:8000/api/v1/health/` returning 200 OK.


### Milestone update template

```markdown
### YYYY-MM-DD — Mx feature
- Implemented: ...
- Tested: command/result/device ...
- Fixed: ...
- Remaining: ...
- Commit: ...
```
