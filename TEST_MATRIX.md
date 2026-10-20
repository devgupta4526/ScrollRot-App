# Scrollrot Test Matrix

## Detector correctness

| Scenario | Expected behavior |
|---|---|
| Scroll regular Instagram feed | count must remain unchanged |
| Enter Instagram Reels without swipe | defined policy; don't randomly increment |
| Swipe to next Reel once | ideally +1 only if recognized high confidence |
| Scroll comments inside Reel | +0 |
| Swipe back to previous Reel | document count policy (new swipe vs unique video); should not double-count if dedup strategy prevents it |
| Two rapid swipes to new items | ideally +2 if evidence permits; don't collapse with hard cooldown |
| Stutter / bounce / fling settling | don't repeatedly count same transition |
| Switch from Instagram Reels to DM | stop counting |
| Watch a Reel without swiping | +0 swipe transitions, even if time increases |
| YouTube Shorts comments, scrub, likes | +0 |
| Facebook and Lite variant | version-specific verification |
| Snapchat chat vs Spotlight | chat +0; Spotlight only when recognized |
| No accessibility tree | no blind increase; unsupported/unknown state |
| Revoke accessibility permission | service stops, UI reports disabled |
| Pause tracking | count remains unchanged; user can resume |
| Locked screen / incoming call / system dialog | no overlay; no counts |

## Persistence/lifecycle

- Reboot, force-stop, process kill/restart, app update, permission disabled/re-enabled, Android's service reconnect.
- Night rollover and timezone change; DST boundary; settings goal changes.
- Three network states: offline, flaky network, online (social only).
- Data export, full deletion, account opt-out and post-deletion cloud access.

## Motion/accessibility

- 360dp/411dp/600dp widths, portrait and landscape, 200% font scale.
- TalkBack order, labels/roles, contrast, screen-reader count announcement without spamming.
- Android Reduce Motion / disabled animator duration; animation paused in background; 60 fps target where capable.
- No seizure-like flashes or motion that blocks primary action.

## Accuracy measurement template

For each combination of Android version/device/social app version/language:

```text
Platform:
Device/OEM:
Android SDK:
Social app version:
Language:
Total true next-video swipes manually counted:
True positives:
False positives:
False negatives:
Precision = TP / (TP + FP)
Recall = TP / (TP + FN)
Count difference = app accepted - actual
Battery overhead:
UI count latency p50/p95:
Notes / unsupported UI:
```

Do not publish a numeric accuracy claim until you have actual ground-truth test results from representative devices.

## Policy / release checklist

- [ ] AccessibilityService disclosure is prominent and separate from Terms/Privacy
- [ ] User explicitly opts in; consent version recorded
- [ ] Only selected apps examined; no watched content saved/uploaded
- [ ] Play Console accessibility permission declaration/demo video
- [ ] `isAccessibilityTool` truthful (`false` for general wellness app)
- [ ] Play Data safety and privacy policy reflect all analytics/social/Billing activity
- [ ] Data deletion and privacy controls remain functional without subscription
- [ ] Android 17 Advanced Protection unavailable state handled
- [ ] UI labels count as estimated if validation incomplete
- [ ] Accurate original asset licenses and screenshots
- [ ] Friends' data access locked by backend rules and tested
- [ ] Signed AAB/closed test, crash analytics opt-in and rollout monitoring
