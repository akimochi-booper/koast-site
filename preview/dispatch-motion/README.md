# Koast Dispatch animated motion studies

Status: EXPLORATORY. Published only at /preview/dispatch-motion/. This does not replace the live Dispatch launch sequence.

- Relay: two warm/teal light cues meet beneath the existing lockup; a handoff between passenger and chauffeur.
- In Sync: three staggered light lanes align, then clear for the existing lockup.
- Fleet Ready: a generated premium chauffeur fleet scene gains light sequentially before the lockup settles.

All are approximately two-second entrances followed by a review hold. The 3.4-second review loop, playback timeline, controls and gallery frame are preview-only. No remote APIs, account data, trip data or document changes.

Brand sources: wordmark.svg is an exact copy of img/koast-wordmark-orange-v1.svg. assets/dispatch-teal-v1.png is the existing Ops Dispatch raster mask, rendered with the existing mask geometry and #51c6bc. assets/lightpoint.webp is the approved passenger light texture. Fleet scene provenance and full prompt are in PROMPTS.md. No logo geometry was redrawn.

QA: native module syntax checks, site generation, 16 site tests, generated-page checks; desktop and 402px phone playback, timeline and pause, mobile selection, expanded view and close, image decode readiness, reduced-motion static default with explicit Play motion opt-in. Reduced-motion test emulation restored afterward.

The initial Rider/Driver Home Screen edge flash is paused at the owner's request. Reduce Motion comparison was unchanged on the owner's reported iOS 26.6.2. No claim that the flash is resolved.
