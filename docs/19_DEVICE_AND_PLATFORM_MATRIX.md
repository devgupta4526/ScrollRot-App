# 19 — Device and platform coverage matrix

Record each tested configuration. A claim of 'supports Instagram' must name tested version(s) or qualify as experimental.

## Matrix columns

| Tested date | Android / OEM | Social app / version | Feed path | Ground truth transitions | Accepted | False positives | False negatives | Outcome |
|---|---|---|---|---:|---:|---:|---:|---|
| _example only — not tested_ | — | Instagram Reels / — | — | — | — | — | — | UNTESTED |

Never replace `UNTESTED` with invented values.

## Minimum phone test spread

- Android 8–10 representative device where possible, Android 11–13, Android 14–16 and latest supported OS; at least one Samsung device and one Pixel/stock Android device, plus a low-end phone.
- Test dynamic text sizes, dark mode, reduced motion, accessibility services already enabled, battery saver, gesture navigation, screen off, switching apps, uninstall and permission revocation.
- Check OEM background behavior without instructing users to compromise device security.

## Per-platform checklist

**Instagram Reels:** Home feed vs Reels tab, comments, share menu, profile, explore, first item, navigation.

**YouTube Shorts:** Shorts tab vs standard videos, comments, search and ads.

**Facebook Reels:** Reels viewer vs home posts/videos/comments; Facebook Lite only if separately tested.

**Snapchat Spotlight:** Spotlight vs camera/chat/stories; do not assume uniform UI accessibility.

Track app versions per test; platform UI may change remotely even without an app update, so keep a rollback/feature-disable switch in future releases.

## Release labels

`Supported with known limitations`, `Experimental / estimates`, `Unsupported` should be chosen per app/version and tied to evidence. Leave unknown configurations unknown.
