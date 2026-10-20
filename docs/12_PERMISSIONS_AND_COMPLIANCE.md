# 12 — Android permissions and Google Play compliance

This file is an implementation checklist, not legal advice or a guarantee of approval. Revalidate official Google Play policies before release.

## Accessibility (core, user-opted)

- Manifest: register a service derived from `AccessibilityService`; `android.permission.BIND_ACCESSIBILITY_SERVICE` applies to the **service declaration** and is bound by Android, not a normal runtime permission dialog.
- Service metadata file in `res/xml/` declares only needed event types/package filters, feedback and capabilities. Avoid `typeAllMask` if narrower event types suffice; retrieve window content only when the detector truly needs it.
- `isAccessibilityTool=false` for a general digital-wellbeing reel tracker; do not falsely claim disability access.
- Normal app flow must show a **standalone in-app prominent disclosure**, explaining types of data accessible, what is accessed/used/shared, and precise feature purpose. Require affirmative consent; offer a decline path. Only after opt-in direct the user to Android Settings to enable the service manually.
- A privacy-policy link does NOT substitute for the separate disclosure. If usage expands to overlays/intervention/cloud sharing, update disclosures truthfully.
- Provide pause, re-enable instructions and response to service revocation. Never turn on access via hidden behavior.
- Submit Play Console declaration and a demonstration video for the feature and disclosure flow.

### Suggested consent copy (must be truthful to implemented behavior)

> Scrollrot uses Android Accessibility access only when you choose to enable it. It may observe interface and scrolling changes inside supported short-video screens in Instagram, YouTube, Facebook and Snapchat. Accessibility access can expose screen information. Scrollrot uses limited on-device signals to estimate changes between short-video items; it does not intentionally collect or save messages, video content, captions or screenshots. Tracking counts are stored on this phone unless you separately opt into a future sync feature. You can pause tracking in Scrollrot or disable access in Android Settings. These counts are estimates and may be unavailable for some app versions.

UI actions: **Not now** | **I agree — open Android settings**. Save explicit choice appropriately. If the implementation accesses anything beyond this, revise the copy and policy before release.

## Optional special access

| Feature | Permission/path | Rule |
|---|---|---|
| Duration stats | `PACKAGE_USAGE_STATS` + manually granted Usage Access | Does NOT count reels; disclose separately |
| Notifications | `POST_NOTIFICATIONS` runtime on API 33+ | Request when enabling reminder, not launch |
| Outside-app overlay | `SYSTEM_ALERT_WINDOW` + user Settings grant for `TYPE_APPLICATION_OVERLAY` | Only if necessary; avoid obstructive overlays; separate consent |
| Accessibility-service overlay | `TYPE_ACCESSIBILITY_OVERLAY` where appropriate | Scope to user-enabled service and policy; not a bypass of disclosure |
| Network | `INTERNET` when Render API/Billing integration is implemented | No secret uploads |
| Package discovery | narrow `<queries>` if needed | No broad installed-app inventory |

Do not request SMS, contacts, background location, camera, microphone, media/screen recording, storage or `QUERY_ALL_PACKAGES` for the base product.

## Focus/blocking boundaries

Accessibility must not be used to secretly automate or manipulate other app UIs, change settings without authorization, stop service deactivation/uninstallation, or misrepresent impossible guarantees. Use voluntary reminders and minimally intrusive intervention, and get policy review before any stronger blocking behavior.

## Official sources

- https://support.google.com/googleplay/android-developer/answer/10964491
- https://support.google.com/googleplay/android-developer/answer/16558241
- https://developer.android.com/guide/topics/ui/accessibility/views/service
- https://support.google.com/googleplay/android-developer/answer/11926878
