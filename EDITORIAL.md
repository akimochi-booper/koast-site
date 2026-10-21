# Koast daily guides

New guides live in `content/posts/<slug>.json`. The generator adds them to the existing category index, renders the existing article layout, adds clean canonical URLs and sitemap entries, and uses each post's real published/modified dates. Existing legacy publication dates are preserved until independently verified.

## Publication process

1. Read project AGENTS.md and the deployment playbook. Use a fresh task-specific clone, never an old task clone or OneDrive code copy. Check today's already published posts before doing anything to avoid duplicate runs.
2. Read the guide inventory and choose one distinct practical reader question. Prefer Bay Area airport, business travel, vehicle/luggage planning, wine itinerary logistics, and confirmed service areas. Improve an existing guide when it already answers the same intent; do not publish another near-duplicate to meet a quota.
3. Research changing airport pickup rules, events, prices, and transport rules using authoritative current sources. Link sources naturally in the post. Do not invent firsthand experience, human review, statistics, testimonials, prices, service availability, or vehicle capacities. Do not advertise meet-and-greet. Keep Care Rides and the prelaunch app out of public content.
4. Use premium plain language, a direct answer, a usable checklist/example, relevant internal links and one clear next step. Do not target arbitrary word counts. No private customer information or material from business email.
5. Add the JSON post, using its actual Pacific publication date. A substantial update can change modified; never reset publication or dates solely for freshness. Create an article-specific image with the built-in image-generation tool when an original editorial image will help. Follow the image standards below. Use real authorized fleet/vehicle photographs when making claims about actual vehicles, luggage fit or equipment. Keep image names and metadata safe for HTML attributes.
6. Run `python generate.py` and `python scripts/check_site.py --today YYYY-MM-DD`. The generator already verifies clean canonical/indexing rules. Inspect the actual rendered article and index at desktop and mobile sizes before publishing. Ensure no layout overflow and working links. Never create a real booking during checks.
7. Review diff. Fetch/rebase origin/main immediately before push and regenerate/recheck. Commit source and regenerated `_redirects`; use the Koast GitHub App credential helper and push to main to trigger deployment. Never call wrangler deploy directly.
8. Verify the live article, dates/schema, index and sitemap after deployment, including visual checks. Report the live URL. If quality, source verification, build, deployment or live checks fail, do not claim publication success. Preserve work and report the exact blocker. Do not loosen security headers or change rates/policies to publish a guide.

## Current topic queue

- Published 2026-10-21: Airport Rides with Children: Confirming the Car Seat Plan. Restraint requirements, supplier/installation responsibility, vehicle compatibility and return-trip continuity. NHTSA guidance linked; no seat inventory, legal exemption or capacity promises.

- Published 2026-10-13: Hourly Chauffeur or Separate Transfers? Planning a Day of Meetings.
- Published 2026-10-14: Booking an Airport Ride for Someone Else: A Passenger Handoff Checklist. Includes a copyable traveler brief, change ownership and communications fallback; distinct from the broad EA guide.
- Published 2026-10-16: SFO, OAK or SJC? Choosing an Airport for a Silicon Valley Business Trip. Destination-based comparison, official flight resources and a complete-journey checklist; no fixed drive times or airport ranking.
- Published 2026-10-19: Airport SUV Luggage: What to Confirm Before You Book. A measurement and passenger/luggage brief for provider configuration confirmation; no numeric vehicle capacity, fit guarantees or actual fleet demonstration. Specific vehicle fit claims remain dependent on verified fleet configurations.
- Published 2026-10-20: Flight Changed? How to Update Your Airport Ride. Disruption recovery for cancellations, missed connections, replacement flights and diversions; full-date checks, original-reservation status and a copyable amendment request. Distinct from routine passenger handoff; no change-fee, availability or flight-tracking automation promises.
- Candidate: transporting golf clubs or presentation equipment; verify distinct intent beyond the luggage guide and obtain actual configuration evidence for any fit claims.
- Published 2026-10-15: Hotel Checkout Before an Evening Flight: A Luggage and Pickup Plan. Bag custody, retrieval detour, a clearly labeled backwards-planning example and pickup checklist.
- Published 2026-10-17: Napa Wine Tours: Confirming Tastings and Transportation. Separate confirmation checklists, booking responsibility and a change-acknowledgment example; no standard tasting/drive-time or policy assumptions.
- Published 2026-10-18: Wedding Guest Return Rides: Planning the Last Shuttle. Early returns, destination-specific counts, final-departure coordination and a copyable guest message; illustrative times only, no new capacity or service promises.
- Completed 2026-10-13: clearly archive expired San Francisco summer 2026 guide; refreshed SFO pickup and waiting guidance.

Daily cadence is a target, not permission to publish unsupported or repetitive content. Owner authorized automatic publishing after factual, quality and website checks on 2026-10-13.

## Image standards

### Koast visual direction (owner revised October 17, 2026)

- Default to realistic premium travel-editorial imagery: believable light, reflections, vehicle proportions, materials and landscapes. Avoid plastic CGI finishes, toy-like objects, exaggerated HDR and artificial-looking scenes. Realism is an aesthetic goal, not permission to present generated imagery as documentary evidence.
- Choose the mood to suit each article. Natural daylight, warm sunsets, dusk, darker atmospheric scenes and black-and-white photography treatments are all welcome. Be creative; do not force a single lighting treatment, color palette or visual formula across the blog.
- Vary subjects and framing: destination scenery, journeys, architectural details, close-up textures and thoughtfully composed editorial collages. The owner particularly liked the black-and-white grape close-up. Use similarly relevant detail shots where they fit; not every article needs a vehicle.
- Let the website's charcoal, white and orange framing carry the brand. Restrained Koast orange #ff5c1f can be an accent when useful, but do not force orange objects, lines or sunsets into every image. Natural scene colors and monochrome can both fit Koast.
- Review recent article images before choosing a concept. Avoid repeating the same car angle, dark tabletop, floating cards, checkmarks, location pins or phone composition. Variety should follow the topic rather than a rigid rotation. Keep compositions legible at card size and on mobile.
- Use a distinct, relevant editorial image for each new article. Preserve the factual safeguards below: generated scenes must retain accurate internal provenance and must not purport to document Koast's actual fleet, passengers, service, equipment or a specific real location. Actual fleet and service claims require authorized real photography. Do not invent or redraw the Koast logo inside generated art.

- Review the generated image for incorrect vehicle geometry, unreadable text, misleading airport signs, extra limbs, logos, license plates, VINs and misleading fleet representations. Regenerate if the result is poor. No logos or text inside conceptual illustrations by default.
- Keep an original master outside the public deploy. Export a web-ready WebP, ordinarily 1600px wide and below 250KB; automated gates require at least 1200px and at most 350KB. Preserve the composition rather than stretching or cropping essential details.
- Required JSON: image_alt (describe the actual picture, not a keyword list), image_width, image_height, image_generated (boolean). The template reserves image space and shows the full hero composition on mobile. Per owner direction on October 17, 2026, do not display an automatic AI-generated illustration caption in articles. Keep image_generated and docs/image-provenance.md accurate for internal provenance; do not replace the caption with claims that generated images are real photographs. Verify social preview and structured-data image use the actual article image.
- Inspect both the article hero and card thumbnail on mobile and desktop. A technically valid file is not proof of a good image.
- Record the final prompt, tool and asset in docs/image-provenance.md. If generation is unavailable, use a specifically relevant licensed asset or skip and report the blocker; do not silently substitute a generic image.

## Industry articles and video

Mix in occasional industry explainers aimed at passengers and bookers: what a chauffeur quote includes, how transfer and hourly reservations differ, why pickup zones matter, and what to ask before booking. Existing related guides should be improved before creating overlapping articles. Broad industry news belongs only when the change materially affects customer planning, cost or availability and can be supported by current primary sources.

Video is a separate production stream, not a daily publication requirement. Prefer short authentic demonstrations of actual vehicles, luggage fit and pickup preparation, with captions and an accurate transcript. Do not generate footage that purports to show Koast's real fleet or service. Create watch pages and video metadata only when real videos are available and verified; no placeholder players, autoplay hero video or invented VideoObject markup.
