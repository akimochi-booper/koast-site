# Daily guide QA - October 17, 2026

Article: Napa Wine Tours: Confirming Tastings and Transportation.

Duplicate check: latest main and public blog had no October 17 guide. Release contains exactly one post with that date.

Editorial: two confirmation checklists, responsibility for booking, and a hypothetical schedule-change example; distinct from existing broad Napa/group itineraries. Independent daily_guide_review_20261017 reviewed draft and actual image, with no blocking findings. No private content, prices, capacities, tasting/drive-time rules, new Koast policy or prohibited promotions. Coordination by operator/planner remains possible; inclusions must be confirmed.

Primary source checked October 17: https://www.domainecarneros.com/visit/plan-your-tasting-and-tour supports attributed reservations, adults 21+, groups under one reservation and potential inability to accommodate late rescheduling. No universal winery policy inferred. Article uses current direct winery URL.

Image: built-in generation, optimized 1600x900 WebP 71,926 bytes. Prompt/master provenance in docs/image-provenance.md. No text/logo/fleet claims; conceptual cards and vineyard background; accurate alt and honest AI illustration caption. Hero and thumbnail visually reviewed at desktop 1440x1000 and mobile 390x844; both cards legible, no horizontal overflow. Browser scrolling stalled during QA, then recovered; no publication before checks completed.

Validation: python generate.py; python scripts/check_site.py --today 2026-10-17: 207 pages, 38 blog posts, 5 dated posts, no errors. node --check koast-acquisition.js; node --test test/*.test.mjs: 16 passed. Internal article links resolve to generated pages.

Coordination: D1 connector unavailable; read-only platform Sync Log showed sign-in. This editorial release changes no shared database, schema or cross-app behavior.

Final fetch/rebase, repeated validation and actual live results are recorded in the release report after deployment.
