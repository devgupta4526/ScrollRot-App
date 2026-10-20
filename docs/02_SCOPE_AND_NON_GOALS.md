# 02 — Scope, release slices, definitions

## Vocabulary

- **Reel/item exposure:** a new distinct short-form video item appears as the active item in an eligible short-video viewer; count semantics are a **product assumption**, not a system guarantee.
- **Candidate:** an accessibility UI change that might correspond to a video item transition.
- **Accepted transition:** candidate that passes screen classification + change evidence + deduplication.
- **Unknown:** event lacks sufficient evidence; do not inflate count.
- **Session:** consecutive use within one supported short-feed screen, ended by leaving feed/app, device lock or prolonged inactivity.
- **Supported:** measured device/app-version configurations with documented tests, not merely an installed package.

## Must-have for first release

Offline onboarding, consent, limited service, one platform validated, local counts, home, goal, 7-day insights, settings, tests and disclosures. Other platforms may appear labeled **Beta/Unsupported** until validated.

## Should-have later

More validated apps, export/delete, gentle reminders, haptics, optional overlay, focus sessions.

## Could-have later

Cloud social, widgets, themes, subscriptions, group challenges, advanced animation storylines.

## Exclusions

Do not scrape video identifiers/captions, bypass an app's security, use hidden hooks/root or inject code in social apps, intercept private communications, automate swipes to measure feeds, or attribute mental/medical conditions to counts.

## UX truth labels

- `Tracking active` — service + opt-in + supported screen validated.
- `Ready, no supported feed detected` — service enabled but no accepted feed.
- `Tracking paused` — user-controlled paused state.
- `Enable access` — not enabled.
- `Limited accuracy` — supported detection but incomplete signal validation.
- `Unsupported on this app version` — stop counting where signals are insufficient.

Counts are estimates; never describe every physical scroll as a verified watched reel.
