"""Authored Healdsburg landing-page copy; pure markup, no provider or data effects.

Uses the existing marketing hero, cards, grids and FAQ components. Source/factual
review and Search Console baseline: docs/healdsburg-search-20261104.md.
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
<header class="hero-dark"><div class="wrap">
  <div class="crumbs"><a href="/">Home</a><span>/</span><a href="/services/wine-tours">Wine Tours</a><span>/</span>Healdsburg</div>
  <div class="hero-grid">
    <div class="hero-copy">
      <h1>Healdsburg winery tours <span class="o">with a private chauffeur.</span></h1>
      <p class="lede">Visit wine country with a private driver and chauffeured vehicle for your group. Start from Healdsburg or arrange Bay Area pickup, choose your tasting appointments, and confirm the complete route and return plan before you travel.</p>
      <ul class="check">
        <li>Private transportation for your planned winery visits</li>
        <li>Pickup from Healdsburg lodging or the Bay Area by arrangement</li>
        <li>Vehicle, service window and itinerary confirmed before travel</li>
      </ul>
      <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:24px">
        <a class="btn btn-orange btn-lg" href="mailto:reserve@koastride.com">Email for a wine-tour quote</a>
        <a class="btn btn-ghost-light btn-lg" href="#choose-your-route">Compare winery routes</a>
      </div>
      <p style="font-size:16px;margin-top:16px;color:#cdd3dc">Have tasting times already? <a href="#quote-details" style="color:inherit;text-decoration:underline">See what to send for your transportation quote.</a></p>
    </div>
    {booking_markup}
  </div>
</div></header>

<section class="tight" id="choose-your-route" style="scroll-margin-top:100px"><div class="wrap">
  <div class="sec-head"><span class="pill">Choose your wine country</span>
    <h2>Which Healdsburg wine area fits your day?</h2>
    <p>Healdsburg is a base for three nearby wine areas, plus downtown tasting rooms. Start with the wines or experience you want, then connect appointments that work together geographically. A visit to every valley is not a requirement.</p>
  </div>
  <div class="grid-3">
    <div class="card">
      <h3>Dry Creek Valley</h3>
      <p>A starting point for Zinfandel-focused visits. Compare appointment options at <a href="/wineries/ridge-vineyards-lytton-springs">Ridge Lytton Springs</a> and <a href="/wineries/dry-creek-vineyard">Dry Creek Vineyard</a>, then check the route and a lunch gap against your confirmed times.</p>
      <p><a href="/wine-tours/sonoma">Compare Sonoma wine tour planning</a> or explore the <a href="https://www.drycreekvalley.org/dry-creek-valley/">Dry Creek Valley winegrowers' guide</a>.</p>
    </div>
    <div class="card">
      <h3>Alexander Valley</h3>
      <p>Consider a booked estate experience such as Jordan. Choose the experience and its available time first; arrange the rest of the day around that appointment instead of assuming you can drop in.</p>
      <p>Read our <a href="/wineries/jordan-vineyard-and-winery">Jordan planning guide</a> and check <a href="https://www.jordanwinery.com/visit/">Jordan's current visits and reservations</a>.</p>
    </div>
    <div class="card">
      <h3>Russian River Valley</h3>
      <p>Compare Pinot Noir and Chardonnay producers along a route that suits your pickup point. Check the actual winery addresses before combining visits with another valley or a meal in town.</p>
      <p>Read our <a href="/wineries/gary-farrell-vineyards-and-winery">Gary Farrell planning guide</a>, explore the <a href="https://russianrivervalley.org/about/neighborhoods/">Russian River Valley neighborhoods</a>, or compare <a href="/wineries/">Koast's winery planning directory</a>.</p>
    </div>
  </div>
  <p style="color:var(--muted);margin-top:24px">Prefer an afternoon in town? The <a href="https://stayhealdsburg.com/wine-country/">official Healdsburg wine-country guide</a> also lists downtown tasting rooms. Confirm whether each stop is a town tasting room or an estate visit before arranging transportation.</p>
</div></section>

<section class="tight"><div class="wrap grid-2" style="align-items:start;gap:40px">
  <div>
    <span class="pill">Estate visits &amp; tasting appointments</span>
    <h2>Build the itinerary around confirmed reservations</h2>
    <p>Pick the experience you most want to book, then check the other stops around it. Include the full tasting duration, travel between entrances, lunch and the return journey. Check group limits and visitor requirements with each winery.</p>
    <ul class="check">
      <li><strong>Jordan:</strong> advance appointments are required; confirm the particular tour or tasting you want.</li>
      <li><strong>Ridge Lytton Springs:</strong> reserve the particular experience and check its party-size and visitor requirements before arranging the vehicle.</li>
      <li><strong>Dry Creek Vineyard:</strong> reservations are strongly encouraged; larger parties should contact its concierge.</li>
    </ul>
    <p><a href="https://www.ridgewine.com/visit/lytton-springs/">Ridge visitor guidance</a> · <a href="https://drycreekvineyard.com/visit/">Dry Creek Vineyard reservations</a></p>
  </div>
  <div class="card">
    <h3>One focused route to consider</h3>
    <p>A Dry Creek day might pair an available Ridge Lytton Springs appointment with a separately confirmed Dry Creek Vineyard visit. Add lunch only after checking the appointment lengths, transfer and return plan.</p>
    <p>This is a planning example, subject to availability. It does not reserve either winery or promise a particular number of stops.</p>
    <p>Keep two confirmations: <strong>transportation</strong> for the vehicle and service window, and <strong>winery appointments</strong> for the experiences. Agree who is responsible for booking each one and what each price includes.</p>
    <p>For the broader reservation checklist, see <a href="/blog/napa-tasting-and-transportation-reservations">coordinating tastings and transportation</a>; its Napa examples illustrate the same confirmation process.</p>
  </div>
</div></section>

<section class="tight"><div class="wrap grid-2" style="align-items:start;gap:40px">
  <div>
    <span class="pill">Pickup &amp; return</span>
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
"""
