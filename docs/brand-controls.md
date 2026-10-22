# Website orange controls

Approved deployment target: option E orange-gradient wordmark palette, 2026-10-21.

The shared `--brand-gradient` token uses 180deg stops #f3b747 (0%), #f6ab3e (25%), #f98b2b (52%), #fc6a1c (79%), #fd581a (100%). `--brand-ink` is #241205. Use them for primary CTAs, booking buttons, chat controls, and prominent orange decorative badges. Keep the SVG wordmark as the source artwork.

Small functional text stays solid: `--orange-text` #a63b10 on light backgrounds and `--orange-on-dark` #f6ab3e on dark backgrounds. Do not apply gradient text to body copy or links. Large hero highlights may use the gradient with a solid fallback and forced-colors fallback.

Hover increases brightness slightly; active darkens slightly. Existing focus rings remain visible. Disabled primary buttons remove lift/shadow and reduce opacity. Teal status/secondary colors and functional recording indicators retain their semantics.

Contrast: #241205 against the five gradient stops ranges from 5.66:1 to 10.03:1. Light-background link text is 6.45:1 against white; dark-background orange text is 9.81:1 against #0e1013.

The embedded Moovs booking widget is independently hosted and does not inherit website CSS. Its existing controls are intentionally outside this change.