# 17 — Optional subscriptions, restore and entitlement logic

**Not part of MVP.** Build only after basic tracking is useful and stable. Keep core tracking and data deletion accessible without payment.

## Suggested premium differentiation (proposal)

- Free: real estimates, daily count, one goal, last 7 days, privacy controls.
- Premium: richer history, visual customizations, advanced voluntary focus tools and larger private groups — feature set must be truthful and actually implemented.

## Billing implementation

- Google Play Billing Library; consult current official instructions rather than hardcoding an outdated version. As checked October 2026, official docs show Billing Library `9.1.0`, but re-check during integration.
- Products/plans configured in Play Console; backend receipt/purchase-token validation before granting durable entitlements.
- Confirm purchase, acknowledge within Play requirements, handle renewal/cancellation/grace/hold/paused/expired states, restore purchases and account mismatch.
- Respect Play family/payment disclosure policies as applicable and local consumer rules; no hidden auto-renewal wording.
- App must not trust client `isPremium=true` as a durable entitlement.

## Subscription screens

Clear amount/currency, billing interval, renewal terms, what unlocks, links to Terms/Privacy, cancellation instructions and a visible `Restore purchases` action.

## Test matrix

License tester purchase, cancel during active period, renew, payment hold, offline entitlement recovery, refund, account switch, repeat purchase, app reinstall, and server failure. Use Play Console test purchases, not fabricated successful transactions.

Official: https://developer.android.com/google/play/billing/integrate
