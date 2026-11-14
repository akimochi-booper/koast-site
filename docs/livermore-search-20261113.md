# Livermore wine-tour search improvements

Eugene explicitly authorized query review, page updates, checks and publication after passing on November13,2026. The deployment target reuses Site marketing hero/cards/grids/buttons/type/gradient; no CSS or imagery change, new shared standard, provider/tracking or booking-destination change. Shared private query/visual/release evidence is in canonical Koast documents `audits/2026-11-13-social-preview-seo/livermore/`.

## Search baseline and decision

Authenticated Search Console `sc-domain:koastride.com`, exact `/wine-tours/livermore`, Web, all countries/devices, October14–November10,2026, read November13.182impressions,0clicks,average position61.8. All10 exposed query rows reviewed; anonymized queries can make query sums differ from page totals.

| Query | Impressions | Clicks | Average position |
|---|---:|---:|---:|
| livermore wine tours |50|0|62.9|
| livermore valley wine tours |33|0|48.0|
| livermore wine tasting tour |24|0|77.6|
| wine tours livermore |20|0|62.1|
| livermore wine tasting tours |20|0|68.1|
| livermore wine tour |14|0|66.1|
| wine tour livermore |11|0|54.0|
| wine train livermore |2|0|48.0|
| livermore wine trolley |1|0|51.0|
| livermore wine trolley tours |1|0|60.0|

Broad wine-tour intent supports a clear Livermore Valley title, private chauffeur offer, useful local stops, pickup/return and tasting-reservation planning. Low aggregate/query positions mean this is content work rather than a proven title-only CTR fix. Minor trolley/train queries do not justify advertising those products; clarify that Koast transportation is a private ride for the party. No immediate ranking, click or booking gains claimed.

## Owning contract

`src/livermore_wine_tours.py` exports title/description/six FAQs and `render_livermore_body(booking_markup, quote_url)`: pure authored body, trusted existing booking slot, escaped existing quote URL, no import-time/network/customer effects. Scoped `generate.py` wine-region branch composes existing nav/FAQ/related links/footer and truthful regional transport Service. Existing clean URL, canonical, thumbnail and article dates retained. A SanJose related-link label provides a more descriptive existing inbound path; expected generated differences before unrelated main integration: Livermore and SanJose only.

The body uses curated official planning links rather than reproducing legacy winery-list claims. Wente, Concannon and Murrieta's Well are examples to compare, not a fixed itinerary, affiliate package, included tasting or available booking. Larger vehicles remain quote-only. Winery party rules are separate from vehicle seating; tasting confirmation separate from transport; no fixed visit count/drive time, admission, meal, accessibility or space promise.

## Official research

- [Livermore Valley Wine Community itinerary planner](https://www.lvwine.org/itinerary-planner.php) and [maps](https://www.lvwine.org/maps.php): start from an address/select/reorder winery stops; supports route planning without a fixed visit count.
- [Wente visit/FAQ](https://wentevineyards.com/visit/) and [current address](https://wentevineyards.com/contact-us/):5050ArroyoRoad; seated tasting reservations encouraged, not a blanket requirement. Avoid using an older TeslaRoad address or assuming its former restaurant is still the same offering.
- [Concannon experiences](https://concannon.wine/experiences/) and [address](https://concannon.wine/contact-us/):4590TeslaRoad; reservations encouraged, walk-ins depend on seating; larger parties ask the winery. Experience/food/age rules vary; no broad family/picnic promise.
- [Murrieta's Well visit](https://murrietaswell.com/visit/):3005MinesRoad; seated tasting reservations recommended, patio/walk-up format differs. Date-specific openings/holiday exceptions make a current-date check preferable to hardcoded opening days.

Independent official research checked November13. Preserve winery ownership of current experience details, requirements and availability. No tasting prices, numeric party limits or schedules copied. Individual winery guide pages are outside this change; current official destinations are linked directly.

## Validation and measurement

`test/livermore-wine-tours.test.mjs` checks one canonical/H1/Service, matching six visible/schema FAQs, real official/quote/planning destinations, truthful reservation/transport boundaries, source-slot/URL escaping and contextual inbound link. Installed `node scripts/check-pr.mjs`, generated comparison, independent review and desktop/390/320 anchor/FAQ/quote checks precede current-main exact hosted validation. D1 claim/readbacks, protected Git/Pages, served content/schema and live visuals are required for completion. Compare equivalent complete query/page periods after recrawl, not same-day ranking movement. No recurring automation added.
