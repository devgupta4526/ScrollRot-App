# 01 — Refactor to clean MVVM, navigation and testable state

## Goal

Introduce a maintainable View/XML structure without changing user-visible dashboard behavior. This is a foundation refactor, not new features.

## Read first

- `docs/05_ARCHITECTURE_AND_FOLDER_STRUCTURE.md`
- `docs/09_NAVIGATION_AND_STATES.md`
- `docs/04_STACK_AND_SETUP.md`

## Execute this task

1. Inspect current MainActivity/store files; design incremental migration with stable names.
2. Enable ViewBinding, AndroidX Navigation and ViewModel/StateFlow with lifecycle-aware collection.
3. Create a single MainActivity shell, dashboard fragment, future route placeholders only where navigable; no empty fake feature tabs.
4. Define DashboardUiState and TrackingPermissionState, immutable repository contracts, injectable Clock and simple testable fake repository for tests only.
5. Move preview/demo state to isolated debug-only source or explicit demo abstraction, separated from persistent tracking.
6. Extract reusable values/colors/dimens and ensure existing mascot renders under Fragment lifecycle.
7. Add navigation recreation and ViewModel reducer unit tests.

## Tests and verification

- [ ] Build and unit tests pass
- [ ] UI still launches and has same or better behavior
- [ ] Rotation/activity recreation does not duplicate counting
- [ ] Preview does not write to tracking repository

## Acceptance gate

- [ ] One Activity + Fragment XML shell
- [ ] UI collects StateFlow safely
- [ ] No premature cloud/injection framework
- [ ] Status/decision logs updated

## Stop condition

Do not proceed to the next milestone; give the exact next prompt path.


## Universal constraints

Read `AGENTS.md` first. The existing project is Kotlin + XML Views; never introduce Compose/Flutter. Inspect actual files before assuming paths exist. Make small compilable changes. Do not manufacture counts or tests. Update `PROJECT_STATUS.md`, `CHANGELOG.md` and, for major decisions, `DECISIONS.md` only after evidence. Use the required end-of-task report format.
