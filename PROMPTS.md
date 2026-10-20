# SCROLLROT — COPY/PASTE VIBE CODING PROMPT PACK

**Recommended tool:** Android Studio with a code agent (Gemini, Codex, Claude Code or other capable coding assistant). Work **one prompt at a time**, test on a real Android device before moving on. Supply `BUILD_SPEC.md`, the source files and screenshots of the current build to the agent; don't just ask for a BrainPal clone.

## MASTER SYSTEM PROMPT (paste once at the beginning of the coding session)

```text
You are my lead Android engineer, UI motion designer, and testing partner.
Build a polished original Android application called SCROLLROT with Kotlin and traditional XML Android Views only — NO Jetpack Compose, NO Flutter, NO React Native, NO WebViews for the native UI. Package com.scrollrot.app, Android 8+ minSdk 26.

Project objective: A privacy-first, gamified short-form scroll tracker with a live counter, a unique animated blob mascot, daily/weekly breakdown, user-configured limits, optional opt-in overlay, and future friend battles and subscription features.

Read BUILD_SPEC.md, README.md and TEST_MATRIX.md fully before coding. Preserve the original brand tokens, screens, user flows, privacy and animation brief. Do not copy BrainPal artwork, layout pixels, copywriting or other proprietary assets.

Non-negotiable technical rules:
1. MVVM, ViewBinding, Kotlin Coroutines/Flow, Room for count history, DataStore for settings. Use Fragments/Activity + XML layouts with Material Components/ConstraintLayout. Keep logic modular, testable and well named.
2. An AccessibilityService may observe configured app events only after prominent separate disclosure and user opt-in. It may inspect minimal accessibility signals but MUST NOT persist/upload raw UI text, captions, messages, video contents, identifiers or screenshots.
3. Do not claim Accessibility TYPE_VIEW_SCROLLED equals exactly one reel. Implement per-platform detectors with explicit screen classification, event deduplication, state transitions, confidence levels and validation test scenarios. Identify unsupported versions instead of silently generating counts.
4. Build real functionality. No fake server responses, hard-coded friend standings that look real, placeholder analytics presented as user data, fake exact detection, mock paywall advertised as active, or fake promises of unbreakable blocking.
5. Create original delightful animations: character idle breathing/bob/blink, count pop, smooth goal ring, chart transitions, mascot mood changes and reduced-motion fallback. Use Canvas/Lottie/ValueAnimator/MotionLayout as appropriate.
6. Respect user autonomy: optional tracking pause, data deletion, consent state, manual permission revocation. Don't use accessibility to obstruct permission screens, system settings, or uninstall.
7. Every implementation step must compile. Give actual paths and full changed source code. Don't leave broken XML references, missing resources, TODO-crashes or silently skipped Gradle issues.
8. Before each large change: explain goal, files to modify and tests. After changes: provide what compiles, manual test procedure, limitations and next work. Do not pretend you ran builds/tests that were not run.
9. Prefer stable AndroidX/toolchain releases compatible with the project and Android Studio. Avoid adding unnecessary permissions or dependencies.
10. UI must adapt to 360dp phone, 400dp phone, large fonts, TalkBack, landscape/tablet; avoid clipping and inaccessible micro-animations.

Work in small vertical slices. Start by inspecting the existing code and implementing requested phase, not rewriting the entire project without preserving working behavior.
```

## PROMPT 01 — Establish architecture and import source

```text
Audit this Scrollrot Android Studio Kotlin/XML starter. Read BUILD_SPEC.md. Fix all Gradle sync / build issues. Establish clean architecture: single-activity/fragments, ViewBinding, MVVM, repository interfaces, pure domain models, Room and DataStore. Preserve existing working screen and animation. Show changed file tree and explain migration. Add one small unit test and one basic UI smoke test. Do not implement network/billing yet.
```

## PROMPT 02 — Premium original onboarding

```text
Build three original onboarding XML screens for Scrollrot: welcome story, live-count demo, and permission education. Use ConstraintLayout, tasteful dark ink + neon lime/violet/pink identity, accessible typography and truly original mascot visual. Provide progress dots, continue/back/skip where appropriate, soft enter transitions, and a separate prominent AccessibilityService disclosure with explicit consent action. DO NOT ask for Accessibility before disclosure. Preserve Settings return and verify permission enabled, not just intent fired. Deliver complete XML, Kotlin, strings, and navigation.
```

## PROMPT 03 — Production reel detector design & Instagram first

```text
Implement a robust tracking architecture with PlatformDetector interface, ScreenClassifier, Debouncer, Deduplicator, bounded inspection, confidence enum, reason codes and testable event snapshots. Start with Instagram only. Scope service package filter. Identify Reels view via version-specific UI signals without storing content. Ignore normal feed, comments, profile and chat scrolls. Debounce burst events; verify possible item changes and label low confidence unsupported cases. Supply a synthetic test suite and a real-device validation checklist. Clearly communicate detection is estimated until validated. No screenshot/MediaProjection.
```

## PROMPT 04 — YouTube Shorts + Facebook + Snapchat

```text
Add independent YouTube Shorts, Facebook Reels/Facebook Lite, and Snapchat Spotlight adapters. Keep each detector in its own Kotlin class, feature flags with allow/deny app versions, and gracefully mark unsupported interfaces. Reuse the tested detection state machine. Include tests: first video, next video, swipe back, bouncing, comments, scrub, app switching, horizontal swipes, screen off. Do not create generic TYPE_VIEW_SCROLLED = count++ code.
```

## PROMPT 05 — A wow-worthy Scrollrot mascot

```text
Turn Scrollrot's original mascot into a full motion system using Lottie (for authored vector art) + native Canvas/ObjectAnimator where needed. States: energized, distracted, overloaded, resting. Original lumpy blob with spiral forehead; do not reproduce competitors' brain character. Implement idle bob/breathing, blink, count reaction, 4-state transitions, progress halo, touch reactions, reduced-motion setting, animation pause on background and minimum resource footprint. Give usable animation asset brief if original JSON files cannot be created correctly; never pretend missing Lottie files exist.
```

## PROMPT 06 — Animated XML home dashboard

```text
Rebuild the dashboard with premium native XML visuals: animated numeric reel count, mascot in spotlight card, 24h daily goal arc, per-platform icon rows, streak, 'you reclaimed time' only if measurable, permission/unsupported warnings, and friendly limits. Use MotionLayout transitions and custom views as needed. 60fps animations. No Compose. Support 360dp width, large fonts, dark mode and TalkBack. Show full screen XML/Kotlin/resources and run UI tests.
```

## PROMPT 07 — Room + histories + insights

```text
Implement Room entities/DAOs with migration tests, local date/timezone handling, daily/weekly/monthly history, real per-platform counts, and a reliable transaction-based increment. Add DataStore settings. Build stats UI in XML with an original animated 7-day Canvas bar chart, app breakdown, goal completion and empty states. Add optional CSV export via Storage Access Framework and delete-all-data flow. Never mix demo previews with recorded counts.
```

## PROMPT 08 — Floating mini counter overlay

```text
Design an opt-in draggable 50dp-or-greater mini floating counter chip using WindowManager TYPE_ACCESSIBILITY_OVERLAY owned by the active accessibility service. No broad SYSTEM_ALERT_WINDOW permission unless demonstrably required for a separate justified design. Show only on a known supported short-feed screen after user opt-in; remove on pause, permission revoked, app switch, unsupported screen and lock screen. Respect secure screens, tap targets and interaction safety; user may hide/disable it. Add tests for window leaks and service restart.
```

## PROMPT 09 — Focus goals and gentle intervention

```text
Add goal settings, no-shame reminders and an optional break timer with WorkManager/notifications as appropriate. Then prototype an explicitly opt-in limit-triggered intervention restricted to known short-form content screens. Explain OS limits and Play policy risks before attempting control over a third-party UI. Do not trap the user, block system settings, spoof access or promise non-bypassable blocking. Test cancellation, revocation, overlays, reboot and unsupported UI.
```

## PROMPT 10 — Real opt-in friend and group battles

```text
Implement Django REST Framework, PostgreSQL and JWT authentication deployed on Render for opt-in Scrollrot battles. Data model: users, requests, accepted friendships, battles, participants, scores. Accept invite by code, 1v1/group battle (2–8), start/end timezone rules, live score, ties, notifications, self-deletion. Use DRF object permissions, server-side ownership checks + Django integration tests to ensure only eligible members read the battle and users cannot change other users' scores. Synchronize only aggregate daily counts after explicit sharing consent, never raw accessible screen content. Offline UX included.
```

## PROMPT 11 — Play Billing and transparent premium

```text
Add Google Play Billing for optional premium features: custom limits, advanced insights, themes. Implement real product fetching, loading states, pending/canceled purchase, verification on secure backend, restore purchase, subscription management URL and refund/expiry handling. Never fake price/entitlement. Keep permission revocation, tracking off and delete-data accessible without paying. Build XML paywall with clear monthly/annual prices from Play response, no dark patterns.
```

## PROMPT 12 — Security, QA, launch readiness

```text
Perform final audit: Kotlin/XML compilation, lint, runtime permission flows, Android 8–17 behavior, service reliability and battery, Accessibility disclosure and user consent, Play Console declaration/demo-video instructions, Data safety, privacy policy accuracy, content descriptions, large fonts, reduced motion, Django API permission and token tests, Billing restore and offline behavior. Generate reproducible manual tests and an AAB release checklist. Do not claim verified accuracy or production readiness without executed tests and actual measured results.
```

## When the AI agent breaks something: focused recovery prompt

```text
Do not add features. Diagnose the exact supplied Gradle/build/runtime error. State the root cause and fix the smallest possible set of files. Output full changed file content and the run/test commands. Keep the project strictly Kotlin/XML, preserve privacy/permission flow and existing working features. If the error cannot be reproduced here, say so clearly and request the concrete stack trace rather than inventing a solution.
```

## Motion asset-generation prompt for a visual artist/animation specialist

```text
Design an original, friendly digital wellbeing mascot for Scrollrot: soft lumpy glowing spiral blob, pear-shaped body, small feet, enormous expressive eyes, no resemblance to a recognizable brain emoji or competitor IP. Base lime #B3FF72, ink #0D1020, alternate colors amber/pink/violet. Produce a layered editable vector and a Lottie animation plan with loops (2.6 second float and blink), 400ms swipe reaction, and clean stage transitions. Safe, playful, never implying literal brain damage; transparent background; every animation usable at 180–240dp in Android views, crisp at xhdpi and supports reduced motion.
```
