# Wine-day discovery and manual quote handoff

Status: **Experimental / local draft**, November16,2026. Eugene requested coordination between the public website and `Design Wine Tour Homepage Features`. The existing Cinema, Journal and Gallery compositions stay distinct. These additions are suggestions for enquiry, not approved sellable package inventory. No publication or Booker cutover is authorized by this contract.

## One content owner

`src/wine_days.py` → `WINE_DAY_IDEAS` is the canonical current preview catalogue. `ideas_for_region` and `render_wine_days` use the same entries on Home, the wine-tour overview and regional pages. Home's initial view gives Napa/SUV, Sonoma/Sprinter and Livermore/bus equal prominence; All regions includes all nine entries. Explicit region buttons filter every card. Healdsburg currently uses the Sonoma ideas; it is not a separately validated itinerary.

Stable IDs combine region (`napa-valley`, `sonoma`, `livermore`) with one of `private-suv-day`, `executive-sprinter-day`, `group-bus-day`. These nine identifiers name exploratory ideas, not purchasable SKUs or price/vehicle entitlements. The default requested vehicle can be changed without changing the underlying idea reference.

Each definition owns ID, region slug/name, title, short summary, default/requestable vehicle labels, image/alt/provenance, exclusions, `state=exploratory`, `price_state=team_quote`, `duration_hours=null`, `stops=[]`, `itinerary_verified=false`. Never interpret null as a free price or a promised duration. No current rate, seat count, confirmed tasting, partner agreement, admissions, lunch or actual assigned vehicle is supplied. Vans, Sprinters and buses stay quote-only.

The existing12-region `WINE_REGIONS`/`WINERIES` content in `data.py`/`generate.py` is an editorial browsing catalogue. Its presence is not proof of transportation availability, coverage, price, drive time or package inventory. Nearby/state browsing can use known region identity with a manual override; device location requires the visitor's explicit action/permission. Site currently makes no geolocation request.

## Current customer action

`marketing-design.js` owns the single manual flow. Selecting an authored card retains its ID/title/region/default vehicle in memory. Pickup/date/party are reviewed with a changeable requested vehicle and optional winery/return notes. Edit and Clear day idea preserve the visitor's other draft fields. Both party and requested-vehicle choices use the existing scoped Compact picker.

Final action is **Open email draft**. `buildWineQuoteEmail` URL-encodes the chosen idea, requested vehicle, pickup, date, party and custom notes. The visitor sends through their own email app; there is no automatic send, submitted/success claim, live pricing, availability lookup, payment or reservation. No form values enter persistence or analytics. Unknown idea IDs fall back to the generic request; they do not create a product or provider action.

The current authorized Moovs new-request and rider-account URLs remain distinct and functional. `Booking Wizard` confirmed that its replacement is local/synthetic, with no approved new public cutover destination or package import contract. Never point a public CTA at the temporary owner-QA tunnel, guess query parameters, or activate an app/provider route from this merchandising work.

## App handoff and verification

Website owns this source catalogue and renderer; the Passenger chat owns its separate local app adapter and design exploration. Generate the schemaVersion1 read-only JSON handoff with `python -m src.wine_days`; `preview_catalogue` owns the interface. The shared mockup evidence JSON is derived from this catalogue, not a second authored source. Future approved inventory/pricing, import API or live Booker handoff requires its own explicit owner contract. No customer profile/payment records are created by this preview.

`wine-days.js` owns region filtering and manual carousel paging; `wine-controls.js` owns Compact choices; `test/wine-days.test.mjs` covers catalogue states, IDs, region filtering, intent/email retention, ordinary homepage booking precedence and the unchanged online-booking fallback. Actual desktop/phone checks cover selected-card context, notes/vehicle edits, filtering and focus.

November16 image correction: Eugene requested wine-country-led discovery, with no generic fleet product pictures in the winery area. All nine wine-day cards now use distinct fictional vineyard, terrace, cellar or winery-space scenes, reserved from the existing hero, winery-card and transport image assignments. Vehicle classes remain text choices. The same image and descriptive image_alt fields are exported for Passenger; named-estate identity, tasting inclusions and real photography are not implied. Dedicated fleet presentation and the three approved page compositions stay intact.

November16 section-order revision: regional winery discovery precedes suggested wine days. This changes Site composition only; canonical idea IDs, images, catalogue export and manual quote behavior remain unchanged.
