# 05 — App architecture and package layout

## Principles

- One app-level Activity and AndroidX Navigation fragments; XML/ViewBinding everywhere.
- `ViewModel` exposes immutable `StateFlow<UiState>`; Fragment renders lifecycle-aware state; no DB reads from XML/View classes.
- `Repository` is sole owner of data persistence and aggregation. Service sends normalized non-content events to processor, not directly to the UI.
- Core classifier and deduplication are **pure Kotlin** for unit tests; Android accessibility objects are adapted to short-lived, sanitized signals and discarded.
- Feature flags per detector; Render API integration and Billing outside core compile path until implemented.

## Proposed package tree

```text
app/src/main/
  AndroidManifest.xml
  java/com/scrollrot/app/
    ScrollrotApplication.kt
    MainActivity.kt
    core/{clock,model,privacy,permissions,util}/
    data/
      local/{ScrollrotDatabase,dao,entity,migrations}/
      preferences/{PreferencesRepository}/
      repository/{TrackingRepository,GoalsRepository,InsightsRepository}/
    tracking/
      ScrollrotAccessibilityService.kt
      AccessibilityEventAdapter.kt
      DetectorRegistry.kt
      FeedClassifier.kt
      ReelEventProcessor.kt
      detectors/{InstagramDetector,YouTubeDetector,FacebookDetector,SnapchatDetector}.kt
    feature/
      onboarding/{OnboardingFragment,OnboardingViewModel}/
      dashboard/{DashboardFragment,DashboardViewModel}/
      insights/{InsightsFragment,InsightsViewModel}/
      goals/{GoalsFragment,GoalsViewModel}/
      settings/{SettingsFragment,SettingsViewModel}/
      focus/{FocusFragment,FocusViewModel}/
      social/{FriendsFragment,ChallengesFragment}/  # future
      billing/{PremiumFragment}/                   # future
    design/{MascotView,GoalRingView,CounterAnimator}/
  res/{layout,drawable,anim,animator,values,xml,navigation}/
  assets/lottie/  # only authored/licensed JSONs
app/src/test/...  # pure detector/date/count tests
app/src/androidTest/...  # Room migration, permission screens, device tests
```

## Dependency direction

`View/Fragment -> ViewModel -> Repository interfaces -> Room/DataStore`  
`AccessibilityService -> sanitized signals -> detectors -> processor -> tracking repository`  
`Cloud/Billing adapters -> their own repository interfaces (not a prerequisite for home screen)`

## Stream and thread rules

- Accessibility callback lightweight; filter events immediately, never perform database I/O on its callback thread.
- Use bounded queues and a single ordered processor if event ordering matters; do not drop accepted events silently during congestion.
- Database commit drives flows; UI must not show an increment as persisted until the repository acknowledges acceptance.
- Do not over-poll, keep services stopped/limited when tracking is paused. A foreground service is not necessary for every feature.

## UI state model

Include: `TrackingPermissionState`, `TrackingActivityState`, `DetectorSupportState`, `TodaySummary`, `ByAppSummary`, `DailyGoal`, `MascotMood`, `isReducedMotion`, `error`. Handle unknown confidence and 0 separately.
