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
    """Render the editorial service brief with unchanged booking and quote inputs."""
    quote = escape(quote_url, quote=True)
    return f"""
<header class="renewal-hero renewal-editorial"><div class="wrap renewal-editorial-grid">
  <div class="renewal-hero-content">
    <div class="crumbs"><a href="/">Home</a><span>/</span><a href="/cities/">Cities</a><span>/</span>Sacramento</div>
    <p class="renewal-kicker">Sacramento · Private chauffeur</p>
    <h1>Sacramento black car service.<br><span class="o">Make the day your own.</span></h1>
    <p class="lede">An SMF arrival, a Capitol meeting or an evening event. Connect the pickup, complete route and return plan with a private chauffeur and a transportation quote for your party.</p>
    <p><a class="btn btn-orange" href="{quote}">Get a Sacramento quote</a></p>
    <a href="#plan-your-trip">Plan your Sacramento ride →</a>
  </div>
  <img class="renewal-hero-image" src="/img/city-sacramento.jpg" alt="Sacramento skyline and Tower Bridge reflected in the river at dusk" fetchpriority="high" decoding="async">
</div></header>

<section class="renewal-section" id="plan-your-trip" style="scroll-margin-top:100px"><div class="wrap">
  <div class="sec-head"><p class="renewal-kicker">Choose your next stop</p><h2>From arrivals to the evening's plans.</h2>
    <p>Share the actual entrance and full itinerary, so the quote covers the journey you need.</p>
  </div>
  <div class="renewal-fact-grid">
    <article class="card"><p class="renewal-kicker">SMF airport transfers</p><h3>From flight to hotel</h3>
      <p>Send the flight number, local arrival date, destination, passengers and bags. Confirm the terminal and follow your chauffeur's agreed pickup instructions.</p>
      <p>For departure, include hotel luggage collection and any extra stop. Agree on the pickup time with your airline's airport-arrival guidance in mind.</p>
      <p><a href="https://flysmf.gov/about/faq">SMF official airport information</a> · <a href="/services/airport-transfers">Airport-transfer service</a></p>
    </article>
    <article class="card"><p class="renewal-kicker">Capitol, Downtown &amp; Midtown</p><h3>Connect the appointments</h3>
      <p>Name the hotel, Capitol-area building or office entrance. Include meeting times, luggage collection and where the day should finish.</p>
      <p>For Folsom, Roseville or regional stops, send every address and confirm the vehicle's service window.</p>
      <p><a href="/services/corporate-travel">Corporate and executive transportation</a></p>
    </article>
    <article class="card"><p class="renewal-kicker">Golden 1 Center &amp; conventions</p><h3>Agree on the return</h3>
      <p>Share the event, venue, arrival target and expected finish. Confirm a pickup point that accounts for crowds and current street access.</p>
      <p>A venue address does not guarantee curb access. Use the organizer's entrance instructions and agree on the meeting location with your chauffeur.</p>
      <p><a href="https://www.golden1center.com/visit/directions-and-parking/">Golden 1 Center official visitor directions</a></p>
    </article>
  </div>
</div></section>

<section class="renewal-section"><div class="wrap renewal-split">
  <figure class="renewal-image-panel"><img src="/img/fleet-business-suv-airport-scene.webp" alt="Black SUV and a suitcase outside a glass-fronted terminal" loading="lazy" decoding="async"></figure>
  <div><p class="renewal-kicker">Your itinerary, your service</p><h2>A single ride.<br>Or a chauffeur between stops.</h2>
    <article class="renewal-trip-note"><h3>Point-to-point transfer</h3><p>Arrange one journey with agreed stops. Confirm a later return as a separate leg rather than assuming the car remains after drop-off.</p></article>
    <article class="renewal-trip-note"><h3>Hourly chauffeur</h3><p>For several meetings or waiting between appointments, request a service window. Confirm waiting, the finish time and how itinerary changes are handled.</p></article>
    <p><a href="/blog/hourly-chauffeur-vs-point-to-point-transfers">Compare hourly and point-to-point service</a></p>
    <p>Koast provides transportation with a chauffeur; it is not a self-drive truck rental.</p>
  </div>
</div></section>

<section class="renewal-section"><div class="wrap">
  <div class="sec-head"><p class="renewal-kicker">Beyond the city</p><h2>Sacramento to San Francisco or Napa Valley.</h2></div>
  <div class="renewal-fact-grid">
    <article class="card"><h3>Bay Area destination</h3><p>For <a href="/cities/san-francisco">San Francisco transportation</a>, share the full destination address and any return leg. Traffic and collection time can change the journey; confirm a pickup plan instead of relying on a fixed drive-time estimate.</p></article>
    <article class="card"><h3>A Napa tasting day</h3><p>For <a href="/wine-tours/napa-valley">Napa Valley wine transportation</a>, send the tasting confirmations and actual winery addresses. Arrange tasting reservations separately from the vehicle, with travel buffers and the return included in the plan.</p></article>
    <article class="card"><h3>Traveling as a group</h3><p>Choose the vehicle for your actual passengers, luggage, equipment and access requirements. Vans, Sprinters and buses require a quote; <a href="mailto:reserve@koastride.com">send the complete group itinerary</a> and confirm seating and luggage space before reserving.</p></article>
  </div>
</div></section>

<section class="renewal-section" id="reserve-ride"><div class="wrap renewal-split">
  <div><p class="renewal-kicker">Your ride, arranged</p><h2>Send one complete<br>transportation brief.</h2>
    <p>Have your local date, pickup time, entrances and flight or event details ready. Include passengers, bags, all stops, waiting needs and the required finish time.</p>
    <p><a class="btn btn-orange" href="{quote}">Get a Sacramento quote</a></p>
  </div>
  {booking_markup}
</div></section>
"""
