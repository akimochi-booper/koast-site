# Koast website source map

Application authority: `akimochi-booper/koast-site`. Generated static public marketing; no D1/customer writer in the publication path. Shared engineering and preview rules live in the canonical Koast documents.

| Responsibility | Owning source and interface | Effects/guards | Verification |
|---|---|---|---|
| Daily dated guides | `EDITORIAL.md`; `content/posts/<slug>.json`; `editorial.py` → `load_posts`, `display_date` | Repository-authored public content. Validated metadata, honest dates, image provenance; Care Rides/app holds. | `python generate.py`; `python scripts/check_site.py --today YYYY-MM-DD`; desktop/mobile article and index |
| Site generation and public metadata | `generate.py`: `head`, `_schema_for`, `enhance`, `_validate_indexing_contract`, `_write_redirects` | Writes ignored HTML/sitemap/robots and tracked `_redirects`; generates canonical links, article identity, dated-editorial-only lastmod and exact legacy routes. No provider/security-setting changes. | `scripts/check_site.py` including redirect destinations and noindex exclusions; `node --test test/*.test.mjs`; live canonical/article/schema/sitemap/redirect readbacks |
| Visual layout | `generate.py`: `post_card`, `blog_page` and blog index/category rendering; `css/main.css` | Existing marketing layout and responsive image rendering; not Passenger/Dispatch standards. | Desktop/mobile article hero, copy and blog card visuals |
| Healdsburg search landing page | `healdsburg_wine_tours.py`: `render_healdsburg_body`, metadata/FAQ constants → `generate.py`: `healdsburg_winery_tours_page` | Pure authored content composed with existing marketing components at the existing URL. No booking/provider/pricing changes; larger vehicles quote-only. | `scripts/check_site.py`; `test/healdsburg-wine-tours.test.mjs`; desktop/mobile page and FAQ; recorded Search Console baseline in `docs/healdsburg-search-20261104.md` |
| Publication | `.github/workflows/deploy.yml` | Push main → checks → Cloudflare Pages; source/editorial/internal docs excluded. One release coordinator. | Successful Actions run and live page/assets/listing/sitemap |
| Acquisition | `koast-acquisition.js`; `README.md` | Privacy-scoped opt-out-aware collector; no confirmed-booking inference from clicks. | `node --check koast-acquisition.js`; `test/acquisition.test.mjs` |
