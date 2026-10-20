# 01 — Product Requirements Document (PRD)

## Identity

**Name:** Scrollrot. **Positioning:** playful, privacy-respecting digital-wellbeing companion for short-video habits. **Tagline:** “Track the scroll. Save your time.” Competitor functionality may inspire features, but never clone branding, art, screen composition or proprietary assets.

## Problem and user value

People often underestimate how long short-video sessions last. Scrollrot helps a person visualize **estimated** exposures, see habits by app/day, set self-chosen limits, and voluntarily take breaks. It must not shame users or make unsubstantiated neurological/mental-health claims.

## Personas

- **Casual checker:** wants a quick per-day count and gentle reminders without login.
- **Habit builder:** wants trends, goals and periodic resets; may prefer no floating UI.
- **Social challenger:** opts into private group competitions with friends; can delete account and leave groups.
- **Privacy-focused user:** needs clear opt-in and never shares raw on-screen content.

## Scope by priority

### P0 — first meaningful release

- `FR-01` XML onboarding explains estimates and required Android access.
- `FR-02` Dedicated, affirmative AccessibilityService opt-in; Settings transition; denied/revoked states.
- `FR-03` Observe eligible supported apps only; platform-specific state machine; validated candidate transitions.
- `FR-04` Persist per-day/per-app counts offline, prevent obvious duplicates and replay inflation.
- `FR-05` Animated home mascot, large total, daily progress and per-app breakdown.
- `FR-06` Local goals, pause/resume, reset/change history, privacy controls, accessibility, dark theme and reduced motion.
- `FR-07` Seven-day trend and clear ‘count estimate / unsupported’ indicators.

### P1 — quality upgrades

- `FR-08` Optional timely notifications; permission requested contextually.
- `FR-09` Local focus timer and gentle intervention; opt-in and cancellable as Android permits.
- `FR-10` Small live counter overlay, explicitly enabled, readily dismissible, no deceptive coverage.
- `FR-11` Export/delete local data and retention settings.

### P2 — social and commerce

- `FR-12` Sign in, profile, friends, private 1:1/group challenges.
- `FR-13` Clearly labeled approximate leaderboard scores, abuse protection and removal controls.
- `FR-14` Optional subscriptions; preserve basic tracking free; restore and cancel paths.

## Non-goals for initial release

- Perfect accuracy across all third-party social media app versions; browser reels tracking; prediction of brain health; psychological diagnosis; stealth monitoring of another person; unenforceable ‘unbreakable blocker’ guarantees.

## Key metrics

- Tracking opt-in conversion **without coercion**; events with accepted/unsupported status; estimated false positives from voluntary test cases; crash-free sessions; chart load speed; percentage of users completing a self-chosen goal; battery overhead while idle.
- Avoid addictive gamification or obsessive badges; allow dismissing streaks and competitions.

## Example user stories

- **US-1:** As a user, I can see clearly why access is needed before enabling it; denying it does not break the app.
- **US-2:** As a user, I can view today’s approximate counts grouped by supported app without an account.
- **US-3:** As a user, I can stop counting immediately from Scrollrot settings.
- **US-4:** As a user, I can distinguish true zero, not tracking, and unsupported screen states.
- **US-5:** As a user, I can delete all locally stored tracking data.

## Product acceptance

A release may not claim accurate counts unless the device/app test matrix demonstrates acceptable precision for explicitly supported app versions. If reliability is poor, ship as ‘estimated interactions’ or omit that platform.
