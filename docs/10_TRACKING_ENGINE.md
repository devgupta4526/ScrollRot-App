# 10 — Reel tracking engine: test-first technical contract

## Reality check

There is **no public Android API for exact per-reel views on other apps**. An `AccessibilityEvent.TYPE_VIEW_SCROLLED` means a view scrolled, not that the user watched one reel. UI nodes, indices and event patterns vary with app versions, locale, OEM and experimentation. Make no accuracy claims until supported configurations are tested.

## Pipeline

`AccessibilityService -> PackageFilter -> EventSanitizer -> ScreenClassifier -> PlatformDetector -> CandidateValidator -> Deduplicator -> TrackingRepository -> Room -> dashboard Flow`

### Minimal short-lived signal model (in memory)

```kotlin
data class UiSignal(
    val packageName: String,
    val eventType: Int,
    val elapsedRealtimeMs: Long,
    val appVersionCode: Long?,
    val screenHint: ScreenHint,
    val scrollDirection: Direction?,
    val itemChangedEvidence: Boolean?,
    val sessionToken: String // random ephemeral ID; never screen content
)
```

`itemChangedEvidence` must reflect actual, tested **non-content** UI signals; don't fabricate it. Keep raw AccessibilityNodeInfo instances inside the adapter's synchronous inspection scope and discard promptly. Never write raw signals with text to Room or logs.

### Results contract

```kotlin
sealed interface DetectionResult {
    data class Accepted(val app: Platform, val confidence: Confidence): DetectionResult
    data class Ignored(val reason: Reason): DetectionResult
    data class Unknown(val reason: Reason): DetectionResult
}
```

## Session & transition state

`OUTSIDE_FEED -> ENTERED_FEED -> OBSERVING_ITEM -> CANDIDATE -> VERIFIED_ITEM_CHANGE -> ACCEPTED -> OBSERVING_ITEM`. Reset to `OUTSIDE_FEED` on non-supported screen, app exit, lock, service interruption, or prolonged inactivity.

**Suggested count contract:** Count first verified distinct item when entering a supported feed, then one for each verified distinct active-item change. Alternatively choose “swipes only”, but do not mix semantics. Make the choice explicit in UX and tests.

## Validation and deduplication

- Filter only user-opted package names before inspecting nodes.
- Confirm feed mode; common false positives: comments scrolling, profile gallery, Explore/search, chat, ads, notifications, background content loading.
- Candidate from directional scroll/window transition; confirm item change with evidence independent of a raw scroll delta, when available.
- Coalesce event bursts (a tentative 500–900ms guard is a testable starting value, **not** a universal truth).
- Allow actual rapid item changes when positive evidence exists; avoid losing them to blunt time-only debounce.
- Debounce based on session+item transition, not just timestamps; stop counting if unique evidence unavailable.
- Store only accepted normalized `(platform, UTC instant, local-date context, confidence, rule_version)` events, or bounded aggregates; don't store video IDs.
- If reliability cannot be established for one app-version, disable the detector and show `unsupported`.

## Test cases (minimum)

- Enter feed / first item behavior; scroll forward x1 and x10; scroll back; fast consecutive swipes.
- Like/comment/share overlay; comments scroll; caption expansion; pause/play; ad insertion.
- Visit profile, home feed, DMs; app switch; screen lock; app process restart; service restart.
- Locale/font-size changes, low-power mode, old/new social versions and Android OS versions.
- Prove 10 actual transitions do **not** produce 20–30 persisted events.

## Confidence and UX

Use `verified_by_test_matrix`, `limited_evidence`, `unsupported` as support classes; avoid fake numeric 99% scores. Counts may be clearly labeled “estimated.”

## Privacy constraints

No OCR, MediaProjection, notification-listener scraping, capture of captions/DMs, or remote screen recording for this feature; no hidden logs of screen content. Raw access is powerful and must be disclosed precisely.
