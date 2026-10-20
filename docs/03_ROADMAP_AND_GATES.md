# 03 — Roadmap and hard acceptance gates

**Rule:** tackle each phase separately. An agent must stop if build/tests fail. Status belongs in `PROJECT_STATUS.md`; phases below are plans.

| Gate | Feature set | Required proof |
|---|---|---|
| M0 | Source audit and debug build | Gradle success, launch on phone, demo isolated |
| M1 | Design tokens, shell/nav, onboarding, mascot | XML previews/device screenshots, a11y and reduced motion |
| M2 | Consent/accessibility wiring, pause and settings | Denial/grant/revoke/interrupt tests, no unsolicited collection |
| M3 | Detector contract + Instagram pilot | Replayable fixtures, dedupe, false-positive audit, Room transaction |
| M4 | Other platforms independently | Package/app-version matrix per platform or disabled unsupported |
| M5 | Stats and goals | Room/DataStore migration tests, date rollover, no fake counts |
| M6 | Focus, reminders, optional overlay | Opt-in, no tap obstruction, battery check, permission denial |
| M7 | Render/Django API, accounts, friends and group battles | DRF object-level authorization and three-account tests, delete/leave flows, no unverified authority |
| M8 | Billing and release | License testing, entitlement checks, disclosures, Play testing |

## Detailed walkthrough

### Step 1: Establish the baseline (M0)

- Fix Gradle import issues only. Record build output and device model/API. Make a Git commit.
- Read `prompts/00_AUDIT_AND_BUILD.md`.

### Step 2: Build polished XML UI (M1)

- Define dimensions/colors/themes, use a single consistent component system.
- Create onboarding and navigation fragments, plus original mascot states and live state rendering.
- Profile animation to prevent constant layout invalidation.
- Read prompts `01` and `02`.

### Step 3: Secure consent and state flow (M2)

- Implement disclosure, separate opt-in choice, permissions status screen, Settings redirect and check-on-return.
- Observe only whitelisted packages/necessary event types; expose active/paused/not available indicators.
- Read prompt `03`.

### Step 4: Build a test-first reel event pipeline (M3)

- Create `FeedClassification -> Candidate -> Validation -> Accepted/Rejected/Unknown -> Repository`.
- Start with Instagram only; do device experiments and fixtures before promising counts. Add Room transaction and clear date/time behavior.
- Read prompts `04` and `05`.

### Step 5: Add other app detectors one by one (M4)

- YouTube Shorts first; Facebook Reels and Snapchat Spotlight after. Each one has its own release toggle, app-version matrix and fallback.
- Read prompt `06`.

### Step 6: Insights, reminders and focus (M5–M6)

- Real Room aggregation + DataStore preference state, custom-chart UI; avoid magic counts.
- Optional notifications/overlay only when user opts in. Avoid forced lockout claims.
- Read prompts `07` and `08`.

### Step 7: Deploy Django backend, build social + subscriptions (M7–M8)

- Deploy Django REST + PostgreSQL on Render; enforce auth, queryset scoping, membership checks, moderation, and score validation server-side. Social is not required for basic local tracking.
- Add Billing and backend receipt verification if subscriptions are enabled; ship only after full QA and policy review.
- Read prompts `09`, `10`, `11`, `12`, `13`.

## Universal definition of done

- [ ] Feature meets the user story and shows real/error/empty/permission-denied states.
- [ ] Build passes and command result is recorded.
- [ ] Unit tests pass; device test matrix entries added where applicable.
- [ ] No unnecessary permissions, stored raw screen content, hidden data transfer or inaccessible UI.
- [ ] Screens use original assets and honor reduced motion.
- [ ] `PROJECT_STATUS.md`, `CHANGELOG.md`, `DECISIONS.md` updated as appropriate.
- [ ] Git commit made; next phase unblocked explicitly.
