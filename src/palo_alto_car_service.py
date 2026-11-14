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
    """Render the local service brief around the unchanged native booking card/link."""
    quote = escape(quote_url, quote=True)
    return f"""
<header class="hero-dark"><div class="wrap">
  <div class="crumbs"><a href="/">Home</a><span>/</span><a href="/cities/">Cities</a><span>/</span>Palo Alto</div>
  <div class="hero-grid">
    <div class="hero-copy">
      <h1>Palo Alto car service <span class="o">for SFO, SJC &amp; business travel.</span></h1>
      <p class="lede">A private chauffeur for your airport arrival, Stanford visit or Silicon Valley meeting day. Arrange the complete route, choose a vehicle for your party and travel with a fixed transportation quote.</p>
      <ul class="check">
        <li>Flight-tracked SFO and SJC airport transfers</li>
        <li>Downtown Palo Alto, Stanford and nearby Sand Hill Road</li>
        <li>One transfer or an hourly meeting itinerary</li>
      </ul>
      <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:24px">
        <a class="btn btn-orange" href="{quote}">Get a Palo Alto quote</a>
        <a class="btn btn-ghost-light" href="#airport-options">Compare airport transfers</a>
      </div>
    </div>
    {booking_markup}
  </div>
</div></header>

<section class="tight" id="airport-options" style="scroll-margin-top:100px"><div class="wrap">
  <div class="sec-head"><span class="pill">Palo Alto airport transfers</span>
    <h2>SFO or SJC to Palo Alto?</h2>
    <p>Compare the flight schedule and the actual address you need to reach. Both airports can serve a Palo Alto trip; the right ground plan depends on your arrival time, hotel and first appointment.</p>
  </div>
  <div class="grid-3">
    <article class="card"><h3>SFO to Palo Alto</h3>
      <p>Send the flight number and local arrival date, then name the hotel, Stanford building or office entrance. Include passengers, bags and any intermediate stop so the quote covers the whole journey.</p>
      <p>Review <a href="/routes/sfo-to-silicon-valley">SFO to Palo Alto and Silicon Valley transfers</a> and the <a href="/airports/sfo">SFO pickup guide</a>.</p>
    </article>
    <article class="card"><h3>SJC to Palo Alto</h3>
      <p>Arrange a direct ride from San Jose Airport to your Palo Alto destination. For a trip continuing to Menlo Park, Mountain View or another meeting, list each address before confirming the transfer.</p>
      <p>Plan <a href="/routes/sjc-to-silicon-valley">SJC to Palo Alto and Silicon Valley transfers</a> with the <a href="/airports/sjc">SJC pickup guide</a>.</p>
    </article>
    <article class="card"><h3>Palo Alto to the airport</h3>
      <p>For the return, send the flight departure details and exact pickup entrance. Add hotel luggage collection or another stop to the plan, then agree on the pickup time with your airport arrival target in mind.</p>
      <p>Comparing flights? Use our <a href="/blog/sfo-oak-sjc-silicon-valley-business-trip">SFO, OAK and SJC business-trip guide</a>.</p>
    </article>
  </div>
</div></section>

<section class="tight"><div class="wrap">
  <div class="sec-head"><span class="pill">Local pickup details</span>
    <h2>Make the address useful to your chauffeur</h2>
    <p>A street address and the right entrance make a clearer plan than a campus or company name alone. Share the destination's own access instructions when you book.</p>
  </div>
  <div class="grid-3">
    <article class="card"><h3>Downtown &amp; University Avenue</h3>
      <p>For a hotel, restaurant or downtown office, include the property name and street address. Identify the entrance where your party will meet and any luggage collection needed before departure.</p>
    </article>
    <article class="card"><h3>Stanford visits</h3>
      <p>Use the actual building or visitor destination rather than just “Stanford.” Ask your host about vehicle access and the meeting point. Campus activities and transportation need separate arrangements.</p>
      <p>Check <a href="https://visit.stanford.edu/">Stanford's visitor information</a> and its <a href="https://transportation.stanford.edu/getting-around-bay/transportation-airports">official airport-transportation guide</a>.</p>
    </article>
    <article class="card"><h3>Research Park &amp; Sand Hill Road</h3>
      <p>For Stanford Research Park appointments, name the office and entrance. For nearby Menlo Park or Sand Hill Road meetings, include each full address and appointment time, plus where the day should finish.</p>
      <p>Planning a roadshow? Review <a href="/services/corporate-travel">corporate and executive transportation</a>.</p>
    </article>
  </div>
</div></section>

<section class="tight" id="plan-your-ride"><div class="wrap grid-2" style="align-items:start;gap:40px">
  <div>
    <span class="pill">Choose the service</span>
    <h2>One airport ride or a full meeting day?</h2>
    <p><strong>One journey:</strong> book a point-to-point transfer with all agreed stops in the quote. A later return is a separate leg to arrange.</p>
    <p><strong>Several appointments:</strong> request an hourly chauffeur and send the meeting sequence, waiting gaps and required finish time. Confirm the vehicle's service window rather than assuming it stays after a one-way drop-off.</p>
    <p>Our <a href="/blog/hourly-chauffeur-vs-point-to-point-transfers">hourly versus point-to-point guide</a> helps compare the two. For a larger party, <a href="mailto:reserve@koastride.com">request a van, Sprinter or bus quote</a> with the full passenger and luggage requirements.</p>
  </div>
  <div class="card"><h3>Have these details ready for your quote</h3>
    <ul class="check">
      <li>Local travel date, airport code and flight number where applicable</li>
      <li>Exact pickup, drop-off and building entrances</li>
      <li>Passengers, bags, equipment and any child-seat requirements</li>
      <li>Meeting stops, waiting needs and the time you must finish</li>
      <li>Any return leg, including hotel luggage collection</li>
    </ul>
    <p><a class="btn btn-orange" href="{quote}">Get a Palo Alto quote</a></p>
  </div>
</div></section>
"""
