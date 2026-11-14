"""The three approved wine-page compositions, kept as separate visual designs.

Pure trusted-context renderer. Images are illustrative ambience; winery facts and
destinations come from the generator's existing content owners. Quote requests
are reviewed locally before the visitor chooses the existing email/booking path.
"""
from html import escape


def wine_context(slug, region, wineries, winery_details, slug_for):
    """Use the existing content owners; no image is treated as estate evidence."""
    stops = []
    for item in wineries[:3]:
        key = slug_for(item['name'])
        detail = winery_details.get(key, {})
        stops.append(dict(name=item['name'],area=item['area'],res=item['res'],
                          description=item['known'][:1].upper()+item['known'][1:]+'.',
                          href='/wineries/'+key if detail else '/wineries/'))
    if slug == 'livermore':
        stops = [
            dict(name='Wente Vineyards',area='Arroyo Road',res='Reservations encouraged',description='Seated tastings. Confirm your experience and time.',href='https://wentevineyards.com/visit/'),
            dict(name='Concannon Vineyard',area='Tesla Road',res='Walk-ins subject to seating',description='Reservations encouraged. Check space for your party.',href='https://concannon.wine/experiences/'),
            dict(name="Murrieta’s Well",area='Mines Road',res='Seated tastings: reservations recommended',description='Patio and walk-up options vary by date.',href='https://murrietaswell.com/visit/'),
        ]
    return dict(slug=slug,region=region,wineries=stops)


def icon(name, cls=''):
    return f'<img class="reference-icon {cls}" src="/img/icons/tabler/{name}.svg" alt="" width="24" height="24" aria-hidden="true">'


def arrow():
    return icon('arrow-right')


def quote_form(region, variant):
    date = '' if variant == 'gallery' else f'''<label class="reference-field reference-date">{icon('calendar')}
      <span data-date-label>Date</span><input type="date" name="date" aria-label="Travel date" required>{icon('chevron-down','field-chevron')}</label>'''
    label = 'Where are we picking you up?' if variant == 'gallery' else 'Pickup'
    submit = 'Start my ride plan' if variant == 'gallery' else 'Get a quote'
    return f'''<form class="reference-quote-form" data-wine-quote data-region="{escape(region,quote=True)}" data-date-optional="{'true' if variant == 'gallery' else 'false'}" novalidate action="#quote-request" method="post">
      <label class="reference-field reference-pickup">{icon('map-pin')}<input name="pickup" type="text" list="wine-pickups" aria-label="Pickup" placeholder="{label}" autocomplete="street-address" maxlength="180" required>{icon('chevron-down','field-chevron')}</label>
      {date}<label class="reference-field reference-party">{icon('users')}<select name="party" aria-label="Your party" required><option value="" selected disabled>Your party</option>
      <option value="1">1 guest</option><option value="2">2 guests</option><option value="3">3 guests</option><option value="4">4 guests</option><option value="5">5 guests</option><option value="6">6 guests</option><option value="7+">7+ guests · group quote</option></select>{icon('chevron-down','field-chevron')}</label>
      <button class="reference-primary" type="submit" disabled>{submit}{arrow()}</button>
      <p class="reference-form-status" role="status" aria-live="polite"></p>
    </form>'''


def quote_dialog(region, variant, quote_url, email):
    inputs = f'<div data-quote-inputs><p>Pickup, date and your party. Let\'s put your wine day together.</p>{quote_form(region, "dialog")}</div>' if variant == 'journal' else ''
    return f'''<datalist id="wine-pickups"><option value="Livermore or Pleasanton"><option value="San Francisco"><option value="San Jose"><option value="Oakland / East Bay"><option value="Healdsburg"><option value="Napa"></datalist>
    <dialog id="quote-request" class="reference-quote-dialog" data-email="{escape(email,quote=True)}" aria-labelledby="quote-dialog-title">
      <button class="reference-dialog-close" type="button" data-close-quote aria-label="Close quote request">{icon('x')}</button>
      <p class="reference-eyebrow">Your private ride</p><h2 id="quote-dialog-title">Your wine day, connected.</h2>{inputs}
      <div data-quote-review hidden><p>Review your plans, then send them to Koast for a transportation quote.</p>
      <dl><div><dt>Pickup</dt><dd data-review-pickup></dd></div><div><dt>Date</dt><dd data-review-date></dd></div><div><dt>Your party</dt><dd data-review-party></dd></div><div><dt>Wine country</dt><dd>{escape(region)}</dd></div></dl>
      <a class="reference-primary" data-quote-email href="mailto:{escape(email,quote=True)}">Email my quote request{arrow()}</a>
      <button class="reference-edit" type="button" data-edit-quote>Edit my plans</button>
      <p class="reference-quote-note">Your email app opens a draft for you to send. The team confirms the vehicle, route, price and availability. Tasting reservations and fees are separate.</p></div>
      <a class="reference-book-online" href="{escape(quote_url,quote=True)}">Prefer to book online? Open the booking page</a>
    </dialog><noscript><p class="reference-noscript">For a quote, <a href="{escape(quote_url,quote=True)}">open our booking page</a> or email {escape(email)} with your plans.</p></noscript>'''


def reference_nav(variant, quote_url):
    if variant == 'gallery':
        labels = [('Explore wine country','#plan-your-tastings'),('How it works','#how-it-works'),('Guides','/blog/')]
    elif variant == 'journal':
        labels = [('Destinations','/cities/'),('Wine tours','/services/wine-tours'),('Guides','/blog/')]
    else:
        labels = [('Wine tours','/services/wine-tours'),('Destinations','/cities/'),('Guides','/blog/')]
    links = ''
    for i,(text,url) in enumerate(labels):
        link = f'<a href="{url}">{text}{icon("chevron-down") if i < 2 and variant == "cinema" else ""}</a>'
        if variant == 'cinema' and i < 2:
            choices = [('Livermore Valley','/wine-tours/livermore'),('Healdsburg','/wine-tours/healdsburg'),('Napa Valley','/wine-tours/napa-valley'),('All wineries','/wineries/')] if i == 0 else [('San Francisco','/cities/san-francisco'),('San Jose','/cities/san-jose'),('Sacramento','/cities/sacramento'),('All destinations','/cities/')]
            children = ''.join(f'<a href="{href}">{label}</a>' for label,href in choices)
            link = '<div class="nav-dd">'+link+'<div class="dd-menu"><div class="dd-col">'+children+'</div></div></div>'
        links += link
    login = '<a class="reference-login" href="https://customer.moovs.app/koast/new/info">Log in</a>' if variant == 'cinema' else ''
    book = f'<a class="reference-primary" href="{escape(quote_url,quote=True)}">Book a ride</a>' if variant == 'cinema' else '<a class="reference-primary" data-start-quote href="#quote-request">Plan my ride</a>'
    return f'''<nav class="site-nav reference-nav"><div class="reference-wrap reference-nav-inner">
      <a class="logo" href="/"><img class="site-wordmark" src="/img/koast-wordmark-orange-v1.svg" alt="Koast" width="1472" height="454"></a>
      <div class="reference-nav-links">{links}</div><div class="reference-nav-actions">{login}{book}<button class="nav-burger" id="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">{icon('menu-2')}</button></div>
      </div><div class="mobile-menu" id="mobile-menu">{links}<a href="/support">Support</a><a href="https://customer.moovs.app/koast/new/info">Log in</a></div></nav>'''


def _cards(context, variant):
    pictures = {
        'cinema':['cinema-card-one','cinema-card-two','cinema-card-three'],
        'journal':['journal-grapes','cinema-card-two','journal-vineyard'],
        'gallery':['journal-grapes','cinema-card-two','gallery-oak-lane'],
    }[variant]
    result = ''
    for index, winery in enumerate(context['wineries'][:3]):
        w = {key:escape(str(value),quote=True) for key,value in winery.items()}
        result += f'''<article class="reference-winery reference-winery-{index+1}">
          <img class="reference-winery-photo" src="/img/reference-{pictures[index]}.jpg" alt="Illustrative wine-country ambience" loading="lazy">
          <div class="reference-winery-copy"><h3>{w['name']}</h3><div class="reference-winery-meta"><span class="reference-location">{icon('map-pin')}{w['area']}</span>
          <span class="reference-reservation reference-reservation-{index+1}">{icon('users' if index == 1 else 'calendar' if index == 0 else 'glass')}{w['res']}</span></div>
          <p>{w['description']}</p><a class="reference-explore" href="{w['href']}">Explore winery{arrow()}</a></div></article>'''
    return result


def _details(variant):
    items = [
        ('glass','Tastings &amp; transport','Reserve the winery experiences separately. A transportation quote does not include tasting reservations or fees; confirm each visit directly with the winery.'),
        ('car','Pickup &amp; return','Share your pickup address, confirmed tasting times and required return. Confirm the complete route, vehicle and service window before travel.'),
        ('users','Your group','Tell us your passengers, luggage and other requirements. Vans, Sprinters and buses require a quote; confirm seating, luggage space and winery access.'),
    ]
    if variant == 'gallery':
        labels = ['Do I need tasting reservations at the wineries?','How does pickup and return work?','Can you accommodate groups?']
        items = [(symbol,labels[i],text) for i,(symbol,_,text) in enumerate(items)]
    if variant == 'journal':
        body = ''.join(f'<p><strong>{title}:</strong> {text}</p>' for _,title,text in items)
        return f'<details class="reference-detail"><summary>What should I know before booking?{icon("chevron-down")}</summary><div>{body}</div></details>'
    return ''.join(f'<details class="reference-detail"><summary><span class="reference-detail-symbol">{icon(symbol)}</span>{title}{icon("chevron-down")}</summary><div><p>{text}</p></div></details>' for symbol,title,text in items)


def render_reference_top(context, variant, quote_url, email):
    """Return exact composition body; generator retains SEO and supplemental plans."""
    region = escape(context['region'])
    cards = _cards(context,variant)
    if variant == 'cinema':
        hero_image = escape(context.get('hero_image','/img/renewal-vineyard-hero.jpg'),quote=True)
        hero_alt = escape(context.get('hero_alt','Illustrative golden California vineyard landscape'),quote=True)
        regional_class = ' reference-regional-photo' if context.get('hero_image') else ''
        hero = f'''<header class="reference-hero reference-cinema-hero"><img class="reference-hero-background{regional_class}" src="{hero_image}" alt="{hero_alt}" fetchpriority="high">
          <div class="reference-wrap"><p class="reference-eyebrow">{region} · Private chauffeur</p><h1>Wine country.<br><span class="reference-gradient">Your pace.</span></h1>
          <p class="reference-lede">Your tastings, your party, your private driver.</p><a class="reference-primary reference-hero-button" data-start-quote href="#quote-request">Plan my ride{arrow()}</a>
          <div class="reference-quote-bar">{quote_form(context['region'],variant)}</div></div></header>'''
        discovery = f'''<section class="reference-discovery" id="plan-your-tastings" style="scroll-margin-top:100px"><div class="reference-wrap"><h2>Find your kind of wine day.</h2><span class="reference-orange-rule"></span><p class="reference-section-lede">Explore the stops. We'll connect the ride.</p><div class="reference-cards">{cards}</div></div></section>'''
        end = f'''<section class="reference-wrap reference-cinema-end"><div class="reference-conversion"><img src="/img/renewal-wine-ride.jpg" alt="Illustrative SUV on a vineyard lane" loading="lazy"><div><h2>Your stops. One<br>private ride.</h2><p>Tell us your pickup, party and plans for<br>a transportation quote.</p></div><a class="reference-primary" data-start-quote href="#quote-request">Plan my ride{arrow()}</a></div>{_details(variant)}<p class="reference-separate">Tastings are booked separately. Vehicle and route confirmed in your quote.</p></section>'''
    elif variant == 'journal':
        hero = f'''<header class="reference-hero reference-journal-hero"><div class="reference-wrap"><div class="reference-journal-copy"><p class="reference-eyebrow">{region} · Private wine tours</p><h1>A little<br>closer.<br>A world<br>away.</h1><p class="reference-lede">Explore the wineries. Leave the driving to us.</p><a class="reference-primary" data-start-quote href="#quote-request">Plan my ride{arrow()}</a></div>
          <figure class="reference-journal-photos"><img src="/img/reference-journal-vineyard.jpg" alt="Illustrative sunlit vineyard under oak branches" fetchpriority="high"><img class="reference-journal-inset" src="/img/reference-cinema-card-one.jpg" alt="Illustrative wine glasses on a vineyard terrace" loading="lazy"></figure></div></header>'''
        discovery = f'''<section class="reference-discovery reference-journal-discovery" id="plan-your-tastings" style="scroll-margin-top:100px"><div class="reference-wrap"><h2>Discover your next stop.</h2><p class="reference-section-lede">Compare the experiences, then connect your day.</p><div class="reference-cards">{cards}</div></div></section>'''
        end = f'''<section class="reference-journal-conversion"><img src="/img/renewal-wine-ride.jpg" alt="Illustrative SUV in wine country" loading="lazy"><div class="reference-wrap"><div><h2>Your wine day,<br>connected.</h2><p>Hotel pickup. Your chosen stops. A confirmed return.</p><a class="reference-primary" data-start-quote href="#quote-request">Request a ride quote{arrow()}</a><p class="reference-separate">Winery reservations and tasting fees are separate from transportation.</p></div></div></section><section class="reference-wrap reference-journal-end">{_details(variant)}</section>'''
    else:
        hero = f'''<header class="reference-hero reference-gallery-hero"><img class="reference-hero-background" src="/img/renewal-vineyard-hero.jpg" alt="Illustrative sunset over California vineyards" fetchpriority="high"><div class="reference-wrap"><p class="reference-eyebrow">Private {region} wine tours</p><h1>Good wine.<br>Great company.<br><span class="reference-gradient">Your driver.</span></h1><p class="reference-lede">Choose your stops. We'll plan the ride<br>around your party.</p></div></header>
          <div class="reference-wrap reference-steps" id="how-it-works"><span>{icon('plant')}Explore wineries</span><i></i><span>{icon('car')}Plan your ride</span><i></i><span>{icon('glass')}Enjoy your day</span></div>'''
        discovery = f'''<section class="reference-discovery" id="plan-your-tastings" style="scroll-margin-top:100px"><div class="reference-wrap"><h2>Where would you like to go?</h2><span class="reference-orange-rule"></span><div class="reference-cards">{cards}</div></div></section>'''
        end = f'''<section class="reference-gallery-planner"><div class="reference-wrap"><div class="reference-gallery-intro"><h2>Make a day of it.</h2><p>Tell us your date and chosen wineries. We'll confirm<br>the vehicle, route and return.</p></div>{quote_form(context['region'],variant)}{_details(variant)}<p class="reference-separate">Tasting reservations and fees are separate from transportation.</p></div></section>'''
    return hero + discovery + end + quote_dialog(context['region'],variant,quote_url,email)
