# 15 — Focus mode, reminder notifications, and floating counter

## Gentle focus mode (M6)

- A user starts a local focus timer for a chosen period; timer survives activity recreation using stored `start`/`end` timestamps where appropriate.
- Show upcoming/end state, pause/stop options, and optional gentle reminders.
- An intervention can be a normal Scrollrot screen or notification; **do not guarantee a hard lockout** of social app flows on consumer Android.
- No UI automation to forcibly navigate another app or disable user/system controls.

## Notification reminders

- Ask `POST_NOTIFICATIONS` only when a user enables reminder notifications on Android 13+.
- Provide granular toggles, quiet hours and minimum intervals; ensure repeated events do not spam.
- WorkManager is for periodic non-exact background summaries; it is **not** an accurate event counter or exact timer guarantee.
- If notification permission denied, local history/counting still works.

## Live overlay (advanced, opt-in)

- Ask separately after demonstrating the feature. The bubble shows only app-labeled approximate count, pause/hide affordance and small footprint.
- Determine whether a scoped accessibility-service overlay is sufficient; request `SYSTEM_ALERT_WINDOW` only if implementing a permitted `TYPE_APPLICATION_OVERLAY` that needs it.
- Overlay must not impersonate social app UI, capture touches beyond its own bounds, obscure sensitive buttons or interfere with OS permission dialogs.
- Hide cleanly on lock, permission withdrawal, tracking pause, screen rotation and user dismissal.
- Test on different OEMs, Android versions and gesture navigation; no runaway updates/battery drain.

## Acceptance

Decline notifications or overlay without error; on/off toggles work; stop/pause acts immediately; screen content is not retained; overlay is legible and movable only if that behavior is actually implemented.
