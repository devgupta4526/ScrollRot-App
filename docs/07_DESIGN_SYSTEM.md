# 07 — Original Scrollrot visual design system

**Style:** delightful midnight arcade meets calm digital wellness; visually premium yet nonjudgmental. **Do not copy BrainPal art or precise layout.**

## Color tokens (proposal)

| Token | HEX | Usage |
|---|---|---|
| `colorBg` | `#0D1020` | Main background |
| `colorSurface` | `#1B2035` | Cards |
| `colorSurfaceRaised` | `#292E49` | Dialogs/sheets |
| `colorLime` | `#B3FF72` | Positive progress, primary accent |
| `colorLilac` | `#917BFF` | Rest/recovery/secondary accent |
| `colorRose` | `#FF7FBD` | Expressive animation accents |
| `colorGold` | `#FFD262` | Caution/attention, not alarm |
| `colorText` | `#F9F8FC` | Primary text |
| `colorSubtext` | `#A5ACC6` | Secondary text |

Text contrast is **not guaranteed** by the above proposal; test actual foreground/background pairs using WCAG-appropriate standards. Provide separate accessible semantic danger/success colors, light theme if chosen, and avoid color-only meaning.

## Typography

- Use a commercially licensed rounded sans font (e.g., **Nunito Sans** under its current license) or Android system fallback.
- `HeroCounter`: 56–72sp bold, tabular digits if font supports; allow width-safe scaling.
- `Title`: 26–30sp; `Section`: 18–22sp; `Body`: 14–16sp; `Caption`: >=12sp for nonessential metadata.
- Dynamic type supported; avoid fixed-height text containers that clip.

## Layout tokens

- Base grid: 4dp; common spacing 8/12/16/24/32dp.
- Screen horizontal padding: 20–24dp; card radius 20–24dp; button radius 16dp.
- Minimum interactive target: 48x48dp; deliberate touch feedback and hit areas.
- Elevation used sparingly; cards separated with surface contrast.

## Reusable XML components

- `ScrollrotToolbar`, `HeroCounterView`, `RotCharacterView`, `GoalRingView`, `AppCountRow`, `StatusBanner`, `TrackingPermissionCard`, `EmptyStateView`, `PrimaryButton` style, `BottomNav`.
- All content strings in `strings.xml`, sizes in `dimens.xml`, colors in `colors.xml`; semantic `styles.xml` and theme overlays.

## Original mascot brief

Name: **Rotty** (working name). Abstract squishy comet/spiral creature, not a replica brain illustration. Two expressive eyes, swirling antenna, simple scalable silhouette, minimal strokes and cute reactions. Palette transitions should communicate friendly feedback, not medical harm.

## Accessibility and polish

- RTL mirroring where appropriate, TalkBack descriptions, non-motion state fallback and `animator_duration_scale = 0` handling.
- Skeleton/loading placeholders must not imply real counts; show meaningful messages.
- Do not use an unhealthy shame loop or compulsive reward mechanics to encourage excessive tracking.
