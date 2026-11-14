# Stag's Leap and Sacramento search landing pages

Eugene authorized exact-page query review, improvements, checks and publication after passing on November13,2026. Pure static content/metadata change; existing URLs, quote destinations and booking-card ownership remain. No tracking, provider, price or data change. Shared private baseline/screenshots/release evidence: `audits/2026-11-13-social-preview-seo/stags-sacramento/` in the canonical Koast documents.

## Query evidence and interpretation

Authenticated Search Console, `sc-domain:koastride.com`, Web, all countries/devices, exact page URLs, October14–November10,2026, read November13. Stag's Leap:275 impressions,0clicks,average position10.0; all10 exposed query rows reviewed. Sacramento:261 impressions,0clicks,average47.2; all21 exposed query rows reviewed. Query totals can omit anonymized rows and need not equal page totals.

| Exact-page query | Impressions | Clicks | Average position |
|---|---:|---:|---:|
| are there small-group tours available in stags leap? |97|0|8.5|
| stags leap winery tasting reservation |3|0|48.7|
| stags leap wine cellars |2|0|77.5|
| google maps the westin verasa napa to stag's leap wine cellars distance drive time |1|0|5.0|
| stags leap winery tour |1|0|36.0|
| black car service sacramento |85|0|41.5|
| sacramento black car service |32|0|42.6|
| sacramento car service |32|0|59.4|
| private car service sacramento |29|0|58.2|
| rideshare sacramento |17|0|61.1|
| car service sacramento |15|0|49.7|
| black truck service sacramento |3|0|11.7|

Stag's Leap should explain small private-party transportation and separate it from winery-hosted tasting experiences, not invent a join-in tour or available tasting slot. Correctly identify Wine Cellars versus the distinct Stags' Leap Winery. Exact hotel/estate addresses and a confirmed return/service window answer practical intent without fixed drive-time promises.

Sacramento should lead with black car/private chauffeur service; SMF is a useful existing use case, not the dominant observed query. Useful airport/hotel, Capitol/business, event and regional-route briefs replace generic city promises. Self-drive truck-rental and rideshare queries are not a reason to claim those products. Low average positions mean content/title work is a hypothesis, not a guaranteed click fix.

## Contract and design

`src/sacramento_car_service.py` and `src/stags_leap_transport.py` export metadata/FAQ constants and a pure body renderer with injected existing `booking_markup` and escaped `quote_url`. `generate.py` composes existing nav/fleet where appropriate, FAQs, related planning, CTA, footer and schema. Existing marketing `.hero-dark`, `.hero-grid`, `.card`, grids, buttons, typography and gradient tokens are reused; no CSS, imagery or design-system departure. Section anchors clear the fixed nav. Sacramento Service areaServed names the city/CA, not a fabricated local office. Stag's Leap describes Koast transportation rather than winery ownership or affiliation.

Contextual inbound planning links come from Napa Valley, which already links both the winery and Sacramento. Existing article publication/modification dates and all thumbnail assets remain unchanged. Expected generated content scope: Sacramento, Stag's Leap Wine Cellars and Napa Valley only, before integration of any independent newer main changes.

Vans/Sprinters/buses remain quote-only. Actual seating/luggage/access needs, stops/waiting/return window and separate tasting confirmation stay explicit. No new fixed service time, price, stop count, tasting capacity, booking availability or campus/venue/airport access promise.

## Official references

- [SMF official FAQ](https://flysmf.gov/about/faq): current airport/terminal planning resource. No numbered chauffeur curb or permit claim added; current flight/terminal instructions must be confirmed for the trip.
- [Golden1 Center official directions](https://www.golden1center.com/visit/directions-and-parking/): event access planning resource. Its main address does not guarantee a loading location. No event schedule, parking price, pickup-zone or availability claim added.
- Winery-specific official visit/experience/address references are recorded in the Stag's Leap module's source notes and the shared release review after independent research. Do not copy historical tasting prices/capacities into transportation copy.

## Validation and measurement

Owning generated-output tests enforce one indexable canonical/H1/Service, visible/schema FAQ equality, genuine quote/planning destinations, distinct winery identity and transport/quote boundaries. Installed `node scripts/check-pr.mjs` plus generated comparison, independent review, desktop/390px/320px anchor/quote/FAQ checks and exact hosted candidate validation precede protected Git publication. D1 publisher/readback, successful Pages build, matching served content/schema and live visuals are required for completion.

After recrawl, compare the same exact pages and relevant queries across equivalent complete periods. No same-day ranking, click or booking improvement claim; no new recurring automation.
