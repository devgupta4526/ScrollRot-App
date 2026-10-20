# 02 — Premium original XML UI, mascot and onboarding

## Goal

Create a highly polished original Scrollrot experience using XML, Canvas/Lottie/MotionLayout without copying competitor visuals. Do not invent finished Lottie JSON files.

## Read first

- `docs/06_UI_UX_SCREEN_SPECS.md`
- `docs/07_DESIGN_SYSTEM.md`
- `docs/08_ANIMATION_AND_ASSETS.md`
- `docs/21_ASSET_AND_LICENSE_CHECKLIST.md`

## Execute this task

1. Implement color, typography, dimensions and component styles in XML resources. Check contrast/touch target sizes.
2. Build 3 onboarding fragments/screens with Back/Skip/Next and a persistent completion flag; mark all example counters demo.
3. Build DashboardFragment hero counter, mascot container, goal ring, per-app card list and tracking-state banners; use actual repository state or truthful empty state.
4. Improve original Canvas mascot with idle/bounce/expression state animation; use Lottie assets only when valid licensed files exist; make static fallback.
5. Add MotionLayout transitions where they improve navigation or hero panels, keep motion subtle and lifecycle-aware.
6. Handle reduced motion/animator duration scale zero, 200% font, TalkBack descriptions and loading/empty/error screens.
7. Test low-end device smoothness and no infinite background animations.

## Tests and verification

- [ ] Build/unit tests pass and screenshot/visual inspection performed
- [ ] No placeholder animation JSON labeled final
- [ ] All content fits 360dp width at enlarged text
- [ ] Pause animations when offscreen and motion disabled
- [ ] No competitor branding or art

## Acceptance gate

- [ ] Onboarding navigable
- [ ] Dashboard renders honest states
- [ ] Mascot visual state corresponds to goals, not medical claims
- [ ] Animated UI is verifiably smooth on test device or gaps documented

## Stop condition

Do not proceed to the next milestone; give the exact next prompt path.


## Universal constraints

Read `AGENTS.md` first. The existing project is Kotlin + XML Views; never introduce Compose/Flutter. Inspect actual files before assuming paths exist. Make small compilable changes. Do not manufacture counts or tests. Update `PROJECT_STATUS.md`, `CHANGELOG.md` and, for major decisions, `DECISIONS.md` only after evidence. Use the required end-of-task report format.
