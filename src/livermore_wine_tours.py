"""Pure Livermore wine-transport brief; existing marketing components, no effects.

Renderer accepts trusted booking markup and the existing quote destination.
Sources and search intent: docs/livermore-search-20261113.md.
Visual contract: shared renewal classes; parent owns image derivatives and CSS.
Regional/illustrative card images do not represent the named winery estates.
"""
from html import escape

LIVERMORE_TITLE = "Livermore Valley Wine Tours with a Private Driver | Koast"
LIVERMORE_DESCRIPTION = (
    "Plan Livermore Valley wine tours with a private driver for your party. "
    "Choose tastings, arrange local or Bay Area pickup and confirm your return and quote."
)
LIVERMORE_FAQS = [
    ("How do Livermore wine tours with Koast work?",
     "Choose the winery experiences you want and confirm their opening and availability "
     "for your date. Arrange tasting reservations directly with each winery, then send "
     "your confirmations, pickup and return addresses and passenger needs for a private "
     "transportation quote. Confirm the vehicle, route and service window before reserving."),
    ("Are tasting reservations and fees included in the car booking?",
     "A transportation reservation does not reserve a tasting. Confirm the winery "
     "experience and its fees separately from your Koast quote. Reservation policies "
     "differ: Wente and Concannon encourage reservations, and Murrieta's Well recommends "
     "them for seated tastings. Check the current policy and availability for your date "
     "and party; do not assume a walk-in place is available."),
    ("Is this a private ride or a shared trolley tour?",
     "Koast arranges a chauffeured vehicle for your own party. This page does not sell "
     "seats on a shared trolley or train tour. Your winery experience may have its own "
     "format and other guests; a private car does not make the tasting private."),
    ("Can we start in Livermore, Pleasanton, San Francisco or San Jose?",
     "Request pickup from your hotel, home or another agreed address and include the "
     "full route in the quote. For a San Francisco or San Jose departure, include the "
     "journey to wine country and the return. For Livermore or Pleasanton lodging, "
     "name the property, entrance and return destination. Timing and availability "
     "must be confirmed for your travel date."),
    ("How many wineries should we visit, and will the driver stay?",
     "Choose the number after checking tasting durations, travel between the actual "
     "addresses, lunch and your required finish time. Request hourly service if you "
     "need a car between appointments, and confirm waiting and the return window. "
     "A one-way transfer does not reserve a car for the day, and there is no fixed "
     "number of tastings that suits every party."),
    ("What should we arrange for a group or guests with extra requirements?",
     "Send passengers, luggage, space for purchases and any child-seat, mobility or "
     "other requirements. Check the winery's experience-specific age, food, access "
     "and party-size policies separately from the vehicle. Vans, Sprinters and buses "
     "require a quote; confirm the actual seating, luggage space and pickup access "
     "before reserving."),
]


def render_livermore_body(booking_markup, quote_url):
    """Return body HTML; generator owns navigation, FAQ/schema and footer."""
    quote = escape(quote_url, quote=True)
    return f"""
<header class="renewal-hero renewal-cinema">
  <img class="renewal-hero-image" src="/img/renewal-vineyard-hero.jpg" alt="Illustrative California wine-country landscape" fetchpriority="high">
  <div class="wrap renewal-hero-content">
  <div class="crumbs"><a href="/">Home</a><span>/</span><a href="/services/wine-tours">Wine Tours</a><span>/</span>Livermore Valley</div>
    <div class="hero-copy">
      <p class="renewal-kicker">Livermore Valley &middot; Private chauffeur</p>
      <h1>Wine country.<br><span class="o">Your pace.</span></h1>
      <p class="lede">Livermore Valley wine tours. Your tastings, your party, your private driver.</p>
      <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:24px">
        <a class="btn btn-orange" href="{quote}">Get a Livermore quote</a>
        <a class="btn btn-ghost-light" href="#plan-your-tastings">Plan your winery stops</a>
      </div>
    </div>
  </div>
</header>

<section class="tight renewal-section" id="plan-your-tastings" style="scroll-margin-top:100px"><div class="wrap">
  <div class="sec-head"><span class="renewal-kicker">Livermore Valley tasting plans</span>
    <h2>Find your kind of wine day.</h2>
    <p>Compare the stops. Check each winery's experience, availability and tasting time. We'll connect your confirmed appointments.</p>
  </div>
  <div class="grid-3">
    <article class="renewal-winery-card card">
      <figure class="renewal-card-photo"><img src="/img/wt-livermore.jpg" alt="Livermore Valley regional landscape" loading="lazy"><figcaption>Livermore Valley &middot; Regional image</figcaption></figure>
      <h3>Wente Vineyards</h3>
      <p class="renewal-kicker">Arroyo Road</p><p><span class="pill">Reservations encouraged</span></p>
      <p><strong>5050 Arroyo Road, Livermore.</strong><br>Seated tastings. Confirm the experience and time.</p>
      <p><a href="https://wentevineyards.com/visit/">Plan your visit</a> · <a href="https://wentevineyards.com/contact-us/">Address &amp; contact</a></p>
    </article>
    <article class="renewal-winery-card card">
      <figure class="renewal-card-photo"><img src="/img/renewal-wine-terrace.jpg" alt="Illustrative wine-country terrace, not Concannon Vineyard" loading="lazy"><figcaption>Wine-country ambience &middot; Illustration</figcaption></figure>
      <h3>Concannon Vineyard</h3>
      <p class="renewal-kicker">Tesla Road</p><p><span class="pill">Walk-ins subject to seating</span></p>
      <p><strong>4590 Tesla Road, Livermore.</strong><br>Reservations are encouraged. Ask about larger parties.</p>
      <p><a href="https://concannon.wine/experiences/">Explore winery experiences</a></p>
    </article>
    <article class="renewal-winery-card card">
      <figure class="renewal-card-photo"><img src="/img/wt-livermore.jpg" alt="Livermore Valley regional landscape" style="object-position:80% center" loading="lazy"><figcaption>Livermore Valley &middot; Regional image</figcaption></figure>
      <h3>Murrieta's Well</h3>
      <p class="renewal-kicker">Mines Road</p><p><span class="pill">Seated reservations recommended</span></p>
      <p><strong>3005 Mines Road, Livermore.</strong><br>Patio and walk-up options vary by date.</p>
      <p><a href="https://murrietaswell.com/visit/">Explore winery experiences</a></p>
    </article>
  </div>
  <p style="margin-top:24px">More stops? Explore the <a href="https://www.lvwine.org/itinerary-planner.php">Livermore Valley itinerary planner</a> and <a href="https://www.lvwine.org/maps.php">winery maps</a>. Tasting reservations and fees are separate from transportation.</p>
</div></section>

<section class="tight renewal-section"><div class="wrap grid-2 renewal-split">
  <div>
    <span class="pill">Pickup and return</span><h2>Start locally or include the Bay Area journey</h2>
    <p><strong>Livermore or Pleasanton lodging:</strong> send the property name, street address and entrance. Include where you want to finish, whether that is the same hotel, dinner or another agreed destination.</p>
    <p><strong>San Francisco or San Jose:</strong> include both the trip to wine country and the return in the quote. Set pickup around the first confirmed tasting, check-in instructions and conditions for your travel day rather than a fixed drive-time estimate.</p>
    <p><strong>Between tastings:</strong> request an hourly chauffeur if you need the vehicle between appointments. Confirm driving, waiting and the return window. If you only need one transfer, describe that journey and arrange any later pickup separately.</p>
    <p>Compare our <a href="/blog/hourly-chauffeur-vs-point-to-point-transfers">hourly chauffeur and point-to-point options</a>, or review <a href="/cities/san-francisco">San Francisco</a> and <a href="/cities/san-jose">San Jose pickup planning</a>.</p>
  </div>
  <article class="card renewal-trip-note"><h3>Your stops. One private ride.</h3>
    <p><strong>Winery experiences:</strong> confirm each reservation, start and expected finish, address and party requirements with the winery. Tasting fees, food and purchases are separate from the transportation quote.</p>
    <p><strong>Transportation:</strong> confirm your vehicle, pickup, stops, waiting, required return time and change terms. A car booking does not hold a tasting appointment.</p>
    <p>Koast transportation is a private ride for your party. It is not a seat on a shared trolley or train tour, and it does not make a winery-hosted experience private.</p>
  </article>
</div></section>

<section class="tight renewal-section" id="quote-details" style="scroll-margin-top:100px"><div class="wrap grid-2 renewal-split">
  <div><span class="pill">Build a realistic tasting day</span><h2>Leave room for the visits you book</h2>
    <p>Use the actual tasting lengths, travel between entrances, lunch and required return to choose the number of stops. There is no fixed tasting count for every party. Confirm food plans and any winery-specific visitor rules before adding a lunch stop.</p>
    <p>Age, non-taster, mobility, food and larger-party arrangements can differ by experience. Ask each winery directly, then share the transportation requirements for the actual vehicle and route.</p>
    <p>Our <a href="/blog/group-wine-tour-planning">group wine-tour planning guide</a> helps put one brief together. For a van, Sprinter or bus, <a href="mailto:reserve@koastride.com">request a group quote</a> and confirm seating, luggage and access.</p>
  </div>
  <article class="card"><h3>Send these details for your transportation quote</h3>
    <ul class="check">
      <li>Travel date, pickup entrance and final return address</li>
      <li>Passengers, bags, purchases and any assistance requirements</li>
      <li>Winery names, actual addresses and confirmed tasting times</li>
      <li>Lunch or other stops and the time you must finish</li>
      <li>Whether you need one transfer or a chauffeur between visits</li>
    </ul>
    <p><a class="btn btn-orange" href="{quote}">Get a Livermore quote</a></p>
  </article>
</div></section>

<section class="tight renewal-section" id="reserve-ride" style="scroll-margin-top:100px"><div class="wrap renewal-split">
  <div><p class="renewal-kicker">Your wine day, connected</p><h2>Plan the ride around your reservations.</h2><p>Private transportation, hotel or home pickup by arrangement, and a vehicle and service window quoted before travel. Winery reservations and tasting fees are separate.</p></div>
  {booking_markup}
</div></section>
"""
