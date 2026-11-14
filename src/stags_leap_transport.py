"""Pure Stag's Leap transport copy, composed by generate.py's winery-page owner.

Inputs: trusted existing booking markup and the existing quote destination. Returns
body HTML only; the caller owns navigation, FAQ/schema, related links and footer.
Uses the public site's approved editorial renewal classes and existing buttons;
no external effects. The Napa-mapped image is regional, not an estate photograph.

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
<header class="renewal-hero renewal-editorial">
<div class="wrap">
  <div class="crumbs"><a href="/">Home</a><span>/</span><a href="/services/wine-tours">Wine Tours</a><span>/</span><a href="/wine-tours/napa-valley">Napa Valley</a><span>/</span>Stag's Leap Wine Cellars</div>
</div>
<div class="wrap renewal-editorial-grid">
  <div class="renewal-hero-content">
    <span class="renewal-kicker">Napa Valley &middot; Private transportation</span>
    <h1>Stag's Leap Wine Cellars.<br><span class="o">Leave the drive to us.</span></h1>
    <p class="lede">Your tasting, your own party, a private driver. Connect your hotel and winery reservation with a clear plan for the ride home.</p>
    <a class="btn btn-orange" href="{quote}">Get a transportation quote</a>
    <p class="renewal-trip-note"><a href="#small-group-planning">Plan your visit</a> &middot; <a href="#reserve-ride">Arrange your ride</a></p>
  </div>
  <figure class="renewal-hero-visual"><img class="renewal-hero-image" src="/img/blog-banner-napa.jpg" alt="Vineyard rows and a winding lane in warm evening light" width="1100" height="456" fetchpriority="high"><img class="renewal-photo-inset" src="/img/renewal-wine-terrace.jpg" alt="Illustrative wine-country terrace" width="1254" height="1254" loading="lazy"></figure>
</div>
</header>

<section class="renewal-section" id="small-group-planning"><div class="wrap">
  <span class="renewal-kicker">The experience comes first</span>
  <h2>Choose the tasting.<br>We connect the day.</h2>
  <div class="renewal-split">
    <article><h3>Reserve with the winery</h3>
      <p>Choose your experience and confirm your party size and availability directly with the winery. The Estate Wine Tasting &amp; Cave Tour is described as communal and requires reservations.</p>
      <p class="renewal-trip-note">Winery reservations, admission and tasting fees are separate. A private car does not make a communal winery experience private.</p>
    </article>
    <article><h3>Give the drive a plan</h3>
      <p>Share the tasting confirmation, hotel pickup entrance and return destination. Request a transfer for a single journey or hourly service between stops.</p>
      <p class="renewal-trip-note">Confirm the service window, included waiting and return pickup. A one-way ride does not reserve a car for the day.</p>
    </article>
  </div>
</div></section>

<section class="renewal-section"><div class="wrap">
  <span class="renewal-kicker">Your destination, confirmed</span>
  <h2>Similar names.<br>Different estates.</h2>
  <div class="renewal-fact-grid">
    <article><h3>Stag's Leap Wine Cellars</h3>
      <p><strong>5766 Silverado Trail, Napa, CA 94558.</strong></p>
      <p>The destination on this page. Match your confirmation to this address and confirm the winery's current visitor requirements before travel.</p>
    </article>
    <article><h3>Stags' Leap Winery</h3>
      <p><strong>6150 Silverado Trail, Napa, CA 94558.</strong></p>
      <p>A separate winery. If this is the estate on your reservation, send that full name and address and confirm its visitor requirements separately.</p>
    </article>
  </div>
</div></section>

<section class="renewal-section" id="transportation-details"><div class="wrap">
  <span class="renewal-kicker">A better day starts with the details</span>
  <h2>Three things to share.</h2>
  <div class="renewal-fact-grid">
    <article><h3>01 &middot; Where you start</h3>
      <p>Your date, hotel or home address, pickup entrance and winery check-in time. Napa and Yountville hotel pickups can be included in your request.</p>
    </article>
    <article><h3>02 &middot; How the day ends</h3>
      <p>Each reserved stop, expected finish, return address and required return time. Confirm the driving, waiting and changes covered by your quote.</p>
    </article>
    <article><h3>03 &middot; Who is coming</h3>
      <p>Your passengers, luggage and wine purchases. Winery party limits are separate from vehicle seating. Vans, Sprinters and buses require a quote.</p>
    </article>
  </div>
  <p class="renewal-trip-note">Planning more stops? Explore <a href="/wine-tours/napa-valley">Napa Valley private wine transportation</a> or compare <a href="/blog/hourly-chauffeur-vs-point-to-point-transfers">hourly service and separate transfers</a>.</p>
</div></section>

<section class="renewal-section" id="reserve-ride"><div class="wrap renewal-split">
  <div>
    <span class="renewal-kicker">Your winery day, connected</span>
    <h2>The tasting is yours.<br>The driving is ours.</h2>
    <p>Have your reservation details ready? Arrange transportation for your own party, with an agreed pickup and return plan.</p>
    <a class="btn btn-orange" href="{quote}">Plan my winery transportation</a>
    <p class="renewal-trip-note">Tasting reservations and fees are booked separately with the winery.</p>
  </div>
  {booking_markup}
</div></section>
"""
