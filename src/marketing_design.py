"""Public marketing presentation, composed before metadata enhancement.

No provider, booking or tracking effects. Existing authored copy, booking markup,
canonical identity and FAQ remain owned by the generator/route renderers.
"""
from html import escape
from html.parser import HTMLParser
import re
from src.wine_designs import reference_nav, render_reference_top


def group_vehicle_options(email):
    """Illustrative group travel choices; never an assigned vehicle or capacity."""
    contact = escape('mailto:' + email, quote=True)
    return f'''<div class="renewal-vehicle-options">
      <article class="renewal-vehicle-card"><img src="/img/fleet-sprinter-wine-tour-scene.webp" alt="Illustrative black van in wine country" loading="lazy">
      <div><h3>A day together</h3><p>Vans &amp; Sprinters · Quote required</p><a href="{contact}">Plan a group ride</a></div></article>
      <article class="renewal-vehicle-card"><img src="/img/fleet-large-party-bus-events-scene.webp" alt="Illustrative bus for a group occasion" loading="lazy">
      <div><h3>A bigger occasion</h3><p>Buses · Quote required</p><a href="{contact}">Request a bus quote</a></div></article>
      <p class="renewal-vehicle-note">Illustrative scenes. Confirm the actual vehicle, seating, luggage space and venue access in your quote.</p>
    </div>'''


class _Elements(HTMLParser):
    """Locate balanced authored elements without regex-parsing nested divs."""
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source, self.elements, self.stack = source, [], []
        self.lines = [0]
        self.lines.extend(m.end() for m in re.finditer("\n", source))
        self.feed(source)

    def source_offset(self):
        line, column = self.getpos()
        return self.lines[line - 1] + column

    def handle_starttag(self, tag, attrs):
        start = self.source_offset()
        item = dict(tag=tag, attrs=dict(attrs), start=start,
                    inner_start=start + len(self.get_starttag_text()))
        if tag not in self.VOID:
            self.stack.append(item)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                item = self.stack[i]
                del self.stack[i:]
                item.update(inner_end=self.source_offset(), end=self.source_offset() + len(tag) + 3)
                self.elements.append(item)
                break

    def first(self, *, tag=None, cls=None):
        return next((n for n in sorted(self.elements, key=lambda n: n["start"])
                     if (tag is None or n["tag"] == tag)
                     and (cls is None or cls in n["attrs"].get("class", "").split())), None)

    def html(self, node, inner=False):
        return self.source[node["inner_start"]:node["inner_end"]] if inner else self.source[node["start"]:node["end"]]


def _hero(source, image, image_alt, family, quote_url):
    tree = _Elements(source)
    header = tree.first(tag="header")
    if not header or "renewal-hero" in header["attrs"].get("class", ""):
        return source
    fragment = tree.html(header)
    parts = _Elements(fragment)
    copy = parts.first(cls="hero-copy")
    if copy:
        content = parts.html(copy, inner=True)
    else:
        # Keep account-inquiry links and other functional hero content intact.
        wrap = parts.first(cls="wrap")
        content = parts.html(wrap, inner=True) if wrap else parts.html(parts.first(tag="header"), inner=True)
        content_parts = _Elements(content)
        duplicate_crumbs = content_parts.first(cls="crumbs")
        if duplicate_crumbs:
            content = content[:duplicate_crumbs["start"]] + content[duplicate_crumbs["end"]:]
    if not content:
        return source
    crumbs = parts.first(cls="crumbs")
    crumbs = parts.html(crumbs) if crumbs else ""
    copy_parts = _Elements(content)
    checks = copy_parts.first(cls="check")
    highlights = copy_parts.html(checks) if checks else ""
    if checks:
        content = content[:checks["start"]] + content[checks["end"]:]
    # Existing airport figure is displayed in the main picture slot instead.
    copy_parts = _Elements(content)
    figure = copy_parts.first(cls="airport-hero-photo")
    if figure:
        content = content[:figure["start"]] + content[figure["end"]:]
    if not re.search(r'class="[^"]*\bbtn\b', content):
        button_label = 'Request a group quote' if family == 'event' else 'Plan my ride'
        content += f'<a class="btn btn-orange btn-lg" href="{escape(quote_url, quote=True)}">{button_label}</a>'
    title = {"wine":"Wine country · Your private ride", "winery":"A place worth the journey",
             "city":"Your city. Your schedule.", "airport":"From arrival to wherever is next.",
             "home":"Private chauffeurs · Nationwide", "service":"Make the journey part of the occasion.",
             "route":"A better way between places"}.get(family, "Go somewhere good.")
    mode = "gallery" if family == "event" else ("cinema" if family in {"wine", "home"} else "editorial")
    eyebrow = '' if re.search(r'class="(?:wy-eyebrow|airport-eyebrow)"', content) else f'<p class="renewal-kicker">{title}</p>'
    photo = f'<img class="renewal-hero-image" src="/{escape(image, quote=True)}" alt="{escape(image_alt, quote=True)}" fetchpriority="high">'
    if family == 'winery':
        photo += '<img class="renewal-photo-inset" src="/img/renewal-wine-terrace.jpg" alt="Illustrative wine-country terrace" width="1254" height="1254" loading="lazy">'
    hero = f'''<header class="renewal-hero renewal-{mode}">
      <div class="wrap renewal-editorial-grid">
        <div class="renewal-hero-content">{crumbs}{eyebrow}{content}</div>
        <figure class="renewal-hero-visual">{photo}</figure>
      </div></header>'''
    if highlights:
        hero += f'<section class="renewal-highlights"><div class="wrap">{highlights}</div></section>'
    booking = parts.first(cls="book-card")
    if booking:
        # The live quote widget is retained intact; it opens only when requested.
        hero += f'''<section class="renewal-booking-section"><div class="wrap">
          <details class="renewal-booking" id="reserve-ride"><summary>Get a quote for your trip</summary>
          <div class="renewal-booking-inner"><div><p class="renewal-kicker">Your next journey</p>
          <h2>Start with the ride.</h2><p>Enter your itinerary for a quote. For vans, Sprinters and buses, request a tailored quote and confirm availability.</p>
          <a href="{escape(quote_url, quote=True)}">Open the booking page</a></div>{parts.html(booking)}</div>
          </details></div></section>'''
    return source[:header["start"]] + hero + source[header["end"]:]


def renew_reference_page(source, context, variant, quote_url, email):
    """Compose one complete approved design, retaining SEO and detailed planning."""
    nodes = _Elements(source)
    header = nodes.first(tag='header')
    sections = sorted((n for n in nodes.elements if n['tag']=='section'),key=lambda n:n['start'])
    faq = next((n for n in sections if _Elements(nodes.html(n)).first(cls='faq')),None)
    if not header or not faq:
        return source
    extras = source[header['end']:faq['start']]
    # The reference discovery owns this anchor; preserve old details separately.
    extras = extras.replace('id="plan-your-tastings"','id="detailed-tastings"',1)
    extras = extras.replace('id="choose-your-route"','id="detailed-routes"',1)
    hero_parts = _Elements(nodes.html(header))
    booking = hero_parts.first(cls='book-card')
    if booking:
        extras += '<section id="reserve-ride"><div class="reference-wrap">' + hero_parts.html(booking) + '</div></section>'
    route_link = '<a href="#plan-your-tastings">Plan your winery stops</a>'
    route_link += f' · <a href="{quote_url}">Get a transportation quote</a>'
    if context['slug'] == 'healdsburg':
        route_link += ' · <a href="#choose-your-route">Compare winery routes</a>'
    supplement = '<div class="reference-wrap reference-planning-link">'+route_link+'</div><details class="reference-more" id="winery-details"><summary>Detailed winery, pickup and return planning</summary><div>'+extras+'</div></details>'
    top = render_reference_top(context,variant,quote_url,email)
    if context['slug'] == 'healdsburg':
        top = top.replace('<h2>Discover your next stop.</h2>','<span id="choose-your-route"></span><h2>Discover your next stop.</h2>',1)
    source = source[:header['start']] + top + supplement + source[faq['start']:]
    # Replace inherited repeated conversion bands, keeping the complete design's band.
    nodes = _Elements(source)
    for section in sorted((n for n in nodes.elements if n['tag']=='section'),key=lambda n:n['start'],reverse=True):
        if _Elements(nodes.html(section)).first(cls='cta'):
            source = source[:section['start']] + source[section['end']:]
    nodes = _Elements(source)
    nav = nodes.first(tag='nav',cls='site-nav')
    if nav:
        source = source[:nav['start']] + reference_nav(variant,quote_url) + source[nav['end']:]
    source = source.replace('<body>',f'<body class="renewal-site renewal-wine wine-reference reference-{variant}">',1)
    source = source.replace('</head>','<link rel="stylesheet" href="/css/marketing-design.css?v=2">\n<link rel="stylesheet" href="/css/wine-reference.css?v=1">\n</head>',1)
    return source.replace('</body>','<script src="/marketing-design.js?v=2" defer></script>\n</body>',1)


def renew_page(source, path, image, image_alt, quote_url, group_quote_url=None, wine_context=None):
    """Apply shared visual language to an existing generated public page."""
    if (path.startswith("preview/") or 'name="robots" content="noindex' in source
            or re.search(r'<body\b[^>]*\bclass="[^"]*\brenewal-site\b', source)):
        return source
    if wine_context:
        variant = wine_context.get('design_variant') or {'healdsburg':'journal','napa-valley':'gallery'}.get(wine_context['slug'],'cinema')
        email = (group_quote_url or 'mailto:reserve@koastride.com').removeprefix('mailto:')
        return renew_reference_page(source,wine_context,variant,quote_url,email)
    folder = path.split('/')[0]
    family = {"wine-tours":"wine", "wineries":"winery", "cities":"city",
              "airports":"airport", "routes":"route", "services":"service"}.get(folder, "general")
    if path == "index.html":
        family, image, image_alt = "home", "img/hero-desktop.webp", "Koast chauffeur travel scene"
    if path == "services/wine-tours.html":
        family, image, image_alt = "wine", "img/renewal-vineyard-hero.jpg", "Illustrative California vineyard landscape"
    if path == "wineries/index.html":
        image, image_alt = "img/renewal-vineyard-hero.jpg", "Illustrative California vineyard landscape"
    if image.endswith('og-image-v2.jpg'):
        image, image_alt = "img/fleet-first-class-suv-coast-scene.webp", "Illustrative SUV on a coastal road"
    if family == "service":
        scenes = {"corporate-travel.html":"fleet-sedan-hotel-scene.webp",
                  "airport-transfers.html":"fleet-business-suv-airport-scene.webp",
                  "party-bus.html":"fleet-large-party-bus-events-scene.webp",
                  "weddings.html":"svc-weddings.jpg"}
        name = path.split('/')[-1]
        if name in scenes:
            image, image_alt = "img/" + scenes[name], "Illustrative chauffeur travel scene"
        if name == "party-bus.html":
            family = "event"
            quote_url = group_quote_url or quote_url
    source = source.replace('<body>', f'<body class="renewal-site renewal-{family}">', 1)
    source = source.replace('</head>', '<link rel="stylesheet" href="/css/marketing-design.css?v=2">\n</head>', 1)
    if family != "general":
        source = _hero(source, image, image_alt, family, quote_url)
    return source
