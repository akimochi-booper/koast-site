# Koast daily guides

New guides live in `content/posts/<slug>.json`. The generator adds them to the existing category index, renders the existing article layout, adds clean canonical URLs and sitemap entries, and uses each post's real published/modified dates. Existing legacy publication dates are preserved until independently verified.

## Publication process

1. Read project AGENTS.md and the deployment playbook. Use a fresh task-specific clone, never an old task clone or OneDrive code copy. Check today's already published posts before doing anything to avoid duplicate runs.
2. Read the guide inventory and choose one distinct practical reader question. Prefer Bay Area airport, business travel, vehicle/luggage planning, wine itinerary logistics, and confirmed service areas. Improve an existing guide when it already answers the same intent; do not publish another near-duplicate to meet a quota.
3. Research changing airport pickup rules, events, prices, and transport rules using authoritative current sources. Link sources naturally in the post. Do not invent firsthand experience, human review, statistics, testimonials, prices, service availability, or vehicle capacities. Do not advertise meet-and-greet. Keep Care Rides and the prelaunch app out of public content.
4. Use premium plain language, a direct answer, a usable checklist/example, relevant internal links and one clear next step. Do not target arbitrary word counts. No private customer information or material from business email.
5. Add the JSON post, using its actual Pacific publication date. A substantial update can change modified; never reset publication or dates solely for freshness. Reuse a suitable existing site image or verified licensed asset. Keep image names and metadata safe for HTML attributes.
6. Run `python generate.py` and `python scripts/check_site.py --today YYYY-MM-DD`. The generator already verifies clean canonical/indexing rules. Inspect the actual rendered article and index at desktop and mobile sizes before publishing. Ensure no layout overflow and working links. Never create a real booking during checks.
7. Review diff. Fetch/rebase origin/main immediately before push and regenerate/recheck. Commit source and regenerated `_redirects`; use the Koast GitHub App credential helper and push to main to trigger deployment. Never call wrangler deploy directly.
8. Verify the live article, dates/schema, index and sitemap after deployment, including visual checks. Report the live URL. If quality, source verification, build, deployment or live checks fail, do not claim publication success. Preserve work and report the exact blocker. Do not loosen security headers or change rates/policies to publish a guide.

## Current topic queue

- Published 2026-10-13: Hourly Chauffeur or Separate Transfers? Planning a Day of Meetings.
- Airport ride booking for another passenger: an exact handoff checklist (different from the broad EA guide).
- SFO vs OAK vs SJC for a Silicon Valley business trip, with destination-based comparison and official links.
- Business SUV luggage planning: bags, strollers and child seats (confirm real configurations; avoid fixed fit guarantees).
- Hotel checkout before an evening flight: luggage and transportation planning.
- Napa tasting reservations versus transportation reservations: what to arrange separately.
- Wedding hotel shuttles: a pickup timeline and final-departure checklist, with no new capacity promises.
- Refresh expired San Francisco summer 2026 event guidance honestly.

Daily cadence is a target, not permission to publish unsupported or repetitive content. Owner authorized automatic publishing after factual, quality and website checks on 2026-10-13.
