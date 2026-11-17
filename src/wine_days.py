"""One exploratory wine-day catalogue, shared by homepage and region renderers.

These are merchandising ideas for manual enquiries, not priced/available products.
Passenger may consume this contract after its separate design/implementation handoff.
"""
from html import escape
import json

REQUESTED_VEHICLE_CLASSES = ('SUV','First-Class SUV','Executive Sprinter','Party bus / coach')

_REGIONS = (
    ('napa-valley','Napa Valley','A First Taste of Napa','Napa, Together','A Napa Celebration'),
    ('sonoma','Sonoma','An Unhurried Sonoma Day','Sonoma with Friends','Sonoma Celebrations'),
    ('livermore','Livermore Valley','Livermore, Your Way','Livermore, Together','A Livermore Celebration'),
)
_VEHICLES = (
    ('private-suv','SUV','Your chosen wineries. A private ride at your pace.','Plan this day'),
    ('executive-sprinter','Executive Sprinter','Bring friends and family together for a wine-country outing.','Get a group quote'),
    ('group-bus','Party bus / coach','Birthdays, reunions and team outings, planned around your party.','Get a group quote'),
)
_PHOTOS = (
    ('wine-day-napa-terrace.jpg','wine-day-napa-cellar.jpg','wine-day-napa-estate.jpg'),
    ('wine-day-sonoma-oaks.jpg','wine-day-sonoma-garden.jpg','wine-day-sonoma-veranda.jpg'),
    ('wine-day-livermore-rows.jpg','wine-day-livermore-tasting.jpg','wine-day-livermore-picnic.jpg'),
)
_PHOTO_ALTS = (
    ('Wine glasses on a terrace overlooking vineyards','Oak barrels and a tasting table in a wine cave','Stone winery courtyard beside vineyard rows'),
    ('Vineyards beneath a spreading valley oak','Empty tasting table in a flowering winery garden','Redwood winery veranda overlooking vines'),
    ('Grape rows and golden inland hills','Tasting counter beside a broad vineyard window','Picnic table shaded by a tree beside vineyards'),
)
WINE_DAY_IDEAS = tuple(
    dict(id=f'{slug}-{key}-day',region_slug=slug,region=name,title=titles[index],
         vehicle=vehicle,summary=summary,action=action,image='/img/'+_PHOTOS[row][index],
         image_alt='Illustrative wine-country scene: '+_PHOTO_ALTS[row][index],
         image_provenance='AI-generated fictional wine-country ambience; not a photograph of a named estate or offered tasting',
         state='exploratory',price_state='team_quote',duration_hours=None,stops=(),
         requestable_vehicle_classes=REQUESTED_VEHICLE_CLASSES,
         itinerary_verified=False,exclusions=('Tasting reservations and fees','Meals and purchases'))
    for row,(slug,name,*titles) in enumerate(_REGIONS)
    for index,(key,vehicle,summary,action) in enumerate(_VEHICLES)
)


def ideas_for_region(region):
    # Healdsburg discovery remains a Sonoma wine-country enquiry, not a new product.
    region = 'sonoma' if region == 'healdsburg' else region
    return [idea for idea in WINE_DAY_IDEAS if region is None or idea['region_slug']==region]


def preview_catalogue():
    """Read-only local app handoff; never an availability or booking response."""
    return dict(schemaVersion=1,state='exploratory-local-preview',
                source='src/wine_days.py WINE_DAY_IDEAS',bookerIntegration='none',
                ideas=WINE_DAY_IDEAS)


def render_wine_days(region=None):
    ideas = ideas_for_region(region)
    if not ideas:
        return ''
    # The first view deliberately gives SUV, van and bus equal prominence.
    if region is None:
        featured = ['napa-valley-private-suv-day','sonoma-executive-sprinter-day','livermore-group-bus-day']
        ideas = sorted(ideas,key=lambda idea:featured.index(idea['id']) if idea['id'] in featured else len(featured))
    tabs = ''
    if region is None:
        choices = [('all','All regions')]+[(slug,name) for slug,name,*_ in _REGIONS]
        tabs = '<div class="wine-day-regions" role="group" aria-label="Filter wine days by region">'+''.join(
            f'<button type="button" data-wine-day-region="{slug}" aria-pressed="{str(slug=="all").lower()}">{name}</button>' for slug,name in choices)+'</div>'
    cards = ''
    for idea in ideas:
        w = {key:escape(str(value),quote=True) for key,value in idea.items()}
        cards += f'''<article class="wine-day-card" data-wine-day-card data-region="{w['region_slug']}">
          <img class="wine-day-photo" src="{w['image']}" alt="{w['image_alt']}" loading="lazy">
          <div class="wine-day-copy"><p class="wine-day-kicker">{w['region']} · {w['vehicle']}</p><h3>{w['title']}</h3><p>{w['summary']}</p>
          <span class="wine-day-price">Transportation quoted for your plans</span><button class="wine-day-action" type="button" data-plan-wine-day="{w['id']}">{w['action']}<img src="/img/icons/tabler/arrow-right.svg" width="20" height="20" alt=""></button></div></article>'''
    catalogue = json.dumps(ideas,ensure_ascii=False).replace('<','\\u003c').replace('&','\\u0026')
    return f'''<section class="wine-day-collection" id="wine-day-ideas" data-wine-days><div class="wine-day-wrap">
      <p class="wine-day-eyebrow">Wine country, your way</p><h2>Find your kind of day.</h2><p class="wine-day-intro">Your own escape. Your whole group. A ride planned around you.</p>{tabs}
      <div class="wine-day-tools"><span data-wine-day-count role="status" aria-live="polite">{len(ideas)} wine-day ideas</span><div><button type="button" data-wine-day-previous aria-label="Previous wine days"><img src="/img/icons/tabler/arrow-right.svg" width="22" height="22" alt=""></button><button type="button" data-wine-day-next aria-label="Next wine days"><img src="/img/icons/tabler/arrow-right.svg" width="22" height="22" alt=""></button></div></div>
      <div class="wine-day-track" data-wine-day-track tabindex="0" role="region" aria-label="Wine-day ideas">{cards}</div>
      <p class="wine-day-note">Suggested days. Our team confirms the itinerary, vehicle and transportation price. Tastings are booked separately. Images are illustrative.</p>
      <script type="application/json" id="wine-day-catalog">{catalogue}</script></div></section>'''


if __name__ == '__main__':
    print(json.dumps(preview_catalogue(),ensure_ascii=False,indent=2))
