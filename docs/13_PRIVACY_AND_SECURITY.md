# 13 — Privacy, security, threat model and data deletion

## Data minimization policy

Store local **aggregated counts** and limited timestamps. A service may technically see sensitive UI information; immediately throw away everything not needed to decide a transition. No saved UI trees, captions, videos, usernames, message contents, URLs, screenshots or raw screen recordings. Never send raw accessibility-derived content to AI APIs or the Render backend.

## Threat model

| Risk | Mitigation |
|---|---|
| Accessibility reveals private UI content | Whitelist packages, minimal event types, discard sources, no content logs |
| Over-collection of device usage | No installed-app-wide scan, user-select platform toggles |
| False counts or gamified pressure | Estimated labels, detector validation, user controls |
| Cloud challenge reveals behavior | Opt-in only, aggregate scores, private membership rules, delete/leave |
| Account takeover / fake challenge membership | Verified Django JWT subject, database-backed server membership checks and invitation authorization |
| Token/session leakage | TLS, short-lived auth as supported, no secrets in logs |
| Malicious client inflates leaderboards | Treat client counts as self-reported, detect anomalies, no claim of anti-cheat certainty |
| Retention beyond expectation | Export/delete, retention policy, cloud deletion flow |

## Privacy requirements

- Local-first default; no sign-in needed for basic features.
- User consent is separate from OS permission; show data-sharing choices only when cloud features are actually available.
- Give users a simple **delete all tracking data** button with confirmation. Consider a scoped export action.
- Publish accurate privacy policy and Google Play Data safety form matching all SDKs used, crash/analytics SDKs and Render backend data flows if used.
- Avoid dark patterns and mandatory notifications.
- Review any optional crash/analytics SDKs and their collection disclosures before use; minimize logs and do not include accessibility event payloads.

## No-secret checklist

Never commit Django `SECRET_KEY`, `DATABASE_URL`, refresh tokens, signing keystore/private key, `.env`, OAuth client secret, production receipts/tokens or real event dumps. Never embed backend administrator credentials in the Android APK.

## Privacy policy outline (prepare before release)

Identity/controller; purpose; what accessibility can access; what is processed and stored; local/cloud boundaries; opt-in and revocation; data shared with infrastructure; retention/deletion/export; children's access restrictions as appropriate; user rights/contact; policy update date.

**Do not ship a placeholder privacy policy** or claim “no data collected” when opt-in API syncing or other actual data processing occurs.
