# Daily guide QA - 2026-10-16

Topic: SFO, OAK or SJC? Choosing an Airport for a Silicon Valley Business Trip.

- Duplicate check: live blog had no October 16 guide; latest main contained three dated posts through October 15. Exactly one October 16 post in release.
- Distinctness: independent editorial review of legacy inventory and recent guides found no airport-choice comparison. Does not duplicate pickup procedures, handoff or luggage-storage guides.
- Primary sources checked October 16: https://www.flysfo.com/about (Peninsula/San Mateo location), https://www.flysfo.com/passengers/flight-info (flight-resource link), https://www.flysanjose.com/flysimple (San Jose location), https://www.flysanjose.com/nonstop-destinations (route-resource link), https://www.iflyoak.com/fly/wherewefly/ (flight-resource link), https://www.iflyoak.com/ground-transportation/driving-directions-getting-to-oak/ (I-880 access and Oakland location). Old oaklandairport.com domain redirects to iflyoak.com. No schedules, frequencies, fares or numerical travel times copied. Geographic comparisons are editorial starting points, explicitly conditional on exact addresses and flights.
- Content: original checklist and three hypothetical comparisons; no customer data, service-policy changes, prohibited service promotions or fleet claims. Four internal links resolve to generated pages.
- Image: built-in generation, original master outside deploy, 1600x900 WebP 45,324 bytes; reviewed image and article/card presentation, no geographic map claims, text/logos or misleading actual fleet evidence. Alt, dimensions, generated flag and honest template caption present. Prompt in image-provenance.md.
- Validation: python generate.py; python scripts/check_site.py --today 2026-10-16: 206 pages, 37 blog posts, 4 dated posts, no errors. node --check koast-acquisition.js; node --test test/*.test.mjs: 16 pass.
- Browser: local article hero/body and blog thumbnail inspected at desktop 1440x1000 and mobile 390x844. Full hero composition visible, legible card composition, no horizontal overflow.
- Independent review: daily_guide_review_20261016 reviewed draft, primary sources and image, no required changes.
- Coordination limitation: no D1 connector available; platform Sync Log opened read-only but requires sign-in. Pure editorial release has no shared DB, schema or app behavior changes.
- Deployment and live verification performed by coordinating agent after final fetch/rebase and repeated workflow checks; see release report for actual outcome.
