# 04 — Test-first reel detector and Instagram pilot

## Goal

Build a pure detector/state machine and a first **experimental** Instagram Reels adapter. Do not claim exact counting; only accept sufficiently validated new-item transitions.

## Read first

- `docs/10_TRACKING_ENGINE.md`
- `docs/19_DEVICE_AND_PLATFORM_MATRIX.md`
- `docs/18_TEST_STRATEGY.md`
- `docs/02_SCOPE_AND_NON_GOALS.md`

## Execute this task

1. Define `UiSignal`, `DetectionResult`, `Platform`, `Confidence`, `ScreenHint`, `SessionState` interfaces. Filter packages before constructing sensitive signals.
2. Implement screen-mode classifier independent of app event callback; ensure comments/chat/profile/home feed do not count.
3. Write a deterministic ordered state machine with enter-feed, observing-item, candidate, acceptance, rejection/unknown, session expiry and replay-safe deduplication.
4. Build unit fixtures with **synthetic/non-content** accessibility signals for repeated scroll events, fast swipes, direction reversals, first item and unrelated UI.
5. Implement Instagram Reels detector behind a feature flag; use only device-observed, privacy-minimized signals. Avoid invented view IDs/class patterns.
6. Separate candidate event processing from persistence; no SharedPreferences increment from each TYPE_VIEW_SCROLLED callback.
7. Add on-device manual test plan and capture observed vs accepted counts in 19_DEVICE_AND_PLATFORM_MATRIX.md.

## Tests and verification

- [ ] Synthetic candidate replay tests pass
- [ ] No increments for comments/home/profile/chat
- [ ] Rapid swipes and duplicate event storms handled without inflation
- [ ] At least one physical Instagram app-version tested before enabling supported label
- [ ] All unverified versions explicitly Experimental/Unsupported

## Acceptance gate

- [ ] Pure Kotlin tests cover state transitions
- [ ] Only accepted verified-enough transitions emitted
- [ ] No raw text or video content persisted
- [ ] If real device testing unavailable, status remains NOT DEVICE VERIFIED

## Stop condition

Do not proceed to the next milestone; give the exact next prompt path.


## Universal constraints

Read `AGENTS.md` first. The existing project is Kotlin + XML Views; never introduce Compose/Flutter. Inspect actual files before assuming paths exist. Make small compilable changes. Do not manufacture counts or tests. Update `PROJECT_STATUS.md`, `CHANGELOG.md` and, for major decisions, `DECISIONS.md` only after evidence. Use the required end-of-task report format.
