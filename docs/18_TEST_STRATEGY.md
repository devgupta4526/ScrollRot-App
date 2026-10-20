# 18 — Testing pyramid, QA and reliability gates

## Layer 1 — pure Kotlin unit tests

Detector state transitions, session resets, deduplication, timezone/day bucketing, goal percentage, pause and opt-in state reducer, rejection of unsupported feeds.

## Layer 2 — Room/DataStore/integration

Atomic increment exactly once; SharedPreferences import idempotent; schema migration; unexpected process death; zero vs unknown; export/delete; opt-out remains sticky; no raw text stored.

## Layer 3 — XML instrumentation

Navigation, first-run onboarding, explicit consent vs decline, Android Settings return, disabled/revoked states, dynamic type, TalkBack semantics, count from saved data, reduced motion, process recreation.

## Layer 4 — real-device social app validation

An emulator alone **cannot** demonstrate valid Instagram/YouTube/Facebook/Snapchat reel detection. Test against actual app packages and versions, record only safe synthetic labels, app version + device + OS in private test log; do not publish or store screen contents.

### Detector acceptance template

- 30 controlled new-item transitions in one feed → candidate accepted count close to observations within team-chosen tolerance, with **zero** increments for comments/chats/profile scrolling in the false-positive set.
- Multiple sessions, navigation backward, reload, ad insertions, fast swipes, split screen, lock/unlock.
- Threshold values must be decided before experiments and documented (not retrofitted to fit results).
- Any platform unable to meet criteria remains `Beta/Unsupported` and is excluded from marketing claims.

## Performance and power

Test low-end phone, continuous idle while service on, 1-hour day-in-the-life (with participant consent), event burst, animation overdraw, low battery, background restrictions, app process killed.

## Security and policy

Data safety worksheet; disclosure and opt-in video; negative permission path; privacy policy accuracy; Django API authentication/authorization integration tests; no secrets in repo; no content logs; app name/branding distinct.

## Pre-release stop conditions

Crashes during permission denial/revocation; false exact claims; repeated phantom increments; missing data deletion; permission misuse; silent data transmission; failing a11y controls; untested Billing account edge cases.
