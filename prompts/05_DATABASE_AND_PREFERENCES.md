# 05 — Room, DataStore and truthful local history

## Goal

Replace fragile persistence with transaction-safe Room aggregates and DataStore preferences while preserving proven existing data and keeping demo separate.

## Read first

- `docs/11_DATA_MODEL.md`
- `docs/05_ARCHITECTURE_AND_FOLDER_STRUCTURE.md`
- `docs/14_INSIGHTS_AND_GOALS.md`

## Execute this task

1. Introduce Room entities/DAOs/repository for bounded accepted normalized counts; settle event-level vs aggregate-only storage based on minimal collection.
2. Create DataStore for onboarding, goal, pause, user-selected platforms, haptics, reduced motion and consent version.
3. Make accepted-event persistence atomic/idempotent under callback repeats or service restarts; expose Flow to dashboard.
4. Create one-time idempotent import from starter SharedPreferences, explicitly label imported legacy counters as estimates.
5. Inject Clock/ZoneId, define day boundary handling, historical zone policy and restart behavior.
6. Implement delete/export aggregates and data clearing in settings; include confirmation and updated UI.
7. Add Room migrations and database unit/instrumentation tests; no destructive migration outside explicitly opted development state.

## Tests and verification

- [ ] Atomic count tests pass even with concurrent acceptance attempts
- [ ] Reopening/restarting does not double-count old events
- [ ] Midnight/timezone tests pass
- [ ] Import runs once and retains provenance
- [ ] Demo preview does not mutate Room

## Acceptance gate

- [ ] Real data drives home Flow
- [ ] Delete local history works
- [ ] No content data in schema
- [ ] Status and migration notes updated

## Stop condition

Do not proceed to the next milestone; give the exact next prompt path.


## Universal constraints

Read `AGENTS.md` first. The existing project is Kotlin + XML Views; never introduce Compose/Flutter. Inspect actual files before assuming paths exist. Make small compilable changes. Do not manufacture counts or tests. Update `PROJECT_STATUS.md`, `CHANGELOG.md` and, for major decisions, `DECISIONS.md` only after evidence. Use the required end-of-task report format.
