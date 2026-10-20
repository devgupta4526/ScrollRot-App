# 03 — Correct permissions UX and AccessibilityService boundaries

## Goal

Implement explicit transparent consent, manual OS setting, status checks, pause/resume and minimal event forwarding. Do not implement counting from raw scroll events yet.

## Read first

- `docs/12_PERMISSIONS_AND_COMPLIANCE.md`
- `docs/09_NAVIGATION_AND_STATES.md`
- `docs/10_TRACKING_ENGINE.md`
- `docs/13_PRIVACY_AND_SECURITY.md`

## Execute this task

1. Create a standalone consent screen with truthful precise disclosure, separate Not now / I agree actions, and link to full privacy policy when available.
2. Only after affirmative opt-in, navigate to system Accessibility Settings; on return query actual enabled service state, not intent result.
3. Use service-bound BIND_ACCESSIBILITY_SERVICE declaration and restrictive `res/xml/accessibility_service_config.xml`: package/event filtering and UI retrieval only when necessary. Set `isAccessibilityTool=false`.
4. Immediately discard events when user paused, target app not selected, or service state invalid; remove raw text/content logging.
5. Expose availability with sealed states (no permission/consent, off, active, paused, interrupted) and persist explicit tracking toggles in preferences.
6. Add denial/withdrawal/return-from-settings UX tests; record the consent text as a reviewed product string, not generic legal boilerplate.
7. Ensure no permission is falsely called a standard runtime permission; add test instructions for OEM restrictions.

## Tests and verification

- [ ] Grant, deny, return, revoke, interrupt, pause tested on device
- [ ] No events processed while paused or from unknown packages
- [ ] No raw screen contents logged
- [ ] Build and tests pass
- [ ] No OS settings are changed autonomously

## Acceptance gate

- [ ] Clear disclosure + affirmative action
- [ ] App usable without permission
- [ ] Visible tracking status
- [ ] Policy declaration requirement documented (not claimed approved)

## Stop condition

Do not proceed to the next milestone; give the exact next prompt path.


## Universal constraints

Read `AGENTS.md` first. The existing project is Kotlin + XML Views; never introduce Compose/Flutter. Inspect actual files before assuming paths exist. Make small compilable changes. Do not manufacture counts or tests. Update `PROJECT_STATUS.md`, `CHANGELOG.md` and, for major decisions, `DECISIONS.md` only after evidence. Use the required end-of-task report format.
