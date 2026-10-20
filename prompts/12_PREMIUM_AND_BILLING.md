# 11 — Google Play subscription purchase, verify and restore

## Goal

Implement subscriptions only when genuine paid features exist. Use Play Billing, server-side verification and transparent entitlements.

## Read first

- `docs/17_BILLING_AND_PREMIUM.md`
- `docs/20_RELEASE_AND_PLAY_STORE.md`
- `docs/13_PRIVACY_AND_SECURITY.md`

## Execute this task

1. Confirm Play Console test products/plans and current Billing Library release using official docs; record pinned version.
2. Implement pricing/product detail retrieval, XML premium screen, complete billing terms and cancel/help links.
3. Implement `BillingClient` lifecycle, purchase callback, pending state, reconnect/retry and acknowledgement with the correct current APIs.
4. Integrate trusted backend verification of purchases/entitlements; never trust plain local premium booleans.
5. Implement restore purchase and account changes, grace, hold, cancel and expiry semantics.
6. Keep basic counting and data deletion available to unpaid users.
7. Run Google Play license-tester flows or explicitly mark billing unverified.

## Tests and verification

- [ ] License-tested purchases work
- [ ] Restore works after reinstall/account switch as appropriate
- [ ] Server controls entitlement
- [ ] Cancelled-but-active/grace/on-hold treated correctly
- [ ] No deceptive trial/renewal claims

## Acceptance gate

- [ ] No billing “production-ready” statement without license tests
- [ ] Screens show prices from Play responses
- [ ] Secrets absent from client

## Stop condition

Do not proceed to the next milestone; give the exact next prompt path.


## Universal constraints

Read `AGENTS.md` first. The existing project is Kotlin + XML Views; never introduce Compose/Flutter. Inspect actual files before assuming paths exist. Make small compilable changes. Do not manufacture counts or tests. Update `PROJECT_STATUS.md`, `CHANGELOG.md` and, for major decisions, `DECISIONS.md` only after evidence. Use the required end-of-task report format.
