"""Short, visible visit facts and three-step transport planning, without legacy essays."""
from html import escape
import re
from src.wine_designs import icon


def render_wine_planning(context, previous_body, quote_url):
    detail = context.get('destination')
    facts = ''
    if detail:
        items = [('map-pin','Where to meet',detail['address']),
                 ('glass','Known for',detail['known']),
                 ('calendar','Before your visit',detail['res']+'. Confirm your experience and party size.')]
        tiles = ''.join(f'<article>{icon(symbol)}<h3>{title}</h3><p>{escape(text)}</p></article>' for symbol,title,text in items)
        facts = f'<section class="reference-visit" id="winery-details"><div class="reference-wrap"><p class="reference-eyebrow">Visit at a glance</p><h2>{escape(detail["name"])}</h2><div class="reference-plan-grid">{tiles}</div></div></section>'
        if context['slug'] == 'stags-leap-wine-cellars':
            facts += '<p class="reference-wrap reference-estate-note">Two different estates: Stag’s Leap Wine Cellars is at 5766 Silverado Trail. Stags’ Leap Winery is at 6150 Silverado Trail. Use the address on your tasting confirmation.</p>'
    steps = [
        ('glass','Choose your stops','Book tastings separately. Bring the address in each tasting confirmation.'),
        ('map-pin','Connect the day','Share your pickup, appointments and return time.'),
        ('car','Confirm your ride','We confirm the vehicle, route, service window and price.')]
    tiles = ''.join(f'<article><span class="reference-plan-number">0{i+1}</span>{icon(symbol)}<h3>{title}</h3><p>{text}</p></article>' for i,(symbol,title,text) in enumerate(steps))
    links = []
    # Keep useful authored internal guide/city links, rather than their long blocks.
    for href,label in re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>',previous_body,re.S):
        if href.startswith(('/blog/','/cities/')) and href not in [item[0] for item in links]:
            text = re.sub('<[^>]+>','',label).strip()
            if text:
                links.append((href,text))
    guides = ''.join(f'<a href="{escape(href,quote=True)}">{label}</a>' for href,label in links[:6])
    native_label = 'Get a Livermore quote' if context['slug']=='livermore' else 'Get a transportation quote'
    route_link = '<a href="#choose-your-route">Compare winery routes</a>' if context['slug']=='healdsburg' else '<a href="#plan-your-tastings">Plan your winery stops</a>'
    return facts + f'''<section class="reference-planning" id="quote-details"><div class="reference-wrap"><p class="reference-eyebrow">Driver for the day or a transfer</p><h2>A little planning. A better day.</h2><div class="reference-plan-grid">{tiles}</div><div class="reference-group-note"><strong>Bringing everyone?</strong><span>Vans, Sprinters and buses require a quote. Confirm seating, luggage and winery access.</span><a data-start-quote href="#quote-request">Plan a group ride</a></div><div class="reference-planning-links">{route_link}<a href="{escape(quote_url,quote=True)}">{native_label}</a>{guides}</div></div></section>'''
