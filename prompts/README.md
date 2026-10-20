# Scrollrot — AI implementation prompts (Render backend, no Firebase)

Execute a single task per session/branch. The Kotlin/XML local-first app is independent of the server. Require **actual** builds and test logs before marking a milestone complete.

| # | Prompt | Prerequisite | Acceptance |
|---|---|---|---|
| 00 | [Audit and build](00_AUDIT_AND_BUILD.md) | Source starter | Gradle debug build |
| 01 | [App architecture](01_FOUNDATION_AND_ARCHITECTURE.md) | 00 | ViewBinding/MVVM skeleton |
| 02 | [UI + animation](02_UI_AND_ANIMATIONS.md) | 01 | Polished original XML UX |
| 03 | [Accessibility/consent](03_PERMISSIONS_AND_ACCESSIBILITY.md) | 02 | Explicit opt-in and denial states |
| 04 | [Instagram detector](04_TRACKER_CORE_INSTAGRAM.md) | 03 | Tested candidate-to-count pipeline |
| 05 | [Room and DataStore](05_DATABASE_AND_PREFERENCES.md) | 04 | Offline data persistence |
| 06 | [Other-platform detection](06_OTHER_PLATFORM_DETECTORS.md) | 05 | Validated per-platform support |
| 07 | [Insights + goals](07_INSIGHTS_AND_GOALS.md) | 05/06 | Real local data visualizations |
| 08 | [Focus + optional overlay](08_FOCUS_AND_NOTIFICATIONS.md) | 07 | Consent, fallbacks, battery tests |
| 09 | [Django/Render backend](09_RENDER_BACKEND_SETUP.md) | 07+; optional | Health route, DB, server build/deploy plan |
| 10 | [Authentication + friends](10_AUTH_AND_FRIENDS.md) | 09 | JWT + privacy-negative tests |
| 11 | [Group battles](11_GROUP_BATTLES.md) | 10 | Secure member-only leaderboards |
| 12 | [Premium Billing](12_PREMIUM_AND_BILLING.md) | Optional after MVP | Verified entitlement handling |
| 13 | [QA and Google Play](13_QA_POLICY_AND_RELEASE.md) | MVP scope | Release testing and disclosures |

You can ship a privacy-reviewed MVP after 07 or 08; the API is only necessary for opt-in social features.

## Universal task footer

```text
Before coding: read AGENTS.md, PROJECT_STATUS.md, DECISIONS.md and the specifications named in this prompt. Inspect the existing repo. Kotlin and XML only on Android. Build one vertical slice; run actual tests and show results. Never invent API deployment, test outcomes, perfect detector accuracy, production-readiness, or cloud credentials. Update status/changelog and stop at the acceptance gate. Keep all local tracking working offline and never transmit raw AccessibilityService data.
```
