# Palo Alto and Healdsburg landing-page improvements

Owner explicitly requested implementation, checks and publication after passing on November13,2026. This changes two existing landing pages and two contextual inbound links; no new URL, pricing, booking integration, tracking or provider setting.

## Search baseline and intent

Authenticated Search Console Web, exact pages, October14–November10,2026, read November13. Private screenshots/report text remain in shared `audits/2026-11-13-social-preview-seo/local-landings/`, outside deployed source.

| Page/query | Impressions | Clicks | Average position |
|---|---:|---:|---:|
| Palo Alto page |481|0|12.7|
| sjc to palo alto car service |93|0|6.4|
| sfo to palo alto car service |76|0|5.4|
| palo alto car service |28|0|18.0|
| palo alto chauffeur service |27|0|8.3|
| palo alto to sfo chauffeur service |27|0|10.7|
| executive car service palo alto |24|0|9.5|
| Healdsburg page |418|0|51.3|
| healdsburg winery tours |387|0|52.2|
| healdsburg wine tours |13|0|62.4|
| healdsburg wine estate tours |5|0|38.0|
| wine tasting driver healdsburg |3|0|17.0|
| wine driver healdsburg |2|0|22.5|

Positions are aggregates, not guaranteed fixed rankings. Palo Alto's airport queries support a clearer SFO/SJC title and practical pickup brief; Healdsburg's driver queries support a clearer commercial driver/quote path. Its broad winery-tour query remains low-ranking. These are improvement hypotheses, not evidence of post-release search growth.

## Implementation

- `src/palo_alto_car_service.py` is pure authored markup with existing booking markup/quote URL passed in. The generator composes existing nav, fleet, FAQ, related links, CTA and footer at `/cities/palo-alto`. SFO/SJC and return-trip planning, exact Stanford/office entrances, nearby Menlo Park/Sand Hill Road and transfer-versus-hourly needs replace the generic city body. No fixed travel-time promise or invented Palo Alto business address. Service schema expresses area served only; six visible/schema-matching FAQs.
- `healdsburg_wine_tours.py` retains its renderer interface and six FAQs. Title/hero now state private-driver intent, with existing email quote buttons and route/checklist anchors. Adds practical exact tasting-address/driver-window guidance and contextual winery links. Existing separate tasting/transport reservations and larger-vehicle quote boundaries remain. An old unsupported Ridge late-arrival assertion was removed after source review.
- Inbound contextual links: the existing SiliconValley airport-choice guide links its Palo Alto sentence to the landing page; the Sonoma related-planning area links to Healdsburg driver/route planning. The guide's original publication and current November13modification dates remain correct. Existing thumbnail selection is preserved.
- Existing marketing hero/cards/grids/buttons/type and orange-gradient tokens are reused. No new stylesheet, artwork, page-redesign system, fleet availability claim, form, service price, payment terms or provider action.
- The new Python source lives under already-excluded `src/`; production generation adds no dependency and deployment does not expose the new source file.

## Factual references reviewed

- [Stanford airport transportation](https://transportation.stanford.edu/getting-around-bay/transportation-airports) and [official visitor information](https://visit.stanford.edu/): used as direct planning resources. No transfer-minute guarantee, campus-access permission or institutional affiliation is implied.
- Current [Healdsburg wine-country guide](https://stayhealdsburg.com/wine-country/), [Ridge Lytton Springs visits](https://www.ridgewine.com/visit/lytton-springs/), [Dry Creek Vineyard visits](https://drycreekvineyard.com/visit/) and [Jordan visits](https://www.jordanwinery.com/visit/): source/confirmation-address planning and reservation guidance. No prices, numeric group limits or guaranteed stop counts added.
- Koast's existing service/airport/route pages own its public offerings; copy does not create a new service or change accepted booking terms. Vans/Sprinters/buses remain quote-only.

## Verification contract

`node scripts/check-pr.mjs` retains all installed checks, including `test/palo-alto-car-service.test.mjs`, `test/healdsburg-wine-tours.test.mjs` and current sharing-image tests. Assert one indexable canonical/H1/service identity, honest local area, visible/schema FAQ equality, real quote/route destinations and contextual inbound links. Baseline generated-output comparison should change only Palo Alto, Healdsburg, Sonoma and the airport-choice guide. Test actual desktop/390/320 layout, anchors, native FAQ keyboard interaction and quote destinations without submitting a booking/email. Integrate fresh main, exact hosted green, D1 publisher coordination, protected Git/Pages and live verification before recording complete.

After Google recrawls, compare the same exact pages/queries and equivalent complete periods. A same-day check cannot establish improved rankings, clicks or bookings. No extra recurring automation is installed by this change.
