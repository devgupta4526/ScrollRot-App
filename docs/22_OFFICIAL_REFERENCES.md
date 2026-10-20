# 22 — Official references and version checks

**Links checked during pack preparation:** 20 October 2026. These are starting points, not a promise future rules remain unchanged.

## Core Android

- Android Studio install: https://developer.android.com/studio
- Accessibility service (Views): https://developer.android.com/guide/topics/ui/accessibility/views/service
- Accessibility events API: https://developer.android.com/reference/android/view/accessibility/AccessibilityEvent
- Usage statistics: https://developer.android.com/reference/android/app/usage/UsageStatsManager
- Android architecture: https://developer.android.com/topic/architecture
- Room: https://developer.android.com/training/data-storage/room
- DataStore: https://developer.android.com/topic/libraries/architecture/datastore
- WorkManager: https://developer.android.com/topic/libraries/architecture/workmanager
- MotionLayout: https://developer.android.com/develop/ui/views/animations/motionlayout
- Lottie Android implementation: https://github.com/airbnb/lottie-android

## Policy and shipping

- Google Play AccessibilityService policy: https://support.google.com/googleplay/android-developer/answer/10964491
- Sensitive permissions/API policy: https://support.google.com/googleplay/android-developer/answer/16558241
- Target SDK: https://support.google.com/googleplay/android-developer/answer/11926878 (Android mobile new apps/updates require target 36+ starting 31 August 2026)
- Data safety: https://support.google.com/googleplay/android-developer/answer/10787469
- Play Billing: https://developer.android.com/google/play/billing/integrate (official example showed 9.1.0 in October 2026)

## Rules for agents using sources

Prefer official docs for platform APIs and Play policy. A social app can silently change accessibility UI; treat third-party detector compatibility as empirical and version-bound. Never scrape sensitive content or assume app-internal source structure based on a marketing listing.

## Render/Django backend

- Render Django guide: https://render.com/docs/deploy-django
- Render Free instance limitations: https://render.com/docs/free
- Render WebSocket documentation: https://render.com/docs/websocket
- Render Key Value: https://render.com/docs/key-value
- Django security checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
- Django REST Framework: https://www.django-rest-framework.org/
