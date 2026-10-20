# 07 — Seven-day insights, goals and private data controls

## Goal

Create a real, local-first stats feature with XML charts, goal configuration and clear ‘estimated/partial/no data’ semantics.

## Read first

- `docs/14_INSIGHTS_AND_GOALS.md`
- `docs/06_UI_UX_SCREEN_SPECS.md`
- `docs/11_DATA_MODEL.md`

## Execute this task

1. Implement Room aggregation queries by local day/app and reactive ViewModel UI state.
2. Create XML InsightsFragment: 7-day history, accessible labels, per-app breakdown, empty and partial coverage states.
3. Implement user-editable daily goal with validation and state persistence; animate progress ring only from persisted counts.
4. Add reasonable visual progress and optional streak indicator; never present mascot as brain health diagnosis.
5. Implement settings export/delete and review summary after clearing history.
6. Create 200% font tests, dark/contrast checks, date rollover tests, no-data chart tests and recovery after app process kill.

## Tests and verification

- [ ] Counts match Room fixtures exactly
- [ ] Charts do not interpolate unknown days as zero
- [ ] Goals update without data loss
- [ ] Delete/export manual tests pass
- [ ] Build/test/a11y evidence provided

## Acceptance gate

- [ ] MVP UI has live data and privacy controls
- [ ] No fake populated history
- [ ] Local-only MVP usable without Django/Render

## Stop condition

Do not proceed to the next milestone; give the exact next prompt path.


## Universal constraints

Read `AGENTS.md` first. The existing project is Kotlin + XML Views; never introduce Compose/Flutter. Inspect actual files before assuming paths exist. Make small compilable changes. Do not manufacture counts or tests. Update `PROJECT_STATUS.md`, `CHANGELOG.md` and, for major decisions, `DECISIONS.md` only after evidence. Use the required end-of-task report format.
