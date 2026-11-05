# Daily guide restart and search metadata — November 4, 2026

Owner requested moving the archived daily blog workflow into chat `01a1a8af-065e-79c1-bec5-cc172d6d0032` and improving Google/AI search readiness. Recovered original 9:00 AM America/Los_Angeles cadence from archived “Driver log in and account.” The original automation was absent/deleted; recreated `publish-daily-koast-guide` ACTIVE on this chat using the same schedule and quality-before-publication guards. Last prior published dated guide: October 21. No missed-date backfill.

## Release content

- `/blog/airport-pickup-dates-midnight-overnight-flights`: destination local arrival date versus the independently agreed pickup date/time, midnight examples and copyable brief. Primary SFO flight-status and Emirates local-time/next-day schedule conventions checked November 4. No universal readiness buffer, waiting allowance, automatic amendment or fleet claims. Independent reviewer requested an explicit before-/after-midnight date distinction; incorporated.
- Original generated editorial night-terminal image, 1599 × 900 WebP / 132668 bytes, visually inspected. Prompt/master/provenance in `docs/image-provenance.md`; actual hero/card/social/schema image and dimensions agree. Existing blog layout preserved. No automatic visible AI caption.
- Richer article author/publisher organization identity and canonical main entity; `max-image-preview:large`; duplicate `og:site_name` removed. No fabricated human author or review.
- Sitemap lastmod from the ten dated editorial records only; existing publication/modification dates retained. Twelve already-noindex previews omitted from sitemap, with their accessibility/noindex protections retained. 216 index-candidate URLs after adding this article.
- Existing robots search access remains; Cloudflare-managed training rules/security controls untouched. Ordinary public HTTP/browser access does not prove verified crawler WAF treatment, Search Console indexing/rankings or real-user performance. No ranking/citation guarantees.

## Validation before release

- `python generate.py`; `python scripts/check_site.py --today 2026-11-04`: 229 pages, 43 blog posts, ten dated posts, no errors. Checks include author/publisher, canonical main entity, sitemap dates, noindex exclusion, images/social/schema and local links.
- `node --check koast-acquisition.js`; `node --test test/*.test.mjs`: 23 passing. Existing tracking privacy, legal and booking controls preserved.
- Actual Chrome preview at 1440 × 1000 and 390 × 844: article hero, long copy/example and index cards readable; no horizontal overflow. Shared evidence: `audits/2026-11-04-blog-seo-restart/` in canonical Koast document workspace.
- D1 connector absent; read open coordination actions in signed-in Platform Sync Log. No active site publisher observed. This is a static site/content change, with no D1/provider/customer/payment/schema writes.

Final current-main integration, successful GitHub Actions deployment and live article/index/sitemap/desktop/mobile checks must be recorded in the shared review before reporting live.

References: [Google AI-search guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), [Article schema](https://developers.google.com/search/docs/appearance/structured-data/article), [sitemap dates](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap), [robots preview directives](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag), [OpenAI search versus training crawlers](https://developers.openai.com/api/docs/bots).
