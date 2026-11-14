# Website orange controls

Approved deployment target: option E orange-gradient wordmark palette, 2026-10-21.

The shared `--brand-gradient` token uses 180deg stops #f3b747 (0%), #f6ab3e (25%), #f98b2b (52%), #fc6a1c (79%), #fd581a (100%). `--brand-ink` is #241205. Use them for primary CTAs, booking buttons, chat controls, and prominent orange decorative badges. Keep the SVG wordmark as the source artwork.

Small functional text stays solid: `--orange-text` #a63b10 on light backgrounds and `--orange-on-dark` #f6ab3e on dark backgrounds. Do not apply gradient text to body copy or links. Large hero highlights may use the gradient with a solid fallback and forced-colors fallback.

Hover increases brightness slightly; active darkens slightly. Existing focus rings remain visible. Disabled primary buttons remove lift/shadow and reduce opacity. Teal status/secondary colors and functional recording indicators retain their semantics.

Contrast: #241205 against the five gradient stops ranges from 5.66:1 to 10.03:1. Light-background link text is 6.45:1 against white; dark-background orange text is 9.81:1 against #0e1013.

The embedded Moovs booking widget is independently hosted and does not inherit website CSS. Its existing controls are intentionally outside this change.
## Website optical color correction — 2026-10-21

Owner clarified that the website headline and buttons looked different from the logo. Website controls now sample the visible `oast` region of the original SVG, y=477..730.5. Its gradient definition starts at y=357.5 on the taller K, so copying all five stops to a button made it too yellow. Use #f7a339 at0%, #f98b2b at29.37%, #fc6a1c at69.10%, #fd581a at100%. The original SVG stays unchanged.

The home `easy.` span maps that ramp to its visible ink bounds, excluding the font's empty ascender space (at66px, font box84px; actual ink ascent37px/descent15px). Dark-surface headlines use font-relative stops. Small text on white retains its contrast-safe dark-orange role. Decorative borders, shadows and chat surfaces use the source-derived orange family. Website CSS version22.

## Owner correction: retain teal and orange
Supersedes the rejected charcoal-only text revision. Preserve the existing teal/orange assignments. Teal feature icons, controls and badges use coordinated teal gradients. The 30+ statistic uses teal gradient; 3,100+ uses the approved orange gradient. Keep original unaccented numbers neutral. No added statistic rules. The review indicator is a small teal-gradient pill with a transparent button hit area, never a filled square.


## Website Kopilot — November9 first local proposal (superseded)

Owner requested the website popup adopt the newly selected Passenger Kopilot style and read clearly as an AI assistant. Local candidate uses Passenger deep teal155deg action stops for the launcher/identity and flat#2dd4bf for small accents. Neutral charcoal canvas, satin44px square Close/Send,16px message input and scoped welcome/conversation states replace the older orange chat treatment. Other website orange controls and source wordmark remain owned by the existing palette. This is a website-scoped proposed adaptation, not a new cross-app standard or a production release. Geometry, interaction and verification: website-assistant-design-qa.md.


## Website Kopilot — retain orange and existing material

Latest owner direction supersedes the teal website proposal: retain the original source-derived orange gradient rim and165deg translucent charcoal/14pxblur surface. Refresh the composer, name/icon, floating AskKopilot control and quote/team actions. Passenger teal adoption remains Passenger-only. The current local website revision uses existing website orange/ink tokens, an authored chat-and-spark mark, a restrained warm composer/Send rim, quiet neutral text links for quote and email beneath the composer (superseding the earlier prominent buttons). No page-wide recoloring or artificial new texture. Local review only, not published; current evidence in website-assistant-design-qa.md.


## Website favicon — approved K source, November10,2026

The versioned favicon family crops only the two-path K group from `img/koast-wordmark-orange-v1.svg`, the approved optionE source. Both path `d` attributes, original group translate/scale, inherited evenodd fill rule and five-stop `gold-k` gradient are retained exactly. Only the outer square viewport changes; the artwork is centered with6.25percent clear space on each limiting edge. No AI redraw or path approximation. The source SVG SHA256 is `14a2ebe3781072ef04bfd1b04ad886b8fea5a7938d04a239c6e76586a9fc5198`.

Assets: `img/koast-favicon-v2.svg`, `img/koast-favicon-v2-16.png`, `img/koast-favicon-v2-32.png`, `img/koast-favicon-v2-48.png` and root `favicon-v2.ico` containing those three PNG resolutions. PNG alpha padding/dimensions and ICO entry dimensions/byte ranges are asserted during generation; source versus output paths, transform and gradient must match. Existing square app/PWA/apple assets and the full header wordmark are untouched.

Rebuild explicitly with optional isolated tooling: `npm install --prefix .favicon-tools --no-save @resvg/resvg-js@2.6.2 @xmldom/xmldom@0.9.12`, then `node scripts/build-favicon.mjs`. The script uses the current repository vector asset and emits deterministic committed assets; it is not required by `generate.py` or the production publication workflow. Keep `.favicon-tools/` ignored locally. `KOAST_FAVICON_TOOLS` may point to an existing equivalent tooling prefix. A256px visual preview is written only to that ignored tooling folder for inspection. Head-tag wiring and final live verification belong to the integrating publisher; asset creation alone is not a deployment claim.

## November14 owner fidelity correction

The owner explicitly rejected the blended implementation and requested each original composition be kept intact. `src/wine_designs.py` owns the three complete renderers; `css/wine-reference.css` separately scopes Vineyard Cinema, Wine Journal and Afterglow Gallery. Livermore uses Cinema, Healdsburg uses Journal and Napa uses Gallery; private noindex `/preview/wine-designs/{cinema,journal,gallery}` pages compare all three with the same Livermore content. Existing other public-page improvements remain separate.

Cinema retains its transparent header, bright scenic image, orange-gradient display highlight, Pickup/Date/Your party/Get a quote bar, photo-card grid and single scenic conversion band. Journal retains its large black stacked headline, serif accents, overlapping portrait imagery, horizontal winery rows and full-width SUV band. Gallery retains its charcoal canvas, three-line gradient headline, journey steps, square photo gallery and cream planning section. The source mockups are the visual targets; added detailed planning and the complete searchable FAQ sit below the original composition.

The quote UI validates pickup/date/party in memory, then shows a native modal review. A visitor chooses the existing email draft or booking destination. Email requires the visitor to send their draft; no quote price, reservation, email delivery, unsupported provider prefill, tracking event, persistence or provider submission is inferred. No form values enter analytics. The existing Moovs embed remains intact in supplemental planning. Official embed reference: https://intercom.help/moovs-05c940f1970e/en/articles/6650028-how-to-add-moovs-to-your-website ; no verified prefill contract was found in the reviewed installation guidance.

Icons use unmodified Tabler Icons v3.20.0 outline SVGs from the official repository, with MIT attribution in `img/icons/tabler/LICENSE.txt`. Native focus, keyboard, reduced-motion, fallback booking paths and group quote-only handling remain required.
