# Scrollrot — verified project status

**Last reviewed:** 20 October 2026. **Status source:** earlier supplied source ZIP and documentation only; **no successful Gradle build verified in this conversation**.

## Status legend

`NOT STARTED` · `SOURCE PRESENT / UNVERIFIED` · `IN PROGRESS` · `BUILD VERIFIED` · `DEVICE VERIFIED` · `RELEASE READY`

| Feature / milestone | Status | Evidence needed for upgrade |
|---|---|---|
| Android Gradle import/build | SOURCE PRESENT / UNVERIFIED | `:app:assembleDebug` passes; note Android Studio and toolchain |
| XML home dashboard | SOURCE PRESENT / UNVERIFIED | Launch screenshot from real device |
| Canvas mascot idle animation | SOURCE PRESENT / UNVERIFIED | On-device motion check/reduced-motion state |
| Demo preview counter | SOURCE PRESENT / UNVERIFIED | Confirm production data unchanged |
| Accessibility disclosure + settings link | SOURCE PRESENT / UNVERIFIED | Consent/deny/revocation screenshots and review |
| Experimental event listener | SOURCE PRESENT / UNVERIFIED | Unit tests + physical app-version matrix |
| Reliable verified reel transitions | NOT STARTED | Golden test cases and false-positive gate |
| Room + DataStore migration | NOT STARTED | Data persistence and migration tests |
| Navigation + full onboarding | NOT STARTED | XML navigation/instrumentation tests |
| Insights, history, goals | NOT STARTED | Database test + charts against known data |
| Optional overlay / reminders | NOT STARTED | Opt-in, battery and tap-through tests |
| Friend/group battles (Django/Render) | IN PROGRESS | Milestone 09 backend skeleton & tests verified; auth/friends/battles pending |
| Play Billing subscriptions | NOT STARTED | License testers, server verification, restore tests |
| Play Store publication | NOT STARTED | Privacy, data safety, declarations, AAB/release testing |

## Current milestone

**Milestone 09 — Render backend setup (COMPLETED).** Next: `prompts/10_AUTH_AND_FRIENDS.md`.

## Evidence log — append; never invent

| Date | Device / OS | Command or manual case | Result | Commit |
|---|---|---|---|---|
| 2026-10-20 | Not tested | Source ZIP inspection | Files available; build not executed | — |
| 2026-10-20 | Windows 11 / Python 3.14.3 | `python manage.py check` | PASS (0 issues) | — |
| 2026-10-20 | Windows 11 / Python 3.14.3 | `python manage.py makemigrations` & `migrate` | PASS (accounts.0001_initial applied) | — |
| 2026-10-20 | Windows 11 / Python 3.14.3 | `python manage.py collectstatic --noinput` | PASS (157 static files copied) | — |
| 2026-10-20 | Windows 11 / Python 3.14.3 | `python manage.py test tests` | PASS (16 tests, 0 failures, 0 errors) | — |
| 2026-10-20 | Windows 11 / Python 3.14.3 | `pytest` | PASS (16 passed in 8.30s) | — |
| 2026-10-20 | Windows 11 / Python 3.14.3 | `GET http://127.0.0.1:8000/api/v1/health/` | PASS (HTTP 200 {"status":"healthy","database":"connected"}) | — |


## Open blockers

- Starter archive lacks full Gradle wrapper scripts/JAR; use Android Studio-generated compatible wrapper if necessary.
- A cross-platform reel count is **not** exact unless verified per app version and device.
- Google Play AccessibilityService disclosure/declaration must be implemented and reviewed before distribution.

## Product decision pending

- App's default meaning of count: recommended **new unique short-form item exposure** (first visible item + each accepted transition) rather than physical swipes. Validate the semantics with user research and consistent product copy.
