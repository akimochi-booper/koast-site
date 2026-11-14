# Public marketing design QA — November 14, 2026

final result: passed

Scope: approved public-website adaptation of Vineyard Cinema, Wine Journal and Afterglow Gallery. Eugene explicitly approved using all directions in different destinations, favored1/2 and allowed creative vehicle scenarios; no Passenger/Driver/operations/booking-app redesign. Implementation is a local candidate, not a published redesign.

Visual truth: shared `mockups/livermore-visual-directions/2026-11-14/option-1-vineyard-cinema.png` (946×1663) and `option-2-wine-journal.png` (973×1616), plus option3 for event-gallery mood. Approved scope and image provenance are in that folder's README and `docs/marketing-imagery-20261114.md`.

Implementation: http://127.0.0.1:59399, retained allocated loopback preview. Browser-rendered JPEG evidence is in the same shared folder's `implementation/`: cinema hero/discovery comparisons, editorial hero comparison, full Livermore capture, desktop and mobile route-family captures, `browser-qa-metrics.json`. Source and actual images were opened together as composite boards; these are comparison artifacts, not product UI. Actual screenshots946px wide at CSSviewport961 and973px wide at CSSviewport988, matching source-content widths after the browser's scrollbar/capture area. Both board columns use original pixel dimensions (no text/image stretching). Desktop acceptance also used1280×900; phone checks390×844 and320×800. Source mockups are desktop compositions; mobile is the responsive implementation, with no claimed physical-device acceptance.

State: public marketing, initial hero/cards with closed planning and FAQ disclosures; separate interactive checks of menu, filters, open FAQ and booking disclosure. Existing booking widget uses the repository's clearly synthetic local fixture during preview; production booking URL and widget initializer are preserved in generated source.

## Comparison history and findings resolved

- P1 first cinema pass: inherited dark heading color on a dark scenic image. Fixed scoped white cinema/gallery/CTA headings. New rendered hero and conversion-band captures confirm readable text.
- P2 first cinema pass: the custom hero's width was centered/narrowed by overlapping selectors. Fixed full-width wrap and left-aligned content, then reduced navigation/hero geometry to the selected visual rhythm. Matching-width hero board confirms the post-fix composition.
- P1 review: generic no-hero-copy transformation dropped Corporate Account Inquiry and secondary ride links. Preserved the complete authored functional content; focused regression checks cover both actions and nested booking markup.
- P2 discovery pass: oversized duplicate prose, plain reservation labels and two repeated scenic CTAs weakened the visual hierarchy. Condensed winery-card copy, added readable reservation badges, kept one scenic conversion band and placed detailed planning/booking in native disclosures. Preserved official sources, addresses and FAQ/schema equality.
- P2 editorial pass: inset photo intruded into the text-column gap at intermediate width. Reduced its left offset; recaptured desktop and320px view without overlap or horizontal overflow.
- Inherited group-copy risk: replaced generic bus/Sprinter seat claims in renewed planning/event sections with tailored-quote guidance and actual seating/luggage/access confirmation. Event primary and group CTAs now use existing email inquiry; fleet-card cutouts/specifications are retained.

No actionable P0/P1/P2 finding remains in the checked states.

## Required fidelity surfaces

- Typography: existing self-hosted Plus Jakarta Sans retained, heavy tightly spaced display headings, clear hierarchy, readable minimum16px inputs. Large desktop headings and natural phone wrapping checked. Destination-specific SEO/service copy replaces mock placeholder wording.
- Layout/rhythm: full-width scenic wine heroes, warm cream discovery cards, split editorial city/winery heroes with winery inset photography, dark event gallery. Matching-width boards reviewed for radii, image frames and section proportions. Compact native disclosures preserve practical detail without long open prose sections.
- Colors/tokens: original approved orange-gradient wordmark/buttons retained; cream/charcoal editorial palette scoped to public marketing. Contrast fixes verified in screenshots; focus rings and reduced-motion behavior retained. Original site navigation uses the cream editorial treatment across the new families.
- Images: original logo SVG reused. Three individually generated scenic assets plus one people-free edit are original raster assets; whole-composition JPEG exports/provenance documented. Regional mapping is kept; no generic picture claims to document a named winery or assigned fleet. Generated people absent from the four new assets. Existing fleet cutouts remain on the fleet carousel.
- Copy/content: named winery addresses, reservation/walk-in guidance and official links remain useful. Tasting fees/reservations stay separate; group vehicles require quotes. No new ratings/reviews/service statistics/prices/capacities introduced. Homepage unsourced testimonial/performance blocks withheld pending evidence. Existing canonical, structured-data, sitemap, privacy, acquisition and prelaunch/Care Rides gates pass their checks.

Intentional adaptations: existing navigation and exact original wordmark; region-appropriate imagery in place of fictional named-estate photos; native quote/booking handoffs and disclosures rather than unconnected mock form fields; searchable FAQ answers, related planning links and the actual site footer extend beyond the concept image. These preserve the approved visual direction while making the page useful and functional.

## Functional and technical evidence

- Installed full validation:183tests passed;233HTML pages,47posts,16dated editorial posts; zero generated-site errors. Focused parser/booking/action/idempotence tests also pass after final review.
-12desktop destination/family observations;10narrow320px checks and additional390px route/support/privacy checks. No horizontal overflow; requested images load. Final Stag's Leap inset verified at320px; people-free Palo Alto art verified after export.
- Winery search filters to Wente and one correct region; reset works.
- Mobile menu opens, Escape closes and focus returns to Open menu.
- Keyboard Enter opens a FAQ; answer visible. Planning fragment #quote-details reveals its disclosure. Quote disclosure opens the retained iframe (synthetic local endpoint only in preview).
- Browser error/warning readbacks empty in checked final states. No native desktop input or physical-device testing.
- Independent source review completed; identified corporate-action regression fixed and covered. Main refreshed to f2c4ba444f877f8039baf608016d42cf7f31414b before final integration; no publisher claimed for this local redesign.

## Follow-up polish

P3: replace regional/illustrative winery ambience with properly sourced estate photography when available. Current image captions/alt avoid estate-identity claims. Responsive device emulation is complete; physical-device acceptance remains separate.
