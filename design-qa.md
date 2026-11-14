# Public marketing design QA — November 14, 2026

final result: passed

Local candidate only; the redesign is not published. This report supersedes the earlier adaptation report after Eugene rejected the visual drift and explicitly requested that each original mockup remain its own complete design. Approved scope is the public marketing website, excluding booking, Passenger, Driver and operations apps.

## Visual truth and comparison

Exact targets in the shared Koast folder, `mockups/livermore-visual-directions/2026-11-14/`:

- `option-1-vineyard-cinema.png`, 946×1663: transparent navigation, sunset hero, white/gradient headline, floating pickup/date/party quote bar, cream discovery cards, scenic SUV conversion band and three planning disclosures.
- `option-2-wine-journal.png`, 973×1616: cream navigation, large stacked black display type, italic serif accents, portrait vineyard with overlapping wine image, horizontal winery rows and full-width scenic conversion band.
- `option-3-afterglow-gallery.png`, 973×1616: charcoal navigation/gallery, three-line white/gradient hero, journey steps, square winery images and cream pickup/party planner.

Opened each original beside the final browser rendering in `implementation/final-{cinema,journal,gallery}-comparison.jpg`. Sources are on the left, implementation on the right. Comparisons retain native pixel dimensions; browser CSS viewports961/988 produce screenshot content widths946/973 respectively after scrollbar/capture area. Final full-page and hero screenshots use the same filename prefix. Comparisons use the initial closed-disclosure state. The production footer and preserved SEO/planning material extend below the concept composition rather than replacing it.

The original mockups are desktop references. Responsive implementation was also opened at390px and320px; physical-device acceptance is not claimed. Final mobile screenshots and `final-browser-metrics.json` are alongside the comparison boards. Preview remains at http://127.0.0.1:59399.

## Findings corrected

- P1: flat orange headline and inherited cream navigation changed Cinema's character. Restored clipped orange gradient, transparent dark header and bright vineyard palette; matched header/hero geometry.
- P1: original pickup/date/party quote bar was absent. Added real inputs, validation, a review dialog and an explicit email-draft handoff. All entered values survive into the draft. Existing online booking remains available.
- P2: the first implementation blended the concepts. Added three independent compositions, not one shared visual wrapper. Journal restores oversized stacked typography, serif text and overlapping photography; Gallery restores dark cards, journey steps and cream planner.
- P2: reused imagery did not fill the reference roles. Generated and inspected six separate people-free atmosphere assets directly against the original references; exported whole compositions for their measured slots. Original wordmark remains unchanged. Real Tabler3.20.0 icons and MIT license are included.
- P2: card/badge padding and conversion-band height shifted Cinema's section rhythm. Reduced those dimensions and recaptured the combined comparison. Journal lede/photo overlap was corrected before final capture.
- P1 regression caught by existing Stag's Leap test: replacing the conversion band hid the existing transportation-quote link. Restored the original explicit action below the reference composition; the unmodified Stag's Leap action assertion now passes.
- P2 content mapping: individual Livermore wineries initially inherited the region's first winery. Corrected the context key so each estate leads its own page, followed by two nearby wineries. Browser checked Wente and Stag's Leap. The later owner navigation correction replaces the current estate's official-site link with an on-page About action.

No actionable P0/P1/P2 issue remains in the checked states. Remaining P3 differences: exact generated photo subjects/crops, outline icon glyphs and minor type metrics. These do not require another fidelity loop. Verified estate photography can replace illustrative ambience when appropriately sourced.

## Five fidelity surfaces

- Typography: retained self-hosted Plus Jakarta Sans, matched large bold display scale, separate serif Journal accents and natural phone wrapping. Inputs remain at least16px.
- Layout: separate complete compositions, matched navigation/hero/discovery proportions, correct photo frames, overlapping Journal images and distinct quote placement. Practical details remain available through disclosures.
- Color: gradient headline and CTAs, Cinema's warm cream, Journal's pale editorial background and Gallery's charcoal/cream split. Forced-color fallback, focus rings and reduced-motion behavior are retained.
- Imagery: original SVG logo, six measured new raster exports and existing scenic vehicle/hero masters. Fictional ambience is described in alt text; it does not claim to depict a named estate or assigned vehicle. No generated people added.
- Content: winery locations and reservation/walk-in guidance, internal winery guides, separate tasting fees, quote-only group vehicles, established metadata/schema/FAQ and related planning links. No invented rates, capacities, reviews or performance statistics.

## Functional and technical checks

- Installed full validation after navigation correction: `node scripts/check-pr.mjs --today 2026-11-14`;187tests passed, zero failures/skips;236HTML pages,47posts,16dated editorial posts; zero generated-site errors. Full output is `implementation/internal-winery-checks.log`. Existing fidelity output remains in `implementation/fidelity-final-checks.log`. Required gate names and assertions remain intact.
- Quote browser checks: Cinema pickup/date/4guests, Journal pickup/date/7+group and Gallery pickup/5guests. Reviews and encoded email drafts contain entered values; Gallery shows date as “To be confirmed.” No email draft was sent and no production booking created.
- The quote planner does not persist or transmit input, call a backend, calculate a fare or confirm availability. The visitor explicitly opens and sends an email draft. Existing native booking URL is preserved; no unsupported provider prefill is claimed. Local booking iframe remains the repository's synthetic preview fixture.
- Escape closes quote review and returns focus to the invoking control. Mobile menu opens, Escape closes it and focus returns to Open menu. Form errors use a live status and focus the invalid input. Native keyboard date/select semantics are preserved.
- Three final matching-width desktop renders: no horizontal overflow. Lazy images inside closed supplemental disclosures are unrequested rather than broken. Ten additional final mobile observations cover Livermore, Healdsburg, Napa, Stag's Leap and Wente at390/320px with no overflow or broken eager images. Earlier unchanged route-family smoke checks remain applicable to the broader candidate.
- Existing canonical, schema/visible-FAQ equality, sitemap, acquisition/privacy, prelaunch and Care Rides gates pass. Preview comparisons are noindex/nofollow and outside the sitemap.
- Final browser warning/error readback empty in checked states. No native desktop input used. D1 coordination was read through the authenticated Cloudflare console; no Site publisher claimed for this local candidate.

## Owner navigation correction — verified

All winery/region/design-preview exploration links stay on Koast. Removed external winery links from the three main card compositions, every estate facts panel and supplemental Livermore/Healdsburg/Stag's Leap copy. Source/provenance research remains available in developer documentation. Existing booking/account handoffs and email actions retain their established transactional behavior; this is not a provider migration.

Browser verified Livermore's Explore winery → Wente's Koast page → About this winery → expanded details → on-page Plan my ride → native quote inputs, with Close returning to the invoking control. Concannon's About action also opens its details at320px without overflow. No email/provider submission. Screenshot `implementation/internal-winery-details.jpg` shows the on-site details and new ride action; final warning/error readback empty. Original three layouts, colors and images unchanged. A complete generated wine-page navigation guard checks external destinations and current-estate About anchors; generated-site checks catch missing internal destinations.187tests and236page checks pass.
