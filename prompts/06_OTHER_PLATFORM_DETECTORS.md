# 06 — YouTube, Facebook and Snapchat compatibility layers

## Goal

Add **separate** detectors in measured order. If signals are inadequate, disable or mark unsupported; do not reuse Instagram conditions as fake universals.

## Read first

- `docs/10_TRACKING_ENGINE.md`
- `docs/19_DEVICE_AND_PLATFORM_MATRIX.md`
- `docs/18_TEST_STRATEGY.md`

## Execute this task

1. Create a detector registry with strict package + version support metadata and independent toggles.
2. Implement/test YouTube Shorts first, including standard video/search/comment false positives.
3. Implement/test Facebook Reels independently; do not enable Facebook Lite unless separately validated.
4. Implement/test Snapchat Spotlight; exclude chats, camera and stories. If missing signals, show unsupported.
5. Use shared pure pipeline but platform-specific feed detection and item-change evidence; no unsupported raw-scrolling fallback count.
6. Add synthetic fixtures and physical device matrix rows for each supported version and locale/OEM where possible.
7. Implement safe feature flags to turn off failing detectors in updates; record known limitations in settings.

## Tests and verification

- [ ] Per-app tests pass without cross-app false positives
- [ ] Counts persist by exact platform
- [ ] Disabled/unsupported platforms display honest status
- [ ] Package filtering is strict
- [ ] Device evidence recorded for claimed support

## Acceptance gate

- [ ] Do not mark all four apps Supported without real tests
- [ ] Graceful degraded behavior
- [ ] No unreviewed permissions

## Stop condition

Do not proceed to the next milestone; give the exact next prompt path.


## Universal constraints

Read `AGENTS.md` first. The existing project is Kotlin + XML Views; never introduce Compose/Flutter. Inspect actual files before assuming paths exist. Make small compilable changes. Do not manufacture counts or tests. Update `PROJECT_STATUS.md`, `CHANGELOG.md` and, for major decisions, `DECISIONS.md` only after evidence. Use the required end-of-task report format.
