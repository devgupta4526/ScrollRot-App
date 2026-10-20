# 20 — Play Store release preparation and checklist

## Before release

- [ ] Proper package ID, original app name/logo/description/screenshots, no copied BrainPal assets.
- [ ] Tested release build/AAB, R8/shrinker, signing key managed securely.
- [ ] Target API meets current Play requirement (API 36+ for new mobile apps as of October 2026), verify again on launch.
- [ ] Android accessibility prominent disclosure, affirmative consent, accurate `isAccessibilityTool=false`, Play Console Accessibility declaration, explanatory demo video.
- [ ] Accurate Data safety questionnaire and website privacy policy including all actual SDK behaviors.
- [ ] All permissions used for declared features only; notification/overlay separately consented as implemented.
- [ ] Content rating, target audience, app access/testing instructions, support contact, store listing claims audited.
- [ ] Basic offline and permission-denied usage, tracking pause, all-data delete working.
- [ ] Tests on real phone and specific social-app versions, and transparent wording about estimate quality.
- [ ] If billing: Play Billing integration, in-app purchase listing, restore/entitlement/server checks tested.
- [ ] If accounts: user account deletion in app and web path as required by Play; privacy policy updated.

## Suggested rollout

1. Internal test track with small team and evidence log.
2. Closed beta across varied Android versions; collect **anonymous, non-content** error diagnostics if explicitly disclosed.
3. Fix crashes, failed detectors, inappropriate overlays and battery regressions.
4. Staged production rollout, monitor permitted crash reports and opt-in feedback.
5. Roll back or disable detectors when platform UI changes cause false counts.

## Store copy rules

Use “estimates short-video item transitions on supported versions” rather than “tracks every reel perfectly.” Do not claim cured addiction, clinically validated brain effects, or irreversible blocking. Original brand only.

## Source of truth

- Target SDK: https://support.google.com/googleplay/android-developer/answer/11926878
- Accessibility declaration: https://support.google.com/googleplay/android-developer/answer/10964491
- Play data safety: https://support.google.com/googleplay/android-developer/answer/10787469
- Billing: https://developer.android.com/google/play/billing/integrate
