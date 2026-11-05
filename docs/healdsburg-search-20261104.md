# Healdsburg winery tours: search-led landing-page revision

Status: validated locally; publication and live verification pending.

## Search evidence

Google Search Console, koastride.com domain property, Web search, exact page
`https://koastride.com/wine-tours/healdsburg`. Read in the signed-in report on
November 4, 2026. The 28-day chart explicitly covered October 6–November 2, 2026:
412 impressions, zero clicks, 0% CTR, average position 51.2.

| Displayed query | Clicks | Impressions | Average position |
|---|---:|---:|---:|
| healdsburg winery tours | 0 | 387 | 52.2 |
| healdsburg wine tours | 0 | 8 | 61.5 |
| healdsburg wine estate tours | 0 | 4 | 40.0 |
| wine tasting driver healdsburg | 0 | 1 | 16.0 |
| wine driver healdsburg | 0 | 1 | 24.0 |

The original recommendation compared October 27–November 2 with October 20–26:
387 impressions versus zero for the exact winery-tours query. This is evidence
of search exposure, not leads, bookings or market-wide search volume. Query
rows do not account for every page impression. Average position is not a fixed
rank. No post-change performance result is claimed.

The private baseline screenshot, report snapshot and generated-page hashes are
in the shared Koast audit folder `audits/2026-11-04-healdsburg-search/`; account
screenshots are not committed or deployed.

## Changes and intent

- Retain the existing URL and self-canonical. Lead the title and H1 with
  Healdsburg winery tours and clearly identify private chauffeured transportation.
- Help visitors choose among Dry Creek, Alexander and Russian River routes,
  distinguish estate appointments from downtown tasting rooms, and plan around
  the experiences they can actually reserve.
- Answer estate-visit, tasting-reservation, local pickup, San Francisco departure
  and group-vehicle questions. Keep tasting confirmation separate from the car
  reservation and make larger vehicles quote-only.
- Add one truthful Service entity linked to the existing Koast organization;
  keep FAQ structured data identical to the six visible answers and preserve
  breadcrumb identity. These support interpretation, not ranking or rich-result
  guarantees. No special AI files, training settings or security controls change.
- Replace this page's unsupported numeric capacity, fixed duration, firsthand
  experience and flexible tasting claims. Other regional pages remain unchanged.
- Reuse the existing marketing hero, booking card, cards, grids, FAQ and footer.
  No new CSS, imagery, booking integration, prices or provider policies.

## Primary factual references checked November 4, 2026

- [Official Healdsburg wine-country guide](https://stayhealdsburg.com/wine-country/):
  three nearby wine areas and downtown tasting rooms. Linked by the official
  Healdsburg Chamber site.
- [Dry Creek Valley winegrowers](https://www.drycreekvalley.org/dry-creek-valley/):
  regional context and Zinfandel focus.
- [Russian River Valley neighborhoods](https://russianrivervalley.org/about/neighborhoods/):
  regional context, Pinot Noir and Chardonnay.
- [Jordan visits](https://www.jordanwinery.com/visit/) and
  [visit FAQ](https://www.jordanwinery.com/visit-faq/): advance appointments.
- [Ridge Lytton Springs](https://www.ridgewine.com/visit/lytton-springs/):
  experience reservations and arrival guidance.
- [Dry Creek Vineyard visits](https://drycreekvineyard.com/visit/): reservations
  strongly encouraged and concierge contact for larger parties.

A separate read-only factual review found no material unsupported promises.

## Validation and boundaries

- Full generation and site check: 229 HTML pages, 43 blog posts, 10 dated
  editorial posts, no check errors. All 25 Node tests pass; tracker syntax passes.
- SHA-256 comparison against the same-main baseline: only
  `wine-tours/healdsburg.html` changed among the 229 generated pages.
- Built-in browser QA: desktop 1440×1000, phone 390×844 and narrow 320×844;
  no document overflow, native FAQ pointer and keyboard expansion/collapse work.
  The existing third-party booking widget retains its own narrow-screen inner
  scrollbar; its integration and checkout were not changed or submitted.
- D1 connector unavailable; signed-in Platform Sync Log open actions were
  checked. No active Healdsburg or website publisher conflict was visible.
  No shared database or customer/provider data changed.
- Care Rides remains excluded. No WAF/security/training permissions changed.
- Preserve this baseline for a like-for-like Search Console comparison after
  Google recrawls; do not evaluate the revision from same-day exposure.
