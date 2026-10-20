# 04 — Tech stack, toolchain and dependency guidelines

## Baseline toolchain

Use source starter settings unless verified import errors require a change: Kotlin 2.3.21, Android Gradle Plugin 8.13.2, Gradle 8.13, JDK 17, min SDK 26, compile/target SDK 36. **Do not assume old or future plugin versions work together.** Google Play has required API 36+ for new Android mobile apps and updates since 31 August 2026 (subject to published exceptions).

Official requirements: https://support.google.com/googleplay/android-developer/answer/11926878

## Libraries / responsibilities

| Library | Role | When |
|---|---|---|
| AndroidX AppCompat + Material Components | Styled XML Views | M0/M1 |
| ConstraintLayout + MotionLayout | Responsive/animated XML | M1 |
| Navigation Fragment + UI | Typed destinations/back stack | M1 |
| lifecycle-viewmodel-ktx + lifecycle-runtime-ktx | MVVM/StateFlow collection | M1 |
| Room runtime + KSP processor + room-ktx | Local counters and queries | M3 |
| Preferences DataStore | Toggles/goals/preferences | M3 |
| Kotlin coroutines | Structured async work | M1 |
| Lottie for Android | Authored JSON animation files | M1/M2 |
| WorkManager | Opportunistic summary jobs; NOT reel polling | M6 |
| Django REST Framework / PostgreSQL / JWT on Render | Accounts and private challenges | M7 |
| Google Play Billing | Subscriptions and restore | M8 |
| JUnit, coroutines-test, AndroidX Test/Espresso | Automated checks | All phases |

Version policy: let Android Studio resolve compatible stable versions and record exact pins in `libs.versions.toml` or Gradle. No wildcard `+` dependencies. Update deliberately in a dedicated commit. Review current Android docs before using APIs that shift with Android releases.

## Build variants

- `debug`: logging without content data, demo seed/testing enabled only in an explicitly controlled mode.
- `release`: no mock tracker, no debug logging, R8 configured, signed with externally managed signing keys.

## Suggested command set

```bash
./gradlew :app:assembleDebug
./gradlew :app:testDebugUnitTest
./gradlew :app:lintDebug
./gradlew :app:connectedDebugAndroidTest  # device + tests available
```

Use `.\gradlew.bat` on Windows PowerShell. Commands presuppose the wrapper has been generated.

## Do not add by default

Unnecessary ad SDKs, general-purpose analytics trackers, scraping frameworks, root-level permissions, background timers for polling other apps, multiple dependency injection frameworks, or duplicate chart/animation libraries.
