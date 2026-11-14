"""Authored Palo Alto service copy; pure markup using existing marketing components."""
from html import escape

PALO_ALTO_TITLE = "Palo Alto Car Service | SFO & SJC Airport Transfers | Koast"
PALO_ALTO_DESCRIPTION = (
    "Private car service between Palo Alto, SFO and SJC. Plan airport pickups, "
    "Stanford visits and Silicon Valley meetings with a fixed transportation quote."
)

PALO_ALTO_FAQS = [
    ("Can I book a car from SFO to Palo Alto?",
     "Yes. Request an SFO airport transfer with your flight number, local arrival date, "
     "passenger and luggage counts, and exact Palo Alto destination. Confirm the pickup "
     "instructions for your arrival and include any hotel or meeting stop in the quote."),
    ("Does Koast offer SJC to Palo Alto car service?",
     "Yes. Send your SJC flight details and full drop-off address for a private transfer "
     "to Palo Alto, Stanford or a nearby Silicon Valley destination. Choose the vehicle "
     "for your passengers and bags, and confirm the complete itinerary before travel."),
    ("How should I plan a Palo Alto pickup for a return flight?",
     "Provide the departure airport, local flight date and time, airline, pickup address "
     "and building entrance. Include any hotel luggage collection or other stop. Agree on "
     "a pickup time using your airline's arrival guidance and the route for that travel time; "
     "a typical driving-time estimate alone is not a departure plan."),
    ("Can you arrange Stanford and Sand Hill Road transportation?",
     "Yes. Include the exact Stanford building or visitor destination, or the full address "
     "for a meeting on nearby Sand Hill Road in Menlo Park. Share the host's entrance and "
     "loading instructions so the pickup or drop-off is arranged for the correct place."),
    ("Should I request one transfer or an hourly chauffeur?",
     "Request a point-to-point transfer for one journey. For several meetings with a car "
     "between stops, request hourly service and list the addresses, appointment times and "
     "required finish time. Confirm the service window, included waiting and any changes "
     "in the transportation quote."),
    ("How much does Palo Alto car service cost?",
     "The quote depends on the complete route, vehicle and service window. Enter a sedan "
     "or SUV trip for a quote, or send the full itinerary for a meeting day. Vans, Sprinters "
     "and buses require a quote; confirm the actual seating, luggage space and any other "
     "requirements before reserving."),
]


def render_palo_alto_body(booking_markup, quote_url):
    """Render the editorial city brief; keep booking and quote destinations injected."""
    quote = escape(quote_url, quote=True)
    return f"""
<header class="renewal-hero renewal-editorial"><div class="wrap renewal-editorial-grid">
  <div class="renewal-hero-content">
    <div class="crumbs"><a href="/">Home</a><span>/</span><a href="/cities/">Cities</a><span>/</span>Palo Alto</div>
    <p class="renewal-kicker">Palo Alto · Private chauffeur</p>
    <h1>Palo Alto car service.<br><span class="o">Your next stop, connected.</span></h1>
    <p class="lede">SFO or SJC arrivals. Stanford visits. A Silicon Valley meeting day. Arrange your complete route with a private chauffeur and a fixed transportation quote.</p>
    <p><a class="btn btn-orange" href="{quote}">Get a Palo Alto quote</a></p>
    <a href="#airport-options">Compare airport transfers →</a>
  </div>
  <img class="renewal-hero-image" src="/img/city-palo-alto-renewal-v1.jpg" alt="Tree-lined Palo Alto street in warm evening light" fetchpriority="high" decoding="async">
</div></header>

<section class="renewal-section" id="airport-options"><div class="wrap">
  <div class="sec-head"><p class="renewal-kicker">From the terminal to your destination</p>
    <h2>SFO or SJC to Palo Alto?</h2>
    <p>Compare the flight schedule with your hotel address and first appointment. Plan the ground journey around the trip you actually need.</p>
  </div>
  <div class="renewal-fact-grid">
    <article class="card"><p class="renewal-kicker">SFO arrivals</p><h3>Flight to front door</h3>
      <p>Send your flight number, local arrival date, passengers and bags. Name the hotel, Stanford building or office entrance, including any stop along the way.</p>
      <p><a href="/routes/sfo-to-silicon-valley">SFO to Palo Alto and Silicon Valley transfers</a> · <a href="/airports/sfo">SFO pickup guide</a></p>
    </article>
    <article class="card"><p class="renewal-kicker">SJC arrivals</p><h3>Your Silicon Valley connection</h3>
      <p>Arrange a private transfer from San Jose Airport. Continuing to Menlo Park or Mountain View? Include every address before confirming the route.</p>
      <p><a href="/routes/sjc-to-silicon-valley">SJC to Palo Alto and Silicon Valley transfers</a> · <a href="/airports/sjc">SJC pickup guide</a></p>
    </article>
    <article class="card"><p class="renewal-kicker">Your return flight</p><h3>Work back from departure</h3>
      <p>Share the flight details, pickup entrance and hotel luggage collection. Agree on a pickup time using your airline's arrival guidance and conditions on your travel date.</p>
      <p><a href="/blog/sfo-oak-sjc-silicon-valley-business-trip">Compare SFO, OAK and SJC for a business trip</a></p>
    </article>
  </div>
</div></section>

<section class="renewal-section"><div class="wrap renewal-split">
  <figure class="renewal-image-panel"><img src="/img/fleet-sedan-hotel-scene.webp" alt="Black sedan outside a warmly lit hotel entrance" loading="lazy" decoding="async"></figure>
  <div>
    <p class="renewal-kicker">The local details</p><h2>A place name is a start.<br>The entrance makes the plan.</h2>
    <article class="renewal-trip-note"><h3>Downtown &amp; University Avenue</h3>
      <p>Share the hotel, restaurant or office address and the entrance where your party will meet. Include any luggage collection before departure.</p>
    </article>
    <article class="renewal-trip-note"><h3>Stanford visits</h3>
      <p>Name the actual building or visitor destination. Ask your host about vehicle access and the meeting point; campus activities and transportation need separate arrangements.</p>
      <p><a href="https://visit.stanford.edu/">Stanford visitor information</a> · <a href="https://transportation.stanford.edu/getting-around-bay/transportation-airports">Official airport-transportation guide</a></p>
    </article>
    <article class="renewal-trip-note"><h3>Research Park &amp; Sand Hill Road</h3>
      <p>For Stanford Research Park, name the office and entrance. For meetings on nearby Sand Hill Road in Menlo Park, send each full address, appointment time and the final destination.</p>
      <p><a href="/services/corporate-travel">Corporate and executive transportation</a></p>
    </article>
  </div>
</div></section>

<section class="renewal-section" id="plan-your-ride"><div class="wrap">
  <div class="sec-head"><p class="renewal-kicker">Choose your service</p><h2>One arrival. Or the whole meeting day.</h2></div>
  <div class="renewal-fact-grid">
    <article class="card"><h3>Point to point</h3><p>Arrange one journey with all agreed stops in the quote. A later return is a separate leg to confirm; a drop-off does not mean the car stays.</p></article>
    <article class="card"><h3>Hourly chauffeur</h3><p>For several appointments, share the meeting sequence, waiting gaps and finish time. Confirm the vehicle's service window and how changes are handled.</p><p><a href="/blog/hourly-chauffeur-vs-point-to-point-transfers">Compare hourly and point-to-point service</a></p></article>
    <article class="card"><h3>Your party &amp; bags</h3><p>Choose a sedan or SUV around your passengers, luggage and equipment. For a larger party, <a href="mailto:reserve@koastride.com">request a van, Sprinter or bus quote</a> and confirm the actual seating and luggage space.</p></article>
  </div>
</div></section>

<section class="renewal-section" id="reserve-ride"><div class="wrap renewal-split">
  <div><p class="renewal-kicker">Your ride, arranged</p><h2>Bring the itinerary.<br>We'll connect the journey.</h2>
    <p>Have your local travel date, flight details, pickup and destination entrances, passengers and bags ready. Include meeting stops, waiting needs and any return leg.</p>
    <p><a class="btn btn-orange" href="{quote}">Get a Palo Alto quote</a></p>
  </div>
  {booking_markup}
</div></section>
"""
