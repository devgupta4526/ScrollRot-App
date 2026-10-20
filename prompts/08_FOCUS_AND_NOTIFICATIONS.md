# 08 — Gentle focus sessions, reminders and optional bubble

## Goal

Add voluntary wellbeing tools without claiming OS-level unbreakable blocking. All special access must be optional and separately explained.

## Read first

- `docs/15_FOCUS_NOTIFICATIONS_OVERLAY.md`
- `docs/12_PERMISSIONS_AND_COMPLIANCE.md`
- `docs/18_TEST_STRATEGY.md`

## Execute this task

1. Add optional local focus timers stored across activity recreation. Design paused/completed/aborted state UI.
2. Implement opt-in reminders at thresholds, with notification channels, spam safeguards and quiet hours.
3. Ask POST_NOTIFICATIONS only contextually on Android 13+; handle denial without impacting tracking.
4. Implement a small optional floating count bubble only after choosing appropriate lawful/scoped overlay type and explaining it to user.
5. Overlay must not cover OS permission UIs, intercept other app taps or continue after tracking pauses/revokes.
6. Add battery/performance profiling and service lifecycle tests; document unsupported OEM/system settings.
7. Do not implement automated gesture navigation or lockout that interferes with uninstall/disabling access.

## Tests and verification

- [ ] Focus survives Activity recreation
- [ ] Notification denied and quiet hours tested
- [ ] Overlay easily dismissible and never traps input
- [ ] Permission withdrawal removes overlay
- [ ] Battery/idle observations documented

## Acceptance gate

- [ ] Controls are voluntary and reversible
- [ ] No “cannot unlock” false promises
- [ ] No secret collection

## Stop condition

Do not proceed to the next milestone; give the exact next prompt path.


## Universal constraints

Read `AGENTS.md` first. The existing project is Kotlin + XML Views; never introduce Compose/Flutter. Inspect actual files before assuming paths exist. Make small compilable changes. Do not manufacture counts or tests. Update `PROJECT_STATUS.md`, `CHANGELOG.md` and, for major decisions, `DECISIONS.md` only after evidence. Use the required end-of-task report format.
