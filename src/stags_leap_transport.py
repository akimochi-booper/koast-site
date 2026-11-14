"""Pure Stag's Leap transport copy, composed by generate.py's winery-page owner.

Inputs: trusted existing booking markup and the existing quote destination. Returns
body HTML only; the caller owns navigation, FAQ/schema, related links and footer.
Uses existing marketing hero/cards/buttons in css/main.css; no external effects.

Intent: answer small-group planning without selling winery admission or shared tours.
Official sources checked 2026-11-13 (experience details/availability may change):
https://www.stagsleapwinecellars.com/visit-us/
https://www.stagsleapwinecellars.com/visit-us/experiences/
https://www.stagsleapwinecellars.com/experience/estate-tour-tasting/
https://www.stagsleapwinecellars.com/contact-us/
https://www.stagsleap.com/pages/visit
"""
from html import escape

STAGS_LEAP_TITLE = "Stag's Leap Wine Cellars Private Driver & Transport | Koast"
STAGS_LEAP_DESCRIPTION = (
    "Plan a Stag's Leap Wine Cellars visit with a private driver. Separate tasting "
    "reservations, small-party transport, hotel pickup and a clear return plan."
)

STAGS_LEAP_FAQS = [
    ("Are there small-group tours available in Stags Leap?",
     "Stag's Leap Wine Cellars lists winery-hosted tasting and tour experiences, "
     "including communal experiences. Check the winery's current format, party limit "
     "and availability, and reserve directly. Koast provides private transportation "
     "for your own party; it does not sell seats on a shared or join-in tour. "
     "A private car does not make the winery experience private."),
    ("Do I book the winery tasting and the car separately?",
     "Yes. Reserve your tasting or tour directly with Stag's Leap Wine Cellars, then "
     "share the confirmed date, check-in instructions, start time and expected finish "
     "when arranging transportation. Winery admission and tasting fees are separate "
     "from the Koast transportation quote. The winery requires all visitors to be "
     "at least 21, including anyone who is not tasting."),
    ("Is Stag's Leap Wine Cellars the same as Stags' Leap Winery?",
     "No. Stag's Leap Wine Cellars is at 5766 Silverado Trail in Napa. Stags' Leap "
     "Winery is a different estate at 6150 Silverado Trail in Napa. Send the full "
     "winery name and the address on your reservation so your driver reaches the "
     "correct destination."),
    ("Can you pick us up at our Napa Valley hotel?",
     "Request pickup from your hotel or another agreed address, including Napa or "
     "Yountville. Provide the property name, full street address, entrance and any "
     "loading instructions. Include the winery appointment and return destination "
     "so the quote covers the complete route and service window."),
    ("Should I book a transfer or an hourly private driver?",
     "Request a transfer for a single journey, or list both journeys if you need a "
     "return pickup. For a car between winery stops, request hourly service and "
     "confirm the service window, included waiting and return time. A one-way "
     "transfer does not reserve a car for the rest of the day."),
    ("How do I choose a vehicle for a small party or a larger group?",
     "Send the passenger count, luggage, any wine purchases and the full itinerary "
     "to choose a suitable vehicle. Confirm the winery's party-size rules separately "
     "from the vehicle's seating. Vans, Sprinters and buses require a quote; confirm "
     "the actual seating, luggage space and pickup arrangements before reserving."),
]


def render_body(booking_markup, quote_url):
    """Return body HTML around trusted booking markup; escape the quote URL attribute."""
    quote = escape(quote_url, quote=True)
    return f"""
<header class="hero-dark"><div class="wrap">
  <div class="crumbs"><a href="/">Home</a><span>/</span><a href="/services/wine-tours">Wine Tours</a><span>/</span><a href="/wine-tours/napa-valley">Napa Valley</a><span>/</span>Stag's Leap Wine Cellars</div>
  <div class="hero-grid">
    <div class="hero-copy">
      <span class="wy-eyebrow">Napa Valley &middot; Stags Leap District</span>
      <h1>Stag's Leap Wine Cellars <span class="o">with a private driver.</span></h1>
      <p class="lede">Plan the ride around your confirmed winery reservation. A private car for your own party, hotel pickup and an agreed return plan let everyone leave the driving to a chauffeur.</p>
      <ul class="check">
        <li>Private transportation for couples and small parties</li>
        <li>Tasting reservations and admission booked separately</li>
        <li>One transfer or a quoted hourly service window</li>
      </ul>
      <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:24px">
        <a class="btn btn-orange" href="{quote}">Get a transportation quote</a>
        <a class="btn btn-ghost-light" href="#small-group-planning">Plan a small-group visit</a>
      </div>
    </div>
    {booking_markup}
  </div>
</div></header>

<section class="tight" id="small-group-planning" style="scroll-margin-top:100px"><div class="wrap">
  <div class="sec-head"><span class="pill">Small-group planning</span>
    <h2>A winery experience and a private ride are separate reservations.</h2>
    <p>Visiting with a small party? Start with the winery's tasting or tour, then arrange the car around its confirmed schedule. Koast transportation is for your own party, rather than seats on a shared or join-in tour.</p>
  </div>
  <div class="grid-2">
    <article class="card"><h3>Choose your winery experience</h3>
      <p>The estate's <a href="https://www.stagsleapwinecellars.com/visit-us/experiences/">official experiences page</a> describes vineyard-view tastings and cave experiences. Its <a href="https://www.stagsleapwinecellars.com/experience/estate-tour-tasting/">Estate Wine Tasting &amp; Cave Tour</a> is described as communal and requires reservations. Ask the winery about the current format, your party size and availability before confirming a visit.</p>
      <p>A private vehicle does not make the tasting or tour private. Winery reservations, admission and tasting fees are separate from the transportation quote.</p>
    </article>
    <article class="card"><h3>Arrange the driver and return</h3>
      <p>Send the tasting confirmation, pickup address and return destination. For a hotel in Napa or Yountville, name the entrance and any loading instructions rather than only the property.</p>
      <p>Choose a transfer for one journey or request an hourly driver for time between stops. Agree on the service window, included waiting and return pickup; a one-way ride does not reserve a car for the day.</p>
    </article>
  </div>
</div></section>

<section class="tight"><div class="wrap">
  <div class="sec-head"><span class="pill">Check the destination</span>
    <h2>Two similar names. Two different estates.</h2>
    <p>Use the full winery name and address from your confirmation when requesting the car.</p>
  </div>
  <div class="grid-2">
    <article class="card"><h3>Stag's Leap Wine Cellars</h3>
      <p><strong>5766 Silverado Trail, Napa, CA 94558.</strong> This page plans transportation to Wine Cellars. Check the estate's <a href="https://www.stagsleapwinecellars.com/contact-us/">official address</a> and <a href="https://www.stagsleapwinecellars.com/visit-us/">visitor guidance</a> alongside your reservation.</p>
    </article>
    <article class="card"><h3>Stags' Leap Winery</h3>
      <p><strong>6150 Silverado Trail, Napa, CA 94558.</strong> This is a different winery. If your confirmation names Stags' Leap Winery, use its <a href="https://www.stagsleap.com/pages/visit">official visit page</a> and tell us that full name and address.</p>
    </article>
  </div>
</div></section>

<section class="tight" id="transportation-details" style="scroll-margin-top:100px"><div class="wrap">
  <div class="sec-head"><span class="pill">Your transportation quote</span>
    <h2>Build the ride around the appointment.</h2>
  </div>
  <div class="grid-3">
    <article class="card"><h3>Pickup and check-in</h3>
      <p>Provide the date, hotel or home address, pickup entrance and winery check-in instructions. Plan pickup around the confirmed appointment and route for your travel day.</p>
    </article>
    <article class="card"><h3>Stops and service window</h3>
      <p>List each reserved winery, lunch stop and expected finish. Include the return address and required return time, then confirm the driving, waiting and any itinerary changes in the quote.</p>
    </article>
    <article class="card"><h3>People, bags and vehicle</h3>
      <p>Share passengers, luggage and space needed for wine purchases. Check the winery's party limit separately from vehicle seating. Vans, Sprinters and buses require a quote.</p>
    </article>
  </div>
  <p style="margin-top:24px">Planning a wider route? See <a href="/wine-tours/napa-valley">Napa Valley private wine transportation</a> and our <a href="/blog/hourly-chauffeur-vs-point-to-point-transfers">hourly chauffeur versus separate transfers guide</a>.</p>
  <a class="btn btn-orange" href="{quote}">Plan my winery transportation</a>
</div></section>
"""
