# Public website renewal imagery — November 14, 2026

Scope: the public marketing website, using Eugene's selected vineyard-cinema and wine-journal directions. This inventory records image meaning and reuse limits; it is not release or live-verification evidence. Existing files remain preserved. The coordinating publisher owns optimized exports, final URL mappings and rendered crop checks.

## Existing geographic assets

The following are current repository names and `generate.py` mappings, not a new verification of photographer, licensing, exact viewpoint or documentary location. Do not infer a named estate from regional artwork. Existing provenance, where recorded, remains in `docs/image-provenance.md`, `docs/social-preview-20261113.md` and `docs/fleet-imagery-2026-10-24.md`.

| Existing asset or family | Current geographic meaning | Reuse limit |
|---|---|---|
| `img/wy-<winery-slug>.jpg` | Optional named-winery image convention used by the generator | No `wy-*.jpg` files were present in the inspected candidate. Do not manufacture a path or label generic art as an estate photograph. |
| `img/blog-banner-napa.jpg` | `WINE_IMG['napa-valley']` | Visually inspected: vineyard rows, hills, a winding lane and a dark SUV. Use regional/scenic descriptions, without identifying the pictured estate or vehicle. Stag's Leap uses this existing regional fallback. |
| `img/blog-banner-sonoma.jpg` | Sonoma regional mapping | Regional artwork; not proof of any named Sonoma winery. |
| `img/wt-healdsburg.jpg` | Healdsburg regional mapping | Healdsburg wine-country context, not an estate identity claim. |
| `img/wt-livermore.jpg` | Livermore regional mapping | Livermore context; do not reuse as Napa, Sonoma or a named Livermore estate photo. |
| `img/wt-paso-robles.jpg`, `img/wt-santa-ynez.jpg` | Paso Robles and Santa Ynez mappings | Retain the corresponding California region. |
| `img/blog-banner-temecula.jpg`, `img/blog-banner-willamette.jpg` | Temecula and Willamette Valley mappings | Keep separate; northern California scenery does not document Oregon or southern California. |
| `img/wt-walla-walla.jpg`, `img/wt-finger-lakes.jpg`, `img/wt-texas-hill-country.jpg`, `img/wt-virginia.jpg` | Corresponding named regional mappings | Do not replace these with generic northern California art while claiming the pictured place is local. |
| `img/city-palo-alto.jpg`, `img/city-sacramento.jpg` | Palo Alto and Sacramento | Keep city-specific context on the corresponding pages; filenames alone do not newly verify exact landmarks. |
| Other `img/city-<slug>.jpg` files | Corresponding city mappings, where used by `CITY_IMG` | Preserve city-to-asset mapping; avoid presenting one skyline as another city. |

## Existing fleet assets

`fleet-sedan`, `fleet-business-suv`, `fleet-first-class-suv`, `fleet-sprinter`, `fleet-mid-party-bus` and `fleet-large-party-bus` have existing JPG and/or `-cut.webp` artwork. These class images do not establish the actual vehicle assigned to a booking, its model year, equipment, seating or availability. Keep published specifications and quote-only handling for vans, Sprinters and buses independent of imagery.

The retained `fleet-sedan-hotel-scene.webp`, `fleet-business-suv-airport-scene.webp`, `fleet-first-class-suv-coast-scene.webp`, `fleet-sprinter-wine-tour-scene.webp`, `fleet-mid-party-bus-events-scene.webp` and `fleet-large-party-bus-events-scene.webp` are generated editorial scenes. Their earlier website adoption was explicitly withdrawn in `docs/fleet-imagery-2026-10-24.md`; the accepted fleet cards returned to cutouts. Do not treat those scene files as documentary photographs or silently replace the accepted fleet presentation. The new public-site renewal may use approved editorial imagery in its own scope, with honest alt and no fleet-identity claim.

## New generated editorial masters

Built-in image generation produced these standalone original PNGs for the selected design direction. They are retained in the shared documents at `mockups/livermore-visual-directions/2026-11-14/assets/`, outside the deployed image directory. All three were visually inspected. They depict generic imagined northern California ambience, with no people, text, logos or identifiable estate. They are not photographs documenting a winery, Koast service, assigned vehicle or actual fleet.

| Shared master | Actual size / bytes | Intended meaning and suitable alt |
|---|---|---|
| `vineyard-hero.png` | 1536 × 1024 / 2,343,207 | Golden-hour vineyard rows and rolling hills under oak branches. Generic northern California editorial hero; alt: “Vineyard rows and rolling hills in golden evening light.” |
| `wine-terrace.png` | 1254 × 1254 / 2,440,223 | Two wine glasses on a terrace table, flowers and vineyard views. Generic discovery-card ambience; alt: “Wine glasses and flowers on a terrace overlooking vineyard rows.” No named estate or advertised tasting format is depicted. |
| `wine-ride-scene.png` | 1942 × 809 / 2,985,124 | Unbranded black SUV on a vineyard lane under oak shade. Editorial transport conversion band; alt: “Black SUV on a vineyard lane in evening light.” It proves no make, model, equipment, capacity, actual service or availability. |

SHA-256 master fingerprints:

- `vineyard-hero.png`: `AA69C795C93C60E856D756E46FCBAA1E2CFB77D2C62CE01AD29AB7F22EE15D18`
- `wine-terrace.png`: `F6A96FF9CAEBA747FFC2CA3FC5AA87AB7FC990368670FC1761ED054C52270B70`
- `wine-ride-scene.png`: `6F4F6C2E803345E5B4795BFE24EBEABE53B68D2658C4C6A72B9ECFA873376F2A`

Resize/compress copies for deployment while retaining these masters. Record the actual export dimensions, format and URLs with integration evidence. Never upscale a small thumbnail into an estate claim, embed a full mockup as page UI, or stretch panoramic artwork. Check mobile crops for the intended subject and keep image dimensions explicit. Named winery cards should convey confirmed visit guidance in text and link the official source; imagery does not verify walk-in availability, reservation policy or current opening hours.

Integration exports: whole compositions encoded to JPEG quality88 using System.Drawing (no crop/resize). `img/renewal-vineyard-hero.jpg`1536×1024,345783bytes; `img/renewal-wine-terrace.jpg`1254×1254,366858bytes; `img/renewal-wine-ride.jpg`1942×809,478570bytes. Responsive presentation uses CSSobject-fit with original dimensions supplied by enhancement. Current Nov14 owner authorization permits varied editorial van/bus/scenic imagery in the public-site renewal; existing fleet-card cutouts and their published specs remain unchanged. No generated people in the three new masters.

Palo Alto people-free edit: `palo-alto-people-free.png`,1774×887,3316715bytes, SHA256439A11E876E55DEC49FD5D2539B9D6E68C811E8EC7EE1B0A9BDF36D0E4FB8FD6. Built-in ImageGen edited the exact existing city-palo-alto.jpg: remove all people/cyclists/bicycles, reconstruct pavement naturally, retain the architecture, trees and warm evening composition, no added people/vehicles/signage/text/brands. Original generated source exec-1c03c8e5-540d-46f2-953f-f4534dc01fbf.png. Inspected and exported whole composition to `img/city-palo-alto-renewal-v1.jpg`, JPEGquality88,590086bytes. This remains illustrative city artwork, not a newly verified documentary location. Updated Palo Alto hero/city-carousel and mapped destination/social thumbnails; prior asset retained.

Six new fictional ambience masters were generated directly from the corresponding original mockups after owner requested closer fidelity: cinema-card-one/two/three (1254×1254), journal-vineyard (1086×1448), journal-grapes (1774×887), gallery-oak-lane (1254×1254). No people, readable text/logos or identifiable estate. Shared originals remain in the approved mockup asset folder. Whole compositions exported with high-quality bicubic scaling and JPEGquality85: `img/reference-cinema-card-{one,two,three}.jpg`760×760; journal-vineyard840×1120; journal-grapes760×380; gallery-oak-lane760×760. These are atmosphere, not documentary photographs of the named card wineries. Original regional imagery and previous masters remain retained.

November16 distinct-scene additions: built-in ImageGen generated four separate1536×1024 PNG masters, each visually inspected with no visible people, legible text, plates or watermarks. Fictional regional ambience, never documentary estate images or assigned-fleet claims. Shared masters: `mockups/livermore-visual-directions/2026-11-14/assets/20261116/`.

| Master | Export | Scene / original generated source |
|---|---|---|
| tasting-room-oak-interior-master.png | img/wine-tasting-room-oak.jpg | Fictional oak-counter tasting room, barrels, cream plaster and soft vineyard daylight; exec-d9896bdc-b0e1-4c45-9837-ebc2a23a2808.png |
| garden-courtyard-fountain-master.png | img/wine-garden-courtyard.jpg | Fictional garden with low limestone fountain, white flowers and pergola; exec-e22fe5c7-cd3c-497e-a092-8aaa785202a9.png |
| vineyard-fruiting-rows-master.png | img/wine-fruiting-rows.jpg | Purple grapes along right trellis, receding earth lane and hazy ridge; exec-e2472475-a7d6-4628-92f5-2fcfdea1ef67.png |
| sedan-hotel-arrival-master.png | img/wine-sedan-hotel.jpg | Unbranded black sedan at a fictional cream/timber wine-country hotel; exec-fa69105b-f27d-4d1a-b330-a948ee70d9de.png |

All four exports retain the complete composition, resized with System.Drawing high-quality bicubic to1140×760 JPEGquality85. Original generated files remain under C:/Users/eubur/.codex/generated_images/01a1e3ae-d022-71e3-9a6c-8af427060195/. `src/wine_imagery.py` uses stable per-winery assignments and reserves hero/inset/transport scenes from card assignments. Each winery now retains the same card scene across its regional and estate pages; each page avoids repeats. Scenes may recur in unrelated regions. This is not72 distinct documentary estate photographs across the website. Public winery links remain internal per the later navigation direction.


November16 package prototype: `sprinter-vineyard-outing-master.png`,1536×1024,3297682bytes,SHA256a20cb4bd25edf4acc3f87350e7b2c75435c10f5f2e6f3bfef444779812d701b6, shared `assets/20261116/packages/`. Built-in ImageGen generated one people-free fictional rear-three-quarter black van at a vineyard picnic turnout; empty table left, rows/dry hills, closed doors, no readable marks/plates/text. Original exec-47e9b901-380e-48d6-9b24-9850d3fceb22.png preserved under generated_images/01a1e3ae-d022-71e3-9a6c-8af427060195. Whole composition resized with high-quality bicubic to1140×760 JPEGquality85 as `img/wine-sprinter-outing.jpg`. Preview vehicle-class ambience, not assigned fleet/estate evidence. Remaining package card scenes reuse existing approved fleet/regional assets and their owning provenance, with nine distinct scene files in the current catalogue; no new capacity or equipment claim.

## November16 winery-card image correction

Supersedes the earlier wine-day package-card assignments. All nine discovery images now lead with fictional wine-country scenery: vineyards, terraces, a cellar, garden, veranda, tasting room and picnic setting. No people or vehicles are present. Vehicle categories remain explicit text choices; dedicated fleet presentation and the original three page compositions are unchanged. These are not photographs of named estates or proof of an included tasting. Existing earlier images remain preserved.

Built-in image_gen made one distinct landscape master per card. Shared masters and exact prompt set: mockups/livermore-visual-directions/2026-11-14/assets/20261116/wine-country/ (generation.json). Whole compositions exported to1140x760 JPEG quality85 with high-quality bicubic resize. Contact sheet and actual rendered evidence are in the existing implementation folder.

| Export in img/ | Original generated master | SHA256 master |
|---|---|---|
| wine-day-napa-terrace.jpg | exec-e0a0a524-a6e7-42a3-814e-655447202f65.png | 563acd62dec33d98ccdf18f52b733559067638b3894a15640b461509d833888c |
| wine-day-napa-cellar.jpg | exec-e26bc396-b558-4dcf-94e4-665161c1cfc2.png | 2971f26defe52893671449e9380ce7c1c74711c264028d6f0bd95a8705ef5c1e |
| wine-day-napa-estate.jpg | exec-6bf79af7-b806-4e24-a420-99dce66aa0b9.png | 764c6856b656713bf3162d52108eea46abdba1d4d84a25160bb2989f1102a712 |
| wine-day-sonoma-oaks.jpg | exec-b0724bf9-a6b4-413f-b1e9-3d599b95f790.png | a9b04fa77f0869950a6000866b91d00ba96449618cd1de627932f82506b460d2 |
| wine-day-sonoma-garden.jpg | exec-991d872b-3d4a-4869-a812-9efabe16f9ff.png | 330ee77b8c5bdabced362ef50f6ce609b4d171a195cf40f6dcbb55099f705f81 |
| wine-day-sonoma-veranda.jpg | exec-94818c30-7990-4e18-b2d4-8c732637a626.png | 7615650d2fed19f8b27ae96b035808358d2ffc1215673e1aa5121a1aedd76479 |
| wine-day-livermore-rows.jpg | exec-93b6e93a-6d6e-4ad9-9506-726aa5d44766.png | cd53ad3b425d776b5c025ff23cdabc85c42da29f88c0aa903dd40565135fcf23 |
| wine-day-livermore-tasting.jpg | exec-8d40cff6-ff28-42af-b30c-53269ed62732.png | fe6c1fcaa3cc8fcd3a1ac55d891bd2227193bebd74311ff32030c1a9a43928a5 |
| wine-day-livermore-picnic.jpg | exec-c20f337a-e9ae-4fa5-a5ee-fd74948ff93e.png | 62c2cdfdb6f7cbf9b3d9a23142e41c0530b60b9d40cae3fe8e969a6184b7385c |
