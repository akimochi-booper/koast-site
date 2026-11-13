# koast-site
Source for koastride.com. Pushing to `main` builds the static site (`python generate.py`) and auto-deploys to the Cloudflare Pages project `koast` via GitHub Actions.

## Validate before publication

Run `node scripts/check-pr.mjs` with Python and Node available. It regenerates
local pages, parses public/assistant JavaScript, runs every website and assistant
test, then checks generated links, metadata and article dates. The default date
uses America/Los_Angeles; `--today YYYY-MM-DD` supports an explicit check date.
Use `--help` for the command summary. Validation makes no deployment or provider
request. `Site checks` runs it on pull requests and main; repository-required
status enforcement is a separate setting. The existing main deployment and
editorial/live verification rules remain in force.


## Acquisition measurement

All generated pages load `koast-acquisition.js` through the shared head template.
Events go to the Koast Platform collector at `/api/acquisition/events`:
`page_view`, outbound `booking_click` (Moovs or booking routes in the customer app),
and `contact_click` (phone/email destination type only). A click is not a booking.
The collector determines organization from the allowed website origin.

The script uses a random tab-session ID with 30-minute idle expiry, stores first
and latest source within that session, and omits cookies, form values, raw page
queries, click IDs, and destination addresses. Only published canonical paths,
referring origins, sanitized campaign labels (80 characters maximum), and the advertising-platform type when a click marker is present are sent. Raw click identifiers and search-term parameters are never sent or stored. Browser DNT/GPC and
`?koast_tracking=off` disable collection. Local/Pages preview hosts never collect.
Labels should describe campaigns, not people; do not put personal information in
UTM links. The backend must still sanitize, rate-limit, deduplicate, and scope data.

No Moovs completion integration or unsupported iframe messages are assumed.
Their documented GTM integration is separately enabled/configured; iframe loads
and booking-link clicks must not be reported as quotes, reservations, or revenue.

Validation (also required by the deployment workflow):

```sh
python generate.py
node --check koast-acquisition.js
node --test test/acquisition.test.mjs
```

The tests cover every generated HTML page, source retention/expiry, outbound
clicks, opt-outs, privacy filtering, and non-blocking storage/network failures.
Deploy the Platform collector before enabling this site's instrumented build.
