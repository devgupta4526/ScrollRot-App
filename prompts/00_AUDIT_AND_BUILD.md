# 00 — Audit the source, repair import and produce the first Android build

## Goal

Make the previously provided Kotlin/XML Scrollrot starter **actually build and launch** on a connected Android phone. Do not claim the existing source was previously compiled.

## Read first

- `START_HERE.md`
- `PROJECT_STATUS.md`
- `docs/04_STACK_AND_SETUP.md`
- `docs/18_TEST_STRATEGY.md`

## Execute this task

1. Inventory `settings.gradle.kts`, top-level/app Gradle configs, actual Kotlin, layouts, resources, manifest, min/target SDK and Gradle wrapper presence. Summarize compatibility without guessing.
2. If wrapper executables are missing, generate a supported wrapper from a known-good Android Studio Empty Views project; preserve matching AGP/Gradle/JDK versions and explain changes.
3. Run Gradle sync and `:app:assembleDebug`; fix manifest/XML/Kotlin issues narrowly. Do not add Django/Render/Room/Compose yet.
4. Inspect accessibility service and existing demo preview behavior; label unverified detection code as experimental.
5. Launch on a real device if available; document platform API and device model. Do not enable accessibility without user action.
6. Create one small smoke unit test and configure `:app:testDebugUnitTest` if missing.
7. Commit the passing baseline and update project evidence log.

## Tests and verification

- [ ] Actual `:app:assembleDebug` exit 0
- [ ] Actual `:app:testDebugUnitTest` exit 0, or explicitly NOT RUN reason
- [ ] Launch/no-crash and mascot preview confirmed on device, or clearly `NOT DEVICE VERIFIED`
- [ ] No debug demo values persisted to real counters

## Acceptance gate

- [ ] No unresolved Gradle issues
- [ ] Report exact files touched and version changes
- [ ] Tracking permission denial does not crash app
- [ ] Status marks only build/device results actually observed

## Stop condition

Do not proceed to the next milestone; give the exact next prompt path.


## Universal constraints

Read `AGENTS.md` first. The existing project is Kotlin + XML Views; never introduce Compose/Flutter. Inspect actual files before assuming paths exist. Make small compilable changes. Do not manufacture counts or tests. Update `PROJECT_STATUS.md`, `CHANGELOG.md` and, for major decisions, `DECISIONS.md` only after evidence. Use the required end-of-task report format.
