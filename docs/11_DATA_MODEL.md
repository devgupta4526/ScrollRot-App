# 11 — Local data model, transactions and time semantics

## Room entities (recommended, adapt after testing)

### `reel_event` (only if event-level history is truly needed)

- `id`: locally generated UUID
- `observedAtEpochMs`: event acceptance time in UTC
- `platform`: enum/string `INSTAGRAM|YOUTUBE|FACEBOOK|SNAPCHAT`
- `localDate`: ISO date determined with current user zone at time of acceptance
- `zoneId`: IANA zone (`Asia/Kolkata`, etc.) to explain date grouping
- `confidence`: finite enum, not invented numeric percentages
- `ruleVersion`: detector rule version for diagnostics
- `sessionId`: randomized short-lived, non-content ID; retention-limited
- **No screen text, video name/ID, URLs, captions, screenshots or UI trees**

### `daily_app_aggregate`

- Composite primary key `(localDate, platform)`
- `acceptedCount: Long`, `lastAcceptedAtEpochMs`, `lastRuleVersion`
- Unique constraints and atomic Room transaction prevent race/replay inflation.

### `goal_history` (optional)

- Effective start date, user-set daily target, modified UTC timestamp.

### `user_preferences` in DataStore

- `trackingPaused`, platform enabled flags, daily limit, haptics, notifications, reduced motion, overlay enabled, onboarding complete, consent version, retention period.

## Counting transactions

In `@Transaction`: accept once based on normalized replay/dedup key (not a video identifier), append minimal event if retention policy permits, increment daily aggregate, and publish Flow. Always protect against concurrent service restarts or duplicate async work.

## Day boundaries

- Store exact timestamps in UTC; group display with selected device zone.
- At midnight, a new local day is determined from `Clock` + `ZoneId`, not from app restart.
- Handle timezone changes, DST, leap days and changes to device clock. Document whether historic day assignments remain in their original zone or are recalculated. Recommended: preserve original local day and zone for stable history.
- Display history only as authoritative if tracking coverage is known; missed events may occur during OS restrictions.

## Migration

When replacing the starter's SharedPreferences counters: inspect its keys and daily-rollover behavior; write a one-time idempotent migration to Room with provenance labeled `legacy_estimated` (not verified); avoid double imports. Unit/instrumentation tests required.

## Privacy operations

- Implement delete history, delete all local data, export a CSV of **aggregates only** (explicit user action), and optional finite event retention (e.g. 30 days by default if events exist).
- Do not sync local history remotely without a distinct opt-in and data disclosure.
