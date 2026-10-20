# 09 — Navigation, state and error handling

## Main routes

```text
launch
  ├─ onboarding (if first launch)
  ├─ consent_information (optional after onboarding; never force OS grant)
  └─ dashboard
       ├─ insights
       ├─ focus_goals
       ├─ per_app_details
       ├─ settings
       └─ future: friends, challenges, premium
```

Use `Navigation Component` with one Activity, FragmentContainerView, ViewBinding. Keep bottom-nav destinations for Dashboard / Insights / Focus / Settings; friends may be a feature entry only after backend is ready.

## Required behavior matrix

| Input state | Dashboard behavior | Settings |
|---|---|---|
| First launch / no consent | Educational CTA; count area empty or real retained historical count labeled stale | Permission explanation, decline allowed |
| Consented but OS service off | ‘Turn on tracking’ CTA | Open system service Settings; verify on return |
| Active, not in supported feed | Show persisted daily count + “Waiting for supported feed” | Toggle and supported-app list |
| Active, feed recognized | Show accepted count, possibly confidence label | Pause button |
| User paused | Never process candidates; banner and resume button | Pause remains available |
| Service interrupted or revoked | Mark unavailable, preserve historical data | Re-enable explanation |
| Social app unsupported | Report unsupported, not zero recorded | Device/app version support help |
| Empty history | Show zero history only where known; no demo data | No hidden requests |

## Important distinctions

- `No observations yet` is not the same as `Confirmed zero`.
- Permission status is different from tracking paused preference.
- Consent is separate from Android service enabled state; store meaningful consent version and timestamp for auditing only if needed.
- Navigation back from Android Settings must actively re-check actual status; do not trust an intent return code to mean the service was enabled.
- UI tests should cover rotation/activity recreate/process death and deep-link behavior where supported.
