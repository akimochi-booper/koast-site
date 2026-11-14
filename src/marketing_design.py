"""Public marketing presentation, composed before metadata enhancement.

No provider, booking or tracking effects. Existing authored copy, booking markup,
canonical identity and FAQ remain owned by the generator/route renderers.
"""
from html import escape
from html.parser import HTMLParser
import re


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


def _compact_wine_planning(source, quote_url):
    """Keep detailed practical content available after the visual discovery cards."""
    nodes = _Elements(source)
    sections = [n for n in sorted(nodes.elements, key=lambda n:n['start'])
                if n['tag'] == 'section' and 'renewal-section' in n['attrs'].get('class', '').split()]
    # The first winery-discovery section stays open and image-led.
    for section in reversed(sections[1:]):
        inner = nodes.html(section, inner=True)
        pieces = _Elements(inner)
        heading = pieces.first(tag='h2')
        if not heading:
            continue
        label = re.sub('<[^>]+>', '', pieces.html(heading, inner=True))
        if section['attrs'].get('id') == 'reserve-ride':
            label = 'Get a quote for your wine day'
        content = f'<details class="renewal-planning"><summary>{label}</summary>{inner}</details>'
        source = source[:section['inner_start']] + content + source[section['inner_end']:]
    # One scenic conversion band is enough; retain the same quote destination.
    updated = _Elements(source)
    for section in sorted((n for n in updated.elements if n['tag'] == 'section'), key=lambda n:n['start'], reverse=True):
        if _Elements(updated.html(section)).first(cls='cta'):
            source = source[:section['start']] + source[section['end']:]
    # Real booking handoff, not an unconnected form drawn to resemble the mockup.
    band = f'''<section class="renewal-journey-band"><div class="wrap"><div class="cta">
      <h2>Your stops.<br>One private ride.</h2><p>Hotel pickup. Your chosen tastings. A confirmed return.</p>
      <a class="btn btn-orange" href="{escape(quote_url, quote=True)}">Plan my ride</a>
      </div></div></section>'''
    nodes = _Elements(source)
    first = next((n for n in sorted(nodes.elements,key=lambda n:n['start'])
                  if n['tag']=='section' and 'renewal-section' in n['attrs'].get('class','').split()), None)
    if first:
        source = source[:first['end']] + band + source[first['end']:]
    return source.replace('</body>', '<script src="/marketing-design.js?v=1" defer></script>\n</body>', 1)


def renew_page(source, path, image, image_alt, quote_url, group_quote_url=None):
    """Apply shared visual language to an existing generated public page."""
    if (path.startswith("preview/") or 'name="robots" content="noindex' in source
            or re.search(r'<body\b[^>]*\bclass="[^"]*\brenewal-site\b', source)):
        return source
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
    source = source.replace('</head>', '<link rel="stylesheet" href="/css/marketing-design.css?v=1">\n</head>', 1)
    if family != "general":
        source = _hero(source, image, image_alt, family, quote_url)
    if path in {'wine-tours/livermore.html', 'wine-tours/healdsburg.html'}:
        source = _compact_wine_planning(source, quote_url)
    return source
