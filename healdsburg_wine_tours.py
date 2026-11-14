"""Authored Healdsburg landing-page copy; pure markup, no provider or data effects.

Uses the existing marketing hero, cards, grids and FAQ components. Source/factual
review and Search Console baseline: docs/healdsburg-search-20261104.md.
Visual contract: shared renewal classes; parent owns image derivatives and CSS.
Regional/illustrative card images do not represent the named winery estates.
"""

HEALDSBURG_TITLE = "Healdsburg Winery Tours with a Private Driver | Koast"
HEALDSBURG_DESCRIPTION = (
    "Healdsburg winery tours with a private driver and vehicle. Plan local or Bay Area "
    "pickup, a focused wine-country route and separate tasting reservations."
)

HEALDSBURG_FAQS = [
    ("How do I book a private Healdsburg winery tour?",
     "Send your travel date, pickup and return addresses, guest count and preferred wineries. "
     "Include any tasting appointments already booked. Confirm the vehicle, service window "
     "and transportation quote, then keep each winery's separate reservation confirmation with your itinerary."),
    ("Are winery reservations and tasting fees included?",
     "Confirm the inclusions in your transportation quote and each winery booking. "
     "A car reservation does not confirm a tasting appointment. Ask who will book the tastings "
     "and whether tasting fees, food, purchases or other charges are included before paying."),
    ("How many wineries should we visit in one day?",
     "Choose the number after checking appointment lengths, travel between the actual addresses, "
     "lunch and your required return time. A focused route in one valley can leave more room "
     "for the booked experiences than trying to cover every wine area. There is no fixed tasting count for every trip."),
    ("Can we start in Healdsburg instead of San Francisco?",
     "Include the exact Healdsburg lodging or other proposed pickup address in your request. "
     "For a San Francisco departure, include the transfer to wine country and the return journey "
     "when agreeing on the service window. Pickup access, timing and availability must be confirmed for your date."),
    ("What vehicle should we request for a group wine tour?",
     "Send the full passenger count, luggage and any other requirements so the vehicle layout can be confirmed. "
     "Vans, Sprinters and buses require a quote. Passenger capacity alone does not establish space "
     "for luggage or wine purchases, and a larger vehicle's access must be checked with each winery."),
    ("Can children, non-tasters or guests with accessibility needs join?",
     "Check every winery's current age, non-taster and accessibility arrangements before reserving. "
     "Policies differ by winery and experience. Tell the transportation provider about child restraints, "
     "mobility equipment or other requirements and obtain confirmation for the actual vehicle and itinerary."),
]


def render_healdsburg_body(booking_markup):
    """Return this page's header and planning sections with the existing booking card."""
    return f"""
<header class="renewal-hero renewal-cinema">
  <img class="renewal-hero-image" src="/img/wt-healdsburg.jpg" alt="Downtown Healdsburg and its plaza" fetchpriority="high">
  <div class="wrap renewal-hero-content">
  <div class="crumbs"><a href="/">Home</a><span>/</span><a href="/services/wine-tours">Wine Tours</a><span>/</span>Healdsburg</div>
    <div class="hero-copy">
      <p class="renewal-kicker">Healdsburg &middot; Your private wine day</p>
      <h1>Healdsburg winery tours <span class="o">with a private chauffeur.</span></h1>
      <p class="lede">Your chosen tastings. Your own party. A private driver connecting Healdsburg or Bay Area pickup, winery appointments and your return.</p>
      <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:24px">
        <a class="btn btn-orange btn-lg" href="mailto:reserve@koastride.com">Email for a wine-tour quote</a>
        <a class="btn btn-ghost-light btn-lg" href="#choose-your-route">Compare winery routes</a>
      </div>
      <p style="font-size:16px;margin-top:16px;color:#cdd3dc">Have tasting times already? <a href="#quote-details" style="color:inherit;text-decoration:underline">See what to send for your transportation quote.</a></p>
    </div>
  </div>
</header>

<section class="tight renewal-section" id="choose-your-route" style="scroll-margin-top:100px"><div class="wrap">
  <div class="sec-head"><span class="renewal-kicker">Choose your wine country</span>
    <h2>Discover your next stop.</h2>
    <p>Dry Creek, Alexander Valley, Russian River or a tasting room in town. Compare the experiences, then connect appointments that fit your day.</p>
  </div>
  <div class="grid-3">
    <article class="renewal-winery-card card">
      <figure class="renewal-card-photo"><img src="/img/renewal-vineyard-hero.jpg" alt="Illustrative California wine-country landscape, not a Dry Creek estate" loading="lazy"><figcaption>Wine-country landscape &middot; Illustration</figcaption></figure>
      <h3>Dry Creek Valley</h3>
      <p><span class="pill">Zinfandel-focused visits</span></p>
      <p>Compare appointments at <a href="/wineries/ridge-vineyards-lytton-springs">Ridge Lytton Springs</a> and <a href="/wineries/dry-creek-vineyard">Dry Creek Vineyard</a>. Check the route and lunch gap against confirmed times.</p>
      <p><a href="/wine-tours/sonoma">Compare Sonoma wine tour planning</a> or explore the <a href="https://www.drycreekvalley.org/dry-creek-valley/">Dry Creek Valley winegrowers' guide</a>.</p>
    </article>
    <article class="renewal-winery-card card">
      <figure class="renewal-card-photo"><img src="/img/renewal-wine-terrace.jpg" alt="Illustrative wine-country terrace, not an Alexander Valley estate" loading="lazy"><figcaption>Wine-country ambience &middot; Illustration</figcaption></figure>
      <h3>Alexander Valley</h3>
      <p><span class="pill">Estate appointments</span></p>
      <p>Consider a booked estate experience such as Jordan. Choose the available experience first, then arrange the day around it rather than assuming a drop-in visit.</p>
      <p>Read our <a href="/wineries/jordan-vineyard-and-winery">Jordan planning guide</a> and check <a href="https://www.jordanwinery.com/visit/">Jordan's current visits and reservations</a>.</p>
    </article>
    <article class="renewal-winery-card card">
      <figure class="renewal-card-photo"><img src="/img/wt-healdsburg.jpg" alt="Downtown Healdsburg regional scene" loading="lazy"><figcaption>Healdsburg area &middot; Regional image</figcaption></figure>
      <h3>Russian River Valley</h3>
      <p><span class="pill">Pinot Noir &amp; Chardonnay</span></p>
      <p>Compare producers along a route that suits your pickup. Check actual addresses before adding another valley or a meal in town.</p>
      <p>Read our <a href="/wineries/gary-farrell-vineyards-and-winery">Gary Farrell planning guide</a>, explore the <a href="https://russianrivervalley.org/about/neighborhoods/">Russian River Valley neighborhoods</a>, or compare <a href="/wineries/">Koast's winery planning directory</a>.</p>
    </article>
  </div>
  <p style="color:var(--muted);margin-top:24px">Prefer an afternoon in town? The <a href="https://stayhealdsburg.com/wine-country/">official Healdsburg wine-country guide</a> also lists downtown tasting rooms. Confirm whether each stop is a town tasting room or an estate visit before arranging transportation.</p>
</div></section>

<section class="tight renewal-section"><div class="wrap grid-2 renewal-split">
  <div>
    <span class="renewal-kicker">Estate visits &amp; tasting appointments</span>
    <h2>Build the itinerary around confirmed reservations</h2>
    <p>Start with your preferred experience, then fit other stops around its duration, travel, lunch and return. Check each winery's group limits and visitor requirements.</p>
    <ul class="check">
      <li><strong>Jordan:</strong> advance appointments are required; confirm the particular tour or tasting you want.</li>
      <li><strong>Ridge Lytton Springs:</strong> reserve the particular experience and check its party-size and visitor requirements before arranging the vehicle.</li>
      <li><strong>Dry Creek Vineyard:</strong> reservations are strongly encouraged; larger parties should contact its concierge.</li>
    </ul>
    <p><a href="https://www.ridgewine.com/visit/lytton-springs/">Ridge visitor guidance</a> · <a href="https://drycreekvineyard.com/visit/">Dry Creek Vineyard reservations</a></p>
  </div>
  <div class="card renewal-trip-note">
    <h3>One focused route to consider</h3>
    <p>Pair an available Ridge Lytton Springs appointment with a separately confirmed Dry Creek Vineyard visit, leaving room for lunch and the return. This planning example is subject to availability; it reserves neither winery and promises no fixed stop count.</p>
    <p>Keep two confirmations: <strong>transportation</strong> for the vehicle and service window, and <strong>winery appointments</strong> for the experiences. Agree who is responsible for booking each one and what each price includes.</p>
    <p>For the broader reservation checklist, see <a href="/blog/napa-tasting-and-transportation-reservations">coordinating tastings and transportation</a>; its Napa examples illustrate the same confirmation process.</p>
  </div>
</div></section>

<section class="tight renewal-section"><div class="wrap grid-2 renewal-split">
  <div>
    <span class="renewal-kicker">Pickup &amp; return</span>
    <h2>Starting in Healdsburg or traveling from San Francisco?</h2>
    <p><strong>Staying in Healdsburg:</strong> send your lodging address, the first tasting time and where you want to finish. Confirm the property's pickup entrance and whether the final stop is your hotel, dinner or another agreed destination.</p>
    <p><strong>Downtown tasting room or winery estate:</strong> use the address in each tasting confirmation, including any entrance instructions. A winery name alone does not tell your driver which location or arrival point you booked.</p>
    <p><strong>Starting in San Francisco or elsewhere in the Bay Area:</strong> include both the drive to wine country and the journey home. Check traffic for the travel date and route, then agree on a pickup time that protects the first appointment. A fixed drive-time estimate is not a confirmed pickup plan.</p>
    <p>Review <a href="/cities/san-francisco">San Francisco transportation</a> and <a href="/services/wine-tours">Koast wine tour service</a> when comparing the complete trip.</p>
    <p><strong>Driver for the day or a transfer:</strong> request a chauffeured service window if you need transport between appointments and a return journey. If you only need a ride to or from Healdsburg, describe those transfer legs instead. The quote should state what the vehicle and driver cover.</p>
  </div>
  <div class="card" id="quote-details" style="scroll-margin-top:100px">
    <h3>Send these details for a transportation quote</h3>
    <ul class="check">
      <li>Travel date, pickup and final return addresses</li>
      <li>Passenger count, bags and any equipment or assistance requirements</li>
      <li>Confirmed tasting names, addresses and start/end times</li>
      <li>Lunch plans and the time you need to be back</li>
      <li>Any vehicle preference and space needed for purchases</li>
    </ul>
    <p>Ask for the vehicle, service window, inclusions and change terms in the quote. For a van, Sprinter or bus, <a href="mailto:reserve@koastride.com">request a group quote</a> and have winery access and the actual seating layout checked.</p>
    <p><a href="/blog/group-wine-tour-planning">Plan a group wine tour</a> with the full party's requirements in one brief.</p>
    <p><a class="btn btn-orange btn-lg" href="mailto:reserve@koastride.com">Email your wine-tour plans</a></p>
  </div>
</div></section>

<section class="tight renewal-section" id="reserve-ride" style="scroll-margin-top:100px"><div class="wrap renewal-split">
  <div><p class="renewal-kicker">Your wine day, connected</p><h2>Choose the stops. Confirm the ride.</h2><p>Private transportation from Healdsburg lodging or the Bay Area by arrangement. Confirm the vehicle, service window and itinerary before travel; keep each winery's separate reservation confirmation.</p></div>
  {booking_markup}
</div></section>
"""
