# START HERE — exact development workflow

> Goal: get a trustworthy native Kotlin/XML version of Scrollrot running on a **physical Android phone** before attempting sophisticated features.

## A. Install and prepare

- [ ] Latest compatible stable Android Studio from https://developer.android.com/studio
- [ ] Android SDK Platform 36 + Build Tools; IDE-managed JDK 17 for the existing starter toolchain
- [ ] Git, a **private** repository, and a coding assistant that can inspect/modify files and run terminal commands
- [ ] Physical Android phone with Developer Options and USB or Wireless Debugging enabled
- [ ] Supported short-video apps installed and up to date **for testing only**
- [ ] Original/licensed assets only; no copyrighted BrainPal art or animations
- [ ] Optional later: Render and PostgreSQL accounts, Play Console account, Figma, LottieFiles

## B. Verify the existing Android starter

The prior source archive is **not yet verified as compiling** in this environment and may lack `gradlew`, `gradlew.bat`, `gradle-wrapper.jar` (it includes wrapper properties). Avoid telling the agent the build is already successful.

1. Extract `Scrollrot_Kotlin_XML_Starter.zip`.
2. Open in Android Studio; sync the Gradle files.
3. If Gradle wrapper executables are absent, create a new **Empty Views Activity** Kotlin project (`com.scrollrot.app`, min SDK 26), let Studio generate a wrapper, and merge the starter `app/src/main` sources/resources and matching Gradle settings. Never blindly overwrite a known-good wrapper.
4. Build via **Build > Make Project**. After wrapper creation, use:

   ```powershell
   # Windows PowerShell (run from project root)
   .\gradlew.bat :app:assembleDebug
   .\gradlew.bat :app:testDebugUnitTest
   ```

   ```bash
   # macOS/Linux
   ./gradlew :app:assembleDebug
   ./gradlew :app:testDebugUnitTest
   ```

5. Run on the real phone. Verify the home mascot and **Preview one reel (demo)**. Demo counters must not contaminate production counts.
6. Save baseline build output / screenshots, then `git add . && git commit -m "chore: baseline Android build"`.
7. Read `AGENTS.md` and `PROJECT_STATUS.md`, then execute [`prompts/00_AUDIT_AND_BUILD.md`](prompts/00_AUDIT_AND_BUILD.md).

## C. AI-agent routine for EVERY step

1. Give the agent the selected prompt and let it inspect the project.
2. Have the agent state the files it will touch; avoid unrelated refactoring.
3. Implement the smallest vertical slice: UI → ViewModel → Repository → real/fixture data → test.
4. Run `:app:assembleDebug`, unit tests, and relevant device checks.
5. Demand **actual evidence**: command exit status, test counts, device tested, known limitations.
6. Update `PROJECT_STATUS.md` and `CHANGELOG.md`, record architecture choices in `DECISIONS.md`.
7. Commit the working state; only then open the next prompt.

## D. Step-by-step first successful milestone

**Milestone 0:** Import → Gradle sync → compile → launch → confirm mascot animates → confirm demo is isolated → confirm app does not crash on denied tracking permission. Done means a passing debug build and recorded device result.

**Milestone 1:** Design tokens + navigation + three onboarding screens + non-coercive consent UX. Build and screenshot-test.

**Milestone 2:** Accessibility opt-in, state reporting, package filtering. Tracking enabled only after separate affirmative consent and user turning service on in Android Settings. Never auto-enable it.

**Milestone 3:** One validated Instagram Reels detector, then Room writes and UI reaction. **Do not proceed to more platforms until false-positive tests pass.**

**Milestone 4:** YouTube Shorts, Facebook Reels, Snapchat Spotlight added individually, each with explicit unsupported behavior.

**Milestone 5:** Local insights/goals/reduced-motion/export/delete.

**Milestone 6:** Opt-in notifications, focus sessions and optional non-obstructive floating counter.

**Milestone 7:** Django/Render authentication, friends, private group challenges, server-enforced permissions.

**Milestone 8:** Billing, Play compliance, internal testing, staged launch.

See the detailed gates and order in `docs/03_ROADMAP_AND_GATES.md` and `prompts/README.md`.

## E. Paste this as your very first agent instruction

```text
You are my senior native Android engineer. Build Scrollrot only in Kotlin + XML Views (not Compose). Read AGENTS.md, PROJECT_STATUS.md, START_HERE.md and docs/03_ROADMAP_AND_GATES.md. Then execute prompts/00_AUDIT_AND_BUILD.md. Audit the existing code and build it before changing behavior. If the build fails, fix the smallest cause and rerun. Do not invent test results. Report all changed files, commands and exit status. Update PROJECT_STATUS.md with only verified facts. Stop at the current milestone's acceptance gate.
```

## F. Stop rules

Never merge a milestone with a red build, an unverified claim of accurate reels, undisclosed accessibility usage, raw screen content stored in logs, real user data in fixtures, or a broken permission-denial path.
