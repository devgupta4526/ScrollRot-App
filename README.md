# Scrollrot (ScrollRot-App)

**Product:** Scrollrot · Native Android (Kotlin + XML Views) & Django REST Framework Backend  
**Android Package:** `com.scrollrot.app` · **Min SDK:** 26 · **Compile/Target SDK:** 36  
**Backend:** Python Django 5/6, Django REST Framework, PostgreSQL, SimpleJWT, WhiteNoise, Render Blueprint  

Scrollrot is an original digital-wellbeing Android application designed to help users track and moderate doomscrolling through opt-in accessibility tracking, friendly mascot animations, and private friend/group challenges.

---

## Architecture Overview

1. **Android Client (`app/`)**:
   - Native Kotlin + XML Views (no Jetpack Compose or webviews).
   - Local-first and offline-functional using Room and DataStore.
   - Opt-in short-form video tracking via Android `AccessibilityService`.

2. **Backend API (`backend/`)**:
   - Django REST Framework + PostgreSQL + JWT Authentication.
   - Modular structure: `accounts`, `friendships`, `battles`.
   - Custom User model with UUID primary keys and normalized email.
   - Automated Render deployment blueprint (`render.yaml`).
   - Standardized API contract (`/api/v1/`) with healthcheck (`/api/v1/health/`).

---

## Repository Map

| Path | Purpose |
|---|---|
| `app/` | Native Android Kotlin/XML application |
| `backend/` | Django REST Framework API with PostgreSQL & JWT |
| `backend/scrollrot_api/` | Django project settings, ASGI/WSGI, routing, and exception handler |
| `backend/accounts/` | Custom User model, auth architecture, and data sharing consent |
| `backend/friendships/` | Friendships and social connections (Milestone 10) |
| `backend/battles/` | Group battles and score aggregates (Milestone 11) |
| `backend/tests/` | Backend test suite (health, settings guardrails, user model, error contract) |
| `render.yaml` | Render Blueprint configuration (Web Service + Managed PostgreSQL) |
| `docs/` | Comprehensive architecture and API specifications (01 to 24) |
| `prompts/` | Milestone-based development prompts (00 to 13) |
| `AGENTS.md` | Non-negotiable engineering rules and guidelines |
| `PROJECT_STATUS.md` | Evidence-based verified project status log |

---

## Backend Local Setup & Testing

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py test tests
python manage.py runserver
```

Health endpoint: `http://127.0.0.1:8000/api/v1/health/`
