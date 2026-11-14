# Shared-link banner color update — November 13, 2026

Decision: deployment target requested by Eugene. Implementation: local candidate; release evidence follows in the shared audit.

The existing San Francisco skyline / black SUV / “Ride easy.” composition is retained visually. Only the flat orange lettering is intentionally changed to the approved gold-to-orange family from `docs/brand-controls.md`. This is an AI image edit, so the photo is visually preserved rather than pixel-identical. White “Ride”, typography, placement and framing were compared with the prior asset. No new scene or copy was requested.

Asset: `img/og-image-v2.jpg`, 1200×630 JPEG, quality95. The built-in image-editing tool produced the master at `C:/Users/eubur/.codex/generated_images/01a1d779-0ada-7522-aec4-4502807bb6aa/exec-c2b8740c-65c5-466e-8b53-a989443ce7c8.png`; exported with high-quality bicubic scaling. The prior `img/og-image.jpg` is retained. The versioned URL helps fresh crawls obtain the new image; messages/social platforms may retain already-cached cards.

`generate.py:enhance` owns OG/Twitter metadata. Most non-article pages share this default; article hero overrides remain. The noindex splash preview also references the new default. No page-specific thumbnail rollout is part of this color-only change.

Built-in edit prompt:

> Use case: precise-object-edit. Edit target: attached existing Koast social sharing banner. Make only one precise change: recolor the orange word 'easy.' (including period) in the existing 'Ride easy.' text from its flat orange fill to the approved Koast vertical gold-to-orange gradient. Exact visible-ink gradient: top #f7a339 at 0%, #f98b2b at 29.37%, #fc6a1c at 69.10%, bottom #fd581a at 100%. Smooth vertical gradient, no outline, no glow or shadow. Keep the white 'Ride' unchanged. Preserve the exact font, glyph shapes, spacing, positioning, size, photo, vehicle, skyline, foreground, crop, lighting, shadows, textures and all other existing pixels as closely as possible. Do not regenerate the scene, do not add any wordmark or other text. Preserve original wide 1100:577 aspect ratio. Exact text remains 'Ride easy.' Only the color inside the orange letters and period changes.
