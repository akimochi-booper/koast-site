# Account lifecycle policy — synchronized release review

Status: owner-approved policy package, as confirmed by the integrating agent on 2026-10-25. Ready for synchronized Site/Book deployment by the integrating owner; this lane does not deploy. Approval is not a legal-compliance certification.

## Proposed customer choices

- **Deactivate with 90-day recovery:** immediately disable passenger access and end existing sessions; retain the account data needed for recovery for up to90days; explicit verified restoration before the displayed deadline; proceed to permanent deletion after90days without restoration. Deactivation is not completed deletion.
- **Request permanent deletion now:** bypass the optional recovery hold; verify identity, disable access and process account-associated data deletion, with visible status and completion notification. Keep only limited records necessary for lawful service/payment obligations, legal/tax duties, fraud prevention or legal claims. Do not promise all purge tasks complete instantly.
- Neither choice cancels a booked ride, requests a refund or erases a balance. Handle those via the existing reservation and payment workflow. Privacy requests must not be blocked solely because a lawful limited record needs retention.

## Draft locations

`generate.py` adds Terms section9 (account security/closure) and Privacy sections account-deletion and security/signed-in sessions. Final provisions move from9 to10. Privacy has a direct public anchor and deletion-request mailto path so people can initiate a request outside the app. Generated terms.html/privacy.html are ignored build outputs.

The source contains a synchronization comment. Publish with the matching passenger Security release, not independently before that behavior is available.

## Implementation facts to verify before publication

1. Deactivation blocks all passenger authentication methods, does not auto-restore on ordinary sign-in, ends sessions, and prevents stale provider/guest links from granting access.
2. A displayed90day deadline is persisted. Explicit restoration verifies existing account ownership, works only before the deadline, revokes old sessions, and cannot restore already purged data.
3. Deactivated accounts stop calendar syncing and marketing. Restoration does not silently reconnect removed provider authorizations or create new consent.
4. A real scheduled/retryable purge executes after the window and permanent-deletion requests bypass it. Partial failures cannot report completed deletion.
5. Permanent deletion inventories all account-linked data (including linked passenger/preferences, saved places, messages/reviews/content where applicable, calendar tokens/events, payment-provider records, attachments, session metadata and reset challenges). Legal exceptions require a category/purpose/retention schedule. Do not silently retain everything as a blanket business-purpose exception.
6. Request and completion messages match actual outcomes. The external email channel has an operational owner, identity-verification process, tracked status and legally appropriate response deadlines.
7. Sessions are presented as browser sessions, not guaranteed physical devices. Old/incomplete metadata is honestly labeled. Session revocation does not claim to erase cached local content or Google sign-in.
8. Confirm service-provider deletion/revocation work, backup handling and retained financial records before making those claims live.

## Official guidance reviewed on2026-10-24

- Apple: https://developer.apple.com/help/app-review/guideline-reference/5-1-1-account-deletion — in-app initiation, complete account deletion rather than deactivation alone; reasonable processing time with disclosure; identity verification allowed but no unnecessary obstacles. Non-highly-regulated apps generally cannot require support/email to complete the in-app flow.
- Google: https://support.google.com/googleplay/android-developer/answer/13327111?hl=en — in-app and external web request paths, associated user-data deletion, service-provider deletion requests, disclosed lawful retention and reasonably quick processing.
- Google User Data policy: https://support.google.com/googleplay/android-developer/answer/18258653?hl=en — temporary deactivation, disabling or freezing does not qualify as account deletion.
- California AG: https://oag.ca.gov/privacy/ccpa — covered-business deletion requests generally require a response within45days, with an additional45days only as permitted and notified. A product recovery feature does not automatically justify a90day legal response delay. Applicability and exceptions require owner/legal review.
- Current California regulations/statute compilation: https://cppa.ca.gov/regulations/pdf/ccpa_statute_eff_20260101.pdf — verification, timing and deletion/deidentification requirements. No claim made that Krujim currently meets CCPA applicability thresholds.

## Validation

- python -m py_compile generate.py: passed.
- python generate.py: passed; existing Care Rides exclusion untouched.
- node --test test/acquisition.test.mjs test/performance.test.mjs:16 passed.
- git diff --check: passed.
- Generated legal-page anchor uniqueness, public account-deletion anchor, Terms normalized /privacy crosslink and deletion-request mailto verified. Initial link assertion expected source .html form; corrected after inspecting generated canonical links.
- No browser visual QA, public deployment, legal approval, live deletion or sensitive transmission performed by this policy lane.

## Existing policy wording outside this change

The inherited Privacy Policy includes broad device/contact/marketing collection language. This change does not verify all those existing practices; review the complete policy against the actual app data inventory before store submission. The new narrow session description does not validate unrelated inherited claims.


## Integration review — 2026-10-25

- Rebased onto Site origin/main `0eadddb` (Restore website fleet images after scope clarification); no conflicts. Latest fleet-image source and assets remain untouched by the policy diff.
- Source behavior cross-checked in Book `54a2e0d66df7da34e4b4593104c931571b3cab6e`, modules `src/customer-security.js` and `src/customer-account-data.js`: closure is action-approved; access and sessions end immediately; recoverable mode persists a 90-day deadline; permanent mode starts processing without that hold; ordinary sign-in does not restore; explicit verified restoration leaves old passwords/sessions invalid; calendar authorizations are disconnected rather than silently reinstated.
- Added the restoration password disclosure to match implementation and updated the legal-page dates to October25. No new layout or styling.
- Purge is asynchronous and may require review/provider work. Copy continues to describe processing/status and lawful limited retention rather than promise instantaneous completed erasure. Phone-only completion communication still requires the operational support path; no claim that automatic SMS security notices exist.
- The external email request channel and retained-record review remain operational obligations of the release owner. This policy lane does not mark provider deletion, legal retention schedules or public production behavior verified.
- Prior parent-run desktop/phone policy preview may be reused because this integration changes text only, preserving layout and styling. This lane does not independently repeat or claim that browser QA.
