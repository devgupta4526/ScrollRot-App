# 06 — UI/UX screen-by-screen implementation specifications

Each screen requires portrait phone support (360dp wide baseline), landscape/tablet graceful layout, dynamic type, 48dp targets and accessible text. Provide XML layout IDs plus navigation route definitions. Never use actual competitor screenshots in product.

## A. Splash and onboarding (M1)

- Brand splash: original mark, simple 300–500ms animation (honor reduced motion), no artificial progress wait.
- Slide 1: “Notice your short-video habits”; original mascot + example count marked **demo**.
- Slide 2: “See patterns by app”; sample chart clearly not real data.
- Slide 3: “You stay in control”; why accessibility signals are used and that counts are estimates.
- Indicators, Back, Skip/Next; persist onboarding completion in DataStore.
- Separate consent screen before opening Accessibility Settings; never bundle with generic Terms acceptance.

## B. Dashboard (M1/M3)

- Header: name, settings icon, tracking status dot and help link.
- Hero: large formatted daily **estimated item exposures** count, context (“today”), count-up animation only for committed delta.
- Original mascot with 4–5 expressive states and motion fallback.
- Daily goal progress ring; if goal unavailable, explain default.
- Per-app cards: app category, count, confidence/unsupported chip, app share or relative contribution.
- Buttons: “View insights”, “Adjust goal”, and “Pause tracking”; no fake populated data.
- Offline/revoked/paused/unsupported and empty states fully designed.

## C. Insights (M5)

- Week tabs with local dates, animated bars/line with accessible numeric labels.
- Total, average per day, most-observed app; no medical-style harm scoring.
- Distinguish no data from 0. Show unavailable days and chart legend.
- Optional 30-day history; data follows timezone policy in `docs/11_DATA_MODEL.md`.

## D. Goals and Focus (M5/M6)

- Daily limit slider or numeric input; selectable warnings; presets are suggestions, not diagnosis.
- Focus timer start/pause/end, with practical reminder copy and clear “dismiss” options.
- Optional overlay toggle with explanation and system access route when needed.
- Never promise a truly irreversible lockout on consumer Android.

## E. Settings and Privacy (M2 onward)

- Tracking: permission state, opt-in, pause, platforms enabled, count accuracy explanation.
- Preferences: daily limit, animation/reduced motion, haptics, notifications.
- Data: export local aggregate counts, delete tracking history, request cloud-account deletion when signed in.
- Help: disclosure, privacy policy, policy FAQs, version and support email placeholder (**do not invent an address**).

## F. Social + Premium (P2)

- Private friends list, invites, group challenge screens, opt-in sharing and visible score-estimate label.
- Reporting/blocking users, leave groups and delete data.
- Clear price/renewal/restore handling; no dark patterns.

## Accessibility UI acceptance

TalkBack focus and labels, high contrast, large font (at least 200% system font testing), non-color-only statuses, scroll containers when content grows, proper focus return from system Settings.
