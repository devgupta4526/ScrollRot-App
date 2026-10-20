# AGENTS.md — non-negotiable rules for coding assistants

You are working on **Scrollrot**, an original digital-wellbeing Android application. Follow this file before any prompt or user story. If instructions conflict, prioritize user safety, platform policy, verified behavior, and these engineering constraints; identify the conflict.

## Scope and stack

- **ONLY native Android Kotlin + XML Views.** Do not introduce Jetpack Compose, Flutter, React Native, or a webview UI without a separate product decision.
- Package/application ID: `com.scrollrot.app` unless owner directs a change.
- Support min SDK 26; initial target/compile SDK 36. Keep Gradle/Kotlin/AGP versions compatible with an actual local build; do not upgrade casually.
- Single Activity + Fragments, AndroidX Navigation, ViewBinding, ViewModel + StateFlow, repository pattern, Room, DataStore. Add Hilt only when complexity warrants it.
- Local-first and offline-functional. The Render-hosted Django API and Play Billing are **future optional integrations**. No Django/Render SDKs/services.
- Use Material Components/XML, ConstraintLayout, RecyclerView, MotionLayout, Lottie JSON, Android Canvas/ObjectAnimator when appropriate.
- Use **original** mascot, palette, screen hierarchy, voice, and animations. Competitor app is functional inspiration, not an asset source.

## Engineering discipline

1. Inspect current project/code/version catalog before editing. Never claim a file or dependency exists without checking.
2. Break every prompt into small, independently compilable changes. Preserve existing working functionality.
3. Implement every UI state: loading, empty, permission denied, disabled, service interrupted, tracking unsupported, success, error.
4. Make money/network/social layers behind interfaces; keep the MVP able to build without credentials.
5. **Never fake analytics/reel counts** in production. Demo preview must be clearly labeled and isolated from persistent totals.
6. **Do not claim one scroll event equals one reel.** Detector produces candidates; validate, deduplicate, attach confidence and support metadata.
7. Never scan all apps or collect content unnecessarily. Filter allowed packages immediately and minimize UI-node reads.
8. No screen captures, captions, message text, video titles, URLs, entire accessibility trees, or personally identifiable content in permanent storage/logs/telemetry.
9. Do not bypass consent, auto-enable accessibility, conceal indicators, prevent uninstall/revocation, abuse foreground services, or overstate blocking guarantees.
10. Permission refusals must leave the rest of the app usable. Pause toggles must stop processing even if the OS service remains enabled.
11. Follow dynamic type, content descriptions, 48dp touch targets, dark/light contrast, screen readers, reduced motion.
12. Include unit tests and relevant instrumentation/manual tests for each behavior. Never invent successful test output.
13. All network/backend access must follow least privilege and auth/security rules; never trust client-submitted scores as verified competition results.
14. Never commit passwords, private signing material, Django/Render backend secrets, PII, device event logs or raw accessibility output.
15. Explain libraries added, the reason, and their compatibility. Prefer stable maintained AndroidX/Google packages.

## Required end-of-task response format

```markdown
## What changed
- ...
## Files changed
- path — why
## Build / tests actually executed
- command; exit status; unit/instrumented/manual result
## Manual validation required
- exact device + app version scenarios
## Known limitations / policy risks
- ...
## Next milestone
- one recommended next prompt
```

If the coding agent cannot execute Gradle or access an Android phone, it must say **NOT VERIFIED** and list manual commands; never say a build passed.

## Agent state files

Update `PROJECT_STATUS.md` only for evidence-based progress; record substantial tradeoffs in `DECISIONS.md`; append human-readable changes to `CHANGELOG.md`. Never silently mark aspirational features complete.
