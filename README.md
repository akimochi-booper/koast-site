# koast-site
Source for koastride.com. Pushing to `main` builds the static site (`python generate.py`) and auto-deploys to the Cloudflare Pages project `koast` via GitHub Actions.


## Acquisition measurement

All generated pages load `koast-acquisition.js` through the shared head template.
Events go to the Koast Platform collector at `/api/acquisition/events`:
`page_view`, outbound `booking_click` (Moovs or booking routes in the customer app),
and `contact_click` (phone/email destination type only). A click is not a booking.
The collector determines organization from the allowed website origin.

The script uses a random tab-session ID with 30-minute idle expiry, stores first
and latest source within that session, and omits cookies, form values, raw page
queries, click IDs, and destination addresses. Only published canonical paths,
referring origins, and sanitized campaign labels are sent. Browser DNT/GPC and
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
