# 08 — Motion design, animation state machine and asset inventory

## Asset manifest (planned — NOT included in this documentation pack)

| File name | Format | Trigger | Fallback |
|---|---|---|---|
| `assets/lottie/mascot_idle.json` | Lottie JSON | No change | Canvas breathing/bob |
| `mascot_happy.json` | JSON | Low relative daily progress | Smile/squash animator |
| `mascot_distracted.json` | JSON | Mid relative progress | Blink/wobble |
| `mascot_tired.json` | JSON | User over goal | Gentle slower bob |
| `mascot_rest.json` | JSON | Focus started | Calm idle pose |
| `confetti.json` | JSON | Goal reduction milestone only | Small scale pop |
| `streak.json` | JSON | Optional streak | Static badge |
| Original `ic_scrollrot.xml` | Vector | Launcher/splash | Existing icon if properly licensed |

All Lottie JSON assets must be independently drawn/licensed, exported and then added by the implementer. **Do not generate empty placeholder JSON pretending it's a finished animation.**

## Motion tokens

| Behavior | Duration | Easing / handling |
|---|---|---|
| Mascot idle bob | 2600ms loop | ease-in-out; 3–6dp translation; pause offscreen |
| Counter new accepted item | 240ms | 1.0 -> 1.1 -> 1.0 scale, spring-like |
| Progress ring change | 420ms | decelerate; animate actual persisted value |
| Mood transition | 450ms | crossfade + slight squash; no rapid flashing |
| Screen enter | 250–350ms | fade + 8dp translate; back reverses |
| Chart entrance | 350ms | stagger gently, no mandatory animation |
| Haptic | one light tap | Optional; respect user preference |

## State machine

`IDLE -> ENCOURAGED -> NOTICE -> REST_SUGGESTED` based on % of **user-selected** daily goal; the exact thresholds are initial UX parameters and should be configurable through a single policy object. Treat character moods as storytelling, **never as a medical brain-health metric**.

When motion is disabled, render a static pose immediately; no missing counters or delayed important content.

## Implementation rules

- Use `LottieAnimationView` inside XML (if animations are present) with a Canvas fallback from existing starter.
- For interactions between layout regions, MotionLayout belongs in an XML scene, not manually moving dozens of Views.
- Count increments must originate from repository emissions, not animation completion callbacks.
- Pause/stop/release animation references on fragment stop/destroyView to prevent leaks.
- Avoid unbounded loops in background and animation work while screen off.

## Quality gate

Record short on-device videos for idle, increment, mood switch, focus, permission denied, reduced motion, and 200% font; verify no layout jank or flashing. Assets must have license/source tracked by `docs/21_ASSET_AND_LICENSE_CHECKLIST.md`.
