# 12 — Final hardening, policy review and Play Console release

## Goal

Prepare an evidence-based Android release. If optional social/billing are omitted, remove/disable their UI and claims instead of blocking a safe MVP.

## Read first

- `docs/18_TEST_STRATEGY.md`
- `docs/19_DEVICE_AND_PLATFORM_MATRIX.md`
- `docs/20_RELEASE_AND_PLAY_STORE.md`
- `docs/12_PERMISSIONS_AND_COMPLIANCE.md`
- `docs/22_OFFICIAL_REFERENCES.md`

## Execute this task

1. Review every screen and claim against actual implemented/tested features. Remove placeholders, debug previews or clearly guard them in debug builds.
2. Run release build/AAB, Lint and tests. Audit permissions and min/target SDK against latest Play rules.
3. Complete real-device matrix and mark unsupported feed configurations transparently.
4. Validate disclosure and permission demonstration: install -> disclosure -> accept -> OS settings -> enabled -> usage; and decline/revocation case.
5. Draft/verify privacy policy, Play Data safety form, account deletion (if accounts), billing details (if billing). Do not submit made-up data to Play.
6. Check font/art/audio licensing, accessibility, low-end performance, battery and crash behavior.
7. Prepare store text and original screenshots; draft internal track test plan and staged rollout/rollback protocol.
8. Create a release checklist listing truly outstanding manual operations: signing, accounts, Console forms, upload.

## Tests and verification

- [ ] Release AAB built successfully OR explicitly not verified
- [ ] Permission/deletion/denial flows tested
- [ ] No unsupported exact-count or “unbreakable blocking” claims
- [ ] All assets legally sourced
- [ ] Play disclosures filled by real developer

## Acceptance gate

- [ ] All MVP acceptance gates satisfied
- [ ] Remaining manual actions explicitly listed
- [ ] Do not assert Play approval before it actually happens

## Stop condition

Do not proceed to the next milestone; give the exact next prompt path.


## Universal constraints

Read `AGENTS.md` first. The existing project is Kotlin + XML Views; never introduce Compose/Flutter. Inspect actual files before assuming paths exist. Make small compilable changes. Do not manufacture counts or tests. Update `PROJECT_STATUS.md`, `CHANGELOG.md` and, for major decisions, `DECISIONS.md` only after evidence. Use the required end-of-task report format.
