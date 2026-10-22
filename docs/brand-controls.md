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
