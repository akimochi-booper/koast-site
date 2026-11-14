"""Sacramento's authored service brief; pure markup, injected booking card/URL.

Uses existing marketing hero/cards/buttons. Sources and exact Search Console
baseline are recorded in docs/stags-sacramento-search-20261113.md.
"""
from html import escape

SACRAMENTO_TITLE = "Sacramento Black Car Service & SMF Transfers | Koast"
SACRAMENTO_DESCRIPTION = (
    "Private black car service in Sacramento for SMF airport transfers, Capitol "
    "meetings, hotels and events. Plan your route and request a transportation quote."
)
SACRAMENTO_FAQS = [
    ("How do I book black car service in Sacramento?",
     "Send the local travel date, exact pickup and destination addresses, passenger count "
     "and luggage needs. Include any return leg or stops. Request a transportation quote "
     "and confirm the vehicle, route and service window before reserving."),
    ("Can I arrange a private car from SMF to my Sacramento hotel?",
     "Yes. Include your flight number, local arrival date, passengers, bags and hotel address. "
     "Confirm the terminal and current pickup instructions before meeting your chauffeur. "
     "For the return flight, provide departure details and agree on a pickup time that allows "
     "for the airline's airport-arrival guidance and conditions on your travel date."),
    ("Is this a chauffeured ride or a self-drive vehicle rental?",
     "Koast provides private transportation with a chauffeur. A sedan or SUV quote is for "
     "your planned ride, rather than renting a truck to drive yourself. Specify passenger, "
     "luggage and equipment needs so the actual vehicle can be confirmed."),
    ("Should I book a transfer or an hourly chauffeur?",
     "A point-to-point transfer suits one journey with agreed stops. For several meetings, "
     "waiting between appointments or a chauffeured day, request hourly service and confirm "
     "the full service window. A drop-off does not automatically include a later pickup."),
    ("Can we plan a Sacramento trip to San Francisco or Napa Valley?",
     "Include the full destination address and a return plan in the quote request. For Napa "
     "tastings, book winery appointments separately and send each address and confirmed time. "
     "Agree on travel buffers and the vehicle's service window; a map estimate is not a guaranteed journey time."),
    ("How is Sacramento car service priced for a group?",
     "The transportation quote depends on the route, vehicle, stops and service window. "
     "Vans, Sprinters and buses require a quote. Confirm the actual seating, luggage space, "
     "access requirements, waiting and change terms for your party before reserving."),
]


def render_sacramento_body(booking_markup, quote_url):
    """Return page-specific body; generator retains shared fleet/FAQ/footer owners."""
    quote = escape(quote_url, quote=True)
    return f"""
<header class="hero-dark"><div class="wrap">
  <div class="crumbs"><a href="/">Home</a><span>/</span><a href="/cities/">Cities</a><span>/</span>Sacramento</div>
  <div class="hero-grid">
    <div class="hero-copy">
      <h1>Sacramento black car service <span class="o">for airport &amp; city travel.</span></h1>
      <p class="lede">A private chauffeur for your SMF transfer, Capitol meeting or event in Sacramento. Arrange the pickup, complete route and return plan with a transportation quote for your party.</p>
      <ul class="check" style="color:#cdd3dc">
        <li>SMF airport transfers and hotel pickups</li>
        <li>Downtown, Midtown and regional business trips</li>
        <li>One transfer or an hourly chauffeur itinerary</li>
      </ul>
      <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:24px">
        <a class="btn btn-orange" href="{quote}">Get a Sacramento quote</a>
        <a class="btn btn-ghost-light" href="#plan-your-trip">Plan your Sacramento ride</a>
      </div>
    </div>
    {booking_markup}
  </div>
</div></header>

<section class="tight" id="plan-your-trip" style="scroll-margin-top:100px"><div class="wrap">
  <div class="sec-head"><span class="pill">Sacramento pickup planning</span>
    <h2>Start with the journey you need</h2>
    <p>Choose the service around your flight, appointment or event. Share the actual entrance and full itinerary so the quote covers the transportation you need.</p>
  </div>
  <div class="grid-3">
    <article class="card"><h3>SMF to your hotel or meeting</h3>
      <p>Send the flight number and local arrival date, plus your destination, passengers and bags. Confirm your arrival terminal and follow the agreed chauffeur pickup instructions.</p>
      <p>For departure, include hotel luggage collection, the flight details and any extra stop. Allow for check-in and security using your airline's guidance.</p>
      <p>Check <a href="https://flysmf.gov/about/faq">SMF's official airport information</a> and our <a href="/services/airport-transfers">airport-transfer service</a>.</p>
    </article>
    <article class="card"><h3>Capitol, Downtown &amp; Midtown</h3>
      <p>For Capitol-area appointments, downtown hotels or Midtown offices, name the building and entrance rather than a district alone. Add meeting times, luggage collection and the final destination.</p>
      <p>For Folsom, Roseville or other regional stops, send every address. A meeting itinerary needs a confirmed vehicle and service window.</p>
      <p>Review <a href="/services/corporate-travel">corporate and executive transportation</a>.</p>
    </article>
    <article class="card"><h3>Golden 1 Center &amp; conventions</h3>
      <p>Send the event name, venue, arrival target and expected finish. Agree on an accessible pickup point and a return plan that accounts for crowds and current street access.</p>
      <p>A venue's main address is not a promise of curb access. Use the organizer's entrance instructions and confirm the meeting location with your chauffeur.</p>
      <p>Review <a href="https://www.golden1center.com/visit/directions-and-parking/">Golden 1 Center's official visitor directions</a> for venue planning.</p>
    </article>
  </div>
</div></section>

<section class="tight"><div class="wrap grid-2" style="align-items:start;gap:40px">
  <div>
    <span class="pill">Choose your service</span><h2>A single ride or a chauffeur between stops?</h2>
    <p><strong>Point-to-point:</strong> arrange one journey with agreed stops. Book a later return as a separate leg rather than assuming the car remains after drop-off.</p>
    <p><strong>Hourly:</strong> request a chauffeured service window for meetings or several stops. Confirm waiting, the required finish time and how itinerary changes are handled.</p>
    <p>Our <a href="/blog/hourly-chauffeur-vs-point-to-point-transfers">hourly versus point-to-point guide</a> helps compare the options. Koast provides a chauffeur with the ride; it is not a self-drive truck rental.</p>
    <h3>Sacramento to San Francisco or Napa Valley</h3>
    <p>For <a href="/cities/san-francisco">San Francisco transportation</a>, include the full Bay Area destination and whether you need a return. For <a href="/wine-tours/napa-valley">Napa Valley wine transportation</a>, share the tasting confirmations and actual winery addresses. Arrange tasting reservations separately from the vehicle.</p>
    <p>Compare the complete route for your travel date. Traffic, terminal collection and event access can change the timing; confirm a pickup plan instead of relying on a fixed drive-time estimate.</p>
  </div>
  <article class="card"><h3>Send one complete transportation brief</h3>
    <ul class="check">
      <li>Local date, pickup time and exact entrances</li>
      <li>Flight details or appointment and event times</li>
      <li>Passengers, bags and any equipment or assistance requirements</li>
      <li>All stops, waiting needs and the final destination</li>
      <li>Any return leg and required finish time</li>
    </ul>
    <p>For a van, Sprinter or bus, <a href="mailto:reserve@koastride.com">request a group quote</a>. Confirm the actual seating, luggage space and access requirements before reserving.</p>
    <p><a class="btn btn-orange" href="{quote}">Get a Sacramento quote</a></p>
  </article>
</div></section>
"""
