# SCROLLROT — COMPLETE PRODUCT & ENGINEERING SPECIFICATION

Version 1.0 · 19 October 2026 · Android native Kotlin + XML, NOT Compose

## Executive brief

**Product:** Scrollrot — an original, playful digital wellbeing app that observes short-form video navigation in selected apps, estimates swipe-to-next-reel transitions, and turns scrolling awareness into a positive habit.

**Core promise:** "Know your scrolls. Choose your next move." Avoid medical assertions such as "your brain has been damaged"; the mascot state is a playful metaphor, not a neuroscience measurement. Avoid claiming *exact every reel* unless validated across device and app-version matrix.

**User:** Android social-media users who want visible counters, gentle nudges, limits, personal trends and optional friends challenges.

**Primary differentiator:** A glowing spiraled blob mascot, in-session live progress and post-session victories; optional low-pressure, privacy-first friend challenges.

**Not a clone:** Do not use the BrainPal name, icon, mascot illustration, screenshot images, brand copy or paid animations. Create original UI, illustrations, sounds and asset licenses.

## 1. Product features, prioritized

### P0 — MVP (ship for internal testing)

- 3-page consent-first onboarding with 6–12 second skippable previews: problem, how tracking works, permissions.
- AccessibilityService permission flow, check for currently enabled state, don't ask for permission repeatedly. Explain what Android will expose.
- Detect *candidate* short-feed transitions for Instagram, Instagram Lite, YouTube Shorts, Facebook, Facebook Lite and Snapchat Spotlight; per-app adapter flags and remote/local configuration.
- Debounce scroll events and deduplicate on transition identity; log counters/diagnostic stats but never persist accessibility content.
- Live dashboard count, character mood changes, progress-to-user-selected goal, per-app breakdown.
- Room: durable per-day/per-app counts, optional event metadata free of watched content, session buckets.
- Settings: selected apps, set daily goal, pause tracking, export counts CSV, clear data, help and privacy, reduced motion.
- Error states: permission disabled, screen unsupported, unknown detection, battery restrictions, no network for social.

### P1 — Delight + habits

- Floating opt-in count chip outside tracked social apps via a tightly scoped `TYPE_ACCESSIBILITY_OVERLAY`; tap/drag/hide when the service is active. Overlay should never cover essential system controls, trick users, or intercept touches unexpectedly.
- 7- and 30-day analytics, categories by app, trends, best days, estimated minutes *separately labeled* if based on time not reel count.
- Daily milestone celebrations, animated streaks, optional gentle notifications at 50/75/100% of goal, quiet hours.
- Customizable focus/break timer, optional blocking *after* careful testing and Play policy review. Don't advertise unbreakable blocking.
- Intro/exit animation choreography, skeleton states, reduced-motion alternatives, dynamic layout.

### P2 — Social + monetization

- Django account authentication (email/password + JWT), user handles, friend requests, friend privacy.
- 1:1 and opt-in group battles, invite codes, daily/weekly leaderboard, timezone-boundary rules, ties, clock-skew handling, opt-out, delete battle history.
- Django API validation, DRF object permissions, throttling, abuse/rate limits, clear explanation that casual self-reported mobile counts are not tamper-proof.
- Google Play Billing: premium limits/insights/cosmetic themes; restore purchase, price disclosures, cancel flow and secure entitlement verification. Never lock data deletion or essential privacy controls behind a paywall.

## 2. Screens and interaction design

| Screen | Components | Key animations / transitions |
|---|---|---|
| Splash | logo swirl, glow, short brand line | 450ms logo trace then 200ms crossfade; no mandatory long wait |
| Onboarding 1 | story, original 3D-ish blob mascot | floating idle 2.4s, headline rise 320ms |
| Onboarding 2 | fake demo counter over simulated swipe illustration | integer roll 220ms, blob reaction 420ms |
| Permissions | clear disclosure, supported app chips, Open Settings | 180ms chips stagger, 260ms CTA; never fake permission grant |
| Home | large count, mascot, goal arc, cards, app breakdown | count pop 220ms, mascot bounce 340ms, level transform 500ms |
| Insights | 7/30 days, trend graph, calendar, per-app ranking | bar grow 350ms with 35ms stagger, crosshair 100ms |
| Focus/limits | goal slider, break session, allowlist | slider spring, progress sweep; calm idle |
| Live overlay | small movable counter pill + optional icon | fade 160ms, soft scale 240ms, no animation during video playback if too intrusive |
| Friends | connect, compare, invite, privacy | card slide 250ms, subtle confetti on victory |
| Group battle | 2–8 players, score comparison, expiry | row change 180ms, rank shuffle 450ms |
| Profile | avatar, privacy, subscription | simple shared element / crossfade |
| Settings | tracking toggles, permission status, data options | standard accessible transitions |
| Paywall | clear premium comparison, pricing, restore | restrained attention; no dark patterns |
| Data privacy | disclosure, activity retention, export/delete | straightforward no gamification |

### Design tokens — original Scrollrot identity

- Ink/background `#0D1020` ; panels `#1B2035`, elevated `#292E49`.
- Primary lime `#B3FF72`, violet `#917BFF`, pink `#FF7FBD`.
- Main text `#F9F8FC`; secondary `#A5ACC6`; warning amber `#FFD262`.
- Typography: rounded sans font under appropriate license (e.g. Nunito Sans or Manrope), numerical KPI heavy 52–72sp with tabular digits if possible.
- 8dp spacing system; screen insets 20–24dp; 24dp card radius; 16–18dp button radius; minimum 48dp hit areas; elevated surfaces with subtle radial glows, not constant heavy shadows.
- Portrait-first, landscape/tablet responsive via `ConstraintLayout` + `dimens.xml` (`sw600dp` alternative) and window insets. Text scales up to 200% without clipping.
- Central mascot is **a pear-like/lumpy blob with a single spiral-shaped forehead line**. Distinct from a brain-shaped character used elsewhere. Four art states: energized lime (0–24), drifting amber (25–74), saturated pink (75–149), resting violet (150+). Values are **defaults configurable to goal**, not measured damage.

### Motion design, production quality

- Idle mascot: 2.3–2.8s slow vertical bob (3–6dp), periodic blink every 4–8s, slight spiral rotation/shine.
- Counter update: digits pop to 1.12x then return over 220–290ms; haptic tick only if app foreground and user enabled haptics.
- State change: 2-stage 350–550ms crossfade/morph, intermittent sparkles (never rapid flashes), label update on completion.
- Goal ring: determinate stroke animation 420ms, do not sweep from zero on every `onResume`.
- Chart: draw bars 300–450ms; chart selection with talkback value.
- Success: 400ms confetti particles with max 24 sprites and no endless GPU loop.
- Skeleton shimmer: optional while loading remote data; cap to 1–2s then show real empty/error state.
- Reduce motion: obey `ValueAnimator.areAnimatorsEnabled()` and user app toggle. Provide nonanimated equivalent; no auto-playing soundtrack.
- Lottie JSON assets: `mascot_idle.json`, `mascot_blink.json`, `mascot_swipe.json`, `mascot_tired.json`, `mascot_rest.json`, `celebrate.json`, `streak.json`; all should be created for Scrollrot with a consistent visual style. Do not assume a model can create licensed animation JSON correctly; validate each animation in Android Studio.

## 3. Android tech decisions

- **Language/layout:** Kotlin, XML views, ViewBinding, Fragments, ConstraintLayout, Material Components, RecyclerView (where needed); no Jetpack Compose.
- **Pattern:** single-activity MVVM; `ViewModel` → `StateFlow<UiState>`; `Repository` joins Room/DataStore; pure domain detector rules; service only forwards lightweight observations.
- **Persistence:** Room 2.8.x stable or a compatible newer stable release; DataStore preferences for settings.
- **Concurrency:** coroutines with `Dispatchers.IO`; Room transaction for count increment; no expensive DB write per raw accessibility event. Prefer bounded buffer and flush accepted reel transitions, tolerating restart safely.
- **Animations:** Lottie for authored character states; MotionLayout for multi-property screen motion; ValueAnimator, AnimatorSet and SpringAnimation for count and gestures; custom Canvas for rings and particle effects.
- **Dependencies:** official stable AndroidX/Lottie versions; pin and centralize in `gradle/libs.versions.toml`. Before adding large libraries, use built-in Canvas where possible.
- **Optional online:** Django REST Framework, PostgreSQL, JWT on Render; consent only; never upload screen text, captions or video metadata.
- **Billing:** Google Play Billing Library with server-side subscription validation in a later phase.

## 4. The difficult engineering: counting a reel

### Reality check

- Android does **not** expose a public universal "reel viewed" or "reel next" event across social apps.
- `TYPE_VIEW_SCROLLED` may represent comments, profiles, comments panel, feed scrolling, scrub bars, lazy list settling and offscreen changes, not necessarily a new video.
- Accessibility trees, view IDs and labels change without notice between app versions, localizations, A/B tests and OEM versions. Some transitions produce no accessible scroll events.
- UsageStats tells app visibility/usage time, not individual video transitions; no video scanning is justified for this use case.
- Start with a labelled **estimated scroll count** and add per-platform quality/confidence indicators.

### Proposed detector interface

```kotlin
interface PlatformDetector {
    val packageNames: Set<String>
    fun inferScreen(snapshot: MinimalUiSignals): ScreenType
    fun inferTransition(event: UiSignal, previous: DetectorState): TransitionCandidate?
}

data class TransitionCandidate(
    val platform: Platform,
    val eventUptimeMs: Long,
    val confidence: Confidence,
    val reasonCode: ReasonCode // no raw user content
)
```

Adapters: `InstagramDetector`, `YouTubeShortsDetector`, `FacebookReelsDetector`, `SnapchatSpotlightDetector`, plus Lite variants. Keep every matcher behind runtime feature flags so broken versions can be disabled.

### Detection pipeline

1. **Package gate**: selected app installed and enabled in user's Scrollrot settings; use the service's package filter.
2. **Screen classification**: using the smallest possible observable UI signals determine `SHORT_FEED`, `OTHER_APP_SCREEN`, `UNKNOWN`, `COMMENTS_OVERLAY`, or `OFFSCREEN`. Do not persist node text.
3. **Transition**: observe vertical swipe/scroll with a changed stable item indicator when available; debounce settling event bursts. Swipe and watch-count are different concepts.
4. **Dedup**: emit at most one accepted transition for the same stable item fingerprint, and enforce an adaptable time window as a secondary fallback.
5. **Confidence**: `HIGH` if a supported feed context and changed item token were both seen; `MEDIUM` if feed context + plausible swipe; otherwise `LOW` and do **not** count silently.
6. **Repository**: store accepted count with `dateLocal`, `zoneId`, `platform`, `sessionId`, detector revision, and aggregate confidence; do not store content fingerprint/text itself long-term.
7. **UI update**: `Flow` pushes count immediately; optimistic animation can fire after DB confirms accepted event.
8. **Cooldown state**: stop counting on app change, comments, permissions screen, lock screen and when tracking is paused.

### No false confidence

The included prototype checks limited labels (e.g. Reels/Shorts + familiar control labels) and scroll debounce, which proves basic wiring **not** exact correctness. Calibrate detectors by watching a test device and comparing manual clicker ground truth against accepted transitions; make per-platform test cases from synthetic/anonymized events and expected count, not user content dumps.

## 5. Optional blocking / intervention

- Only promise blocking for a supported app/OS combination after validating feasibility; third-party app UI and user permissions can change.
- Prefer user-facing break screen, app-owned timer, or timely overlay prompt. Navigating users away from selected content using accessibility global actions is delicate and must have specific user authorization and comply with Play policy. Never claim system-level non-bypassable blocking.
- Distinguish "limit reached", "nudge displayed", "blocking attempted", and "blocking confirmed" states.
- Provide temporary user override and understandable exit, without trapping people in third-party apps or on top of critical calls.
- **No `SYSTEM_ALERT_WINDOW` needed for the starter.** A connected accessibility service has its own accessibility overlay window type for a narrowly-scoped optional chip; review policy and tap-through safety before enabling.
- Hard timer modes should be transparent, reversible according to user-configured terms, never prevent disabling the service/uninstall.

## 6. Data model

### Room tables

```text
ScrollDailyEntity:
  localDate: String (composite key with platform & deviceProfile)
  zoneId: String
  platform: String
  count: Int
  lowConfidenceDiscarded: Int
  updatedAtEpochMs: Long

ScrollSessionEntity:
  sessionId: String (PK)
  platform: String
  startedAtEpochMs: Long
  endedAtEpochMs: Long?
  acceptedCount: Int
  detectorVersion: Int

GoalEntity:
  goalId: String (PK)
  dailyReelCap: Int
  selectedPlatforms: Set<String> (via TypeConverter)
  startLocalDate: String
  enabled: Boolean

FocusSessionEntity:
  id, plannedDurationMs, startedAt, endedAt, status
```

At midnight, old day remains in Room; new record is created. DST/timezone transitions must not accidentally combine or discard dates; decide whether day boundary follows current device time or a fixed profile zone and explain to user. Use unique indexes and transactions for concurrent increments.

DataStore: consent-version, onboardingComplete, selectedApps, trackingPaused, overlayEnabled, reducedMotion, hapticEnabled, quietHours, goal, diagnosticOptIn.

### Custom Django API on Render (only after explicit opt-in to social)

Cloud features use a **Django REST Framework + PostgreSQL** monolith on Render; Android uses Retrofit/OkHttp and only uploads consented daily estimated aggregates. JWT-authenticated users, friendships, member-only battles and score upserts are enforced by DRF permissions and server-side queryset scoping. No Firebase services are used. See `docs/16_BACKEND_AND_SOCIAL.md`, `docs/23_RENDER_DEPLOYMENT.md`, and `docs/24_API_CONTRACT.md`.

## 7. Expected Kotlin package structure

```text
com.scrollrot.app/
  ScrollrotApp.kt
  MainActivity.kt
  core/{ui,animation,design,permissions,util}
  data/local/{AppDatabase,dao,entity,migration}
  data/preferences/SettingsStore.kt
  data/repository/{ScrollRepository,GoalRepository,FriendRepository}
  domain/model/{Platform,ScrollObservation,DetectionConfidence,BrainState}
  domain/usecase/{CountTransition,GetTodaySummary,CheckGoal,GetWeeklyStats}
  tracking/ScrollrotAccessibilityService.kt
  tracking/DetectorOrchestrator.kt
  tracking/platform/{InstagramDetector,YouTubeDetector,FacebookDetector,SnapchatDetector}
  tracking/overlay/CounterOverlayController.kt
  ui/onboarding/{WelcomeFragment,ConsentFragment,PermissionsFragment}
  ui/home/{HomeFragment,HomeViewModel,RotCharacterView}
  ui/stats/{StatsFragment,StatsViewModel,WeeklyChartView}
  ui/focus/{FocusFragment,FocusViewModel}
  ui/friends/{FriendsFragment,FriendBattleFragment,FriendsViewModel}
  ui/settings/{SettingsFragment,SettingsViewModel}
  billing/{BillingRepository,PaywallFragment}
  notifications/{ReminderScheduler,ReminderWorker}
```

XML files under `res/layout`, `res/drawable`, `res/animator`, `res/motion`, `res/xml`, `res/raw` (Lottie), `res/values`, `res/values-night`. Fonts in `res/font` with redistributable licenses.

## 8. User flows

### New user

Install → brand splash (skippable) → welcome/story → how estimation works → **separate prominent accessibility disclosure + opt in** → Android Settings → come back → validate service truly enabled → animate first count (only on actual observed evidence) → optional goal setup → dashboard.

### Recurring user

Open → daily summary → state changes immediately if count updated while app in background → optional goals/insights → pause controls. If permission revoked, show non-alarming empty state and repair button instead of prompting in an endless loop.

### Blocking (later)

User explicitly enables intervention → sees clear what content can be affected → chooses scope + cap + override behavior → reach cap → show gentle interruption → user can dismiss/override according to agreed design → record policy-independent status.

### Battles (later)

Opt into account → friend invites → accept → score sharing explainer → create challenge (1:1/group) → live asynchronous comparison → end at fixed timezone-aligned deadline → results/confetti → opt out/delete.

## 9. Animation asset brief for animator / AI-art pipeline

Build mascot assets originally for Scrollrot, not traced from any competitor. Required outputs:

1. `scrollrot_base.svg` layered vector model with body, spiral, eyes, mouth, feet, glow.
2. Lottie `idle.json` (2.6s looping) — bob, blink, barely shifting glow.
3. `swipe_reaction.json` (400ms one-shot) — wobble and two sparks.
4. `stage_drift.json` (480ms) — lime-to-amber gradient crossfade, tired eyelids.
5. `stage_saturated.json` (520ms) — hot pink body, unsettled spiral and pulsing outline.
6. `stage_rest.json` (560ms) — purple cozy/restful, no violent cracking or medical claim.
7. `goal_hit.json` (600ms one-shot) — tasteful halo burst, 20 max confetti particles.
8. `level_up.json`, `friend_win.json`, `permission_success.json`.

Every animation: 60fps-capable, pause when view offscreen, haptics optional, minimal file size, respects Animator duration scale/reduce-motion setting. Provide flat static state assets to fall back on if Lottie parsing fails.

## 10. Performance / battery

- No screen recording, MediaProjection, screenshot scanning or content storage for counting.
- Keep service packageNames scoped to supported apps; inspect the hierarchy only when needed and cap traversals.
- Debounce and throttle window-content events. Never allocate giant bitmaps or queue unbounded UI tree snapshots.
- Count and persist with nonblocking coroutine transactions, Room flow update; avoid continuous work when no supported package is visible.
- Overlay optional; remove it on unsupported screen, pause, revoke and service disconnect.
- Avoid long-running foreground service without valid FGS type/purpose. `AccessibilityService` is Android-managed after user opt-in.
- Benchmark baseline 60fps UI, service wakeups, memory, battery and cold start on low-end Android devices.

## 11. Privacy, policy, accessibility

- Prominent, standalone in-app accessibility disclosure and affirmative consent **before** sending to Android Accessibility Settings.
- Disclose possible UI access accurately even if Scrollrot intentionally avoids collecting private messages. No false claim that the OS prevents such access.
- Mark `isAccessibilityTool=false` unless Scrollrot is genuinely designed primarily for disability accessibility.
- Submit an Accessibility API declaration and demonstration video. Include website privacy policy, developer contact and Play Data safety declarations reflecting real app behavior (Render API, analytics, crash logging, etc.).
- Never prevent user disabling the accessibility service or uninstalling app. Never auto-enable permissions or bypass safeguards.
- Android 17 Advanced Protection can remove non-accessibility-tool services; show an understandable unavailable state, do not spoof classification to bypass protection.
- Provide user control to stop counting, clear/export history, opt out of cloud, revoke friend access, delete account/data.
- No notification permission until actually delivering notifications. Do not request overlay/screen capture/device admin/usage access by default.
- Allow TalkBack navigation, content descriptions for mascot/count/progress, sufficient contrast, min 48dp taps, system text scaling and reduced motion.
- Keep account optional for local features. Children's privacy regulations and age-appropriate design should be assessed before social features.

## 12. Test plan and release gates

See `TEST_MATRIX.md` for details.

**Ship-blocking checks:**
- Android Studio Gradle sync and build passes, lint blockers fixed.
- Onboarding permission denial and revocation do not crash.
- Counters remain accurate after process death, midnight rollover, reboot, timezone shift; no phantom counts from other screens or comments.
- Device test: at least 3 devices × Android 11, 13, 15, 16, 17 if feasible; various densities and fonts.
- Each social app tested on 2+ app versions and multiple accounts/languages where practical.
- Record confusion matrix: false counts / 100 manual scrolls, missed counts / 100 and median UI update latency. Define an accuracy goal empirically before saying exact.
- Accessibility overlay does not obstruct critical UI/touches or leak to lock screen.
- Battery overhead accepted in an explicit benchmark; no excessive access events logged.
- DRF API access control tested on unauthorized reads/writes; Billing pending/refund/restore tested in Play license environment.
- Privacy policy, in-app accessibility disclosure, Play Console declaration and Play Data safety forms completed.

## 13. Suggested phased delivery and acceptance

**Milestone A — 3–5 focused coding sessions**: import starter, polish XML Home, accessible onboarding, permission state, lifecycle stability, demo mascot; app builds and demo swipes visibly animate.

**Milestone B — detector validation**: per-platform adapters and diagnostics, Android device test runs, manually verified basic count for supported versions, no persistent sensitive UI data, honest accuracy indicator.

**Milestone C — persistent product**: Room/DataStore, stats, goals, export/delete, optional overlay, offline-first, performance test.

**Milestone D — interventions**: reminder/limits, carefully reviewed user-authorized blocking, health-neutral copy, Play policy compliance.

**Milestone E — social/revenue**: opt-in auth, battle data model, Django services and authorization tests, Billing, end-to-end QA.

**Milestone F — release**: closed testing, icon/screenshot original assets, Data safety, accessibility declaration/demo, policies and production observability.

## References verified 19 Oct 2026

- BrainPal overview: https://play.google.com/store/apps/details?id=com.brainrot.android
- BrainPal public site: https://brainrotapp.ai/
- Accessibility service: https://developer.android.com/guide/topics/ui/accessibility/views/service
- Accessibility events: https://developer.android.com/reference/android/view/accessibility/AccessibilityEvent
- Google Play Accessibility API policy: https://support.google.com/googleplay/android-developer/answer/10964491
- Play sensitive permissions: https://support.google.com/googleplay/android-developer/answer/16558241
- UsageStatsManager: https://developer.android.com/reference/android/app/usage/UsageStatsManager
- Android 17 SDK: https://developer.android.com/about/versions/17/setup-sdk
- Android Gradle plugin versions: https://developer.android.com/build/releases/about-agp
- Room releases: https://developer.android.com/jetpack/androidx/releases/room
- Lottie Android: https://github.com/airbnb/lottie-android
