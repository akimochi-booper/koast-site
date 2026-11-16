"""Illustrative photo assignments: no repeated scene within a wine page.

These images represent regional ambience, not photographs of the named estates.
The catalogue deliberately separates the hero, discovery and transport slots.
"""
CARD_PHOTOS = (
    'wine-tasting-room-oak.jpg', 'wine-garden-courtyard.jpg',
    'reference-journal-grapes.jpg', 'reference-gallery-oak-lane.jpg',
    'reference-cinema-card-two.jpg', 'wine-fruiting-rows.jpg',
    'reference-cinema-card-three.jpg', 'renewal-wine-terrace.jpg',
)


def winery_photo(slug, winery_details):
    """Keep each winery's card scene consistent across region and estate pages.

    Existing authored insertion order is stable; additions append rather than
    reassigning existing wineries. Different regions may share an illustrative
    scene. This is not a catalogue of documentary estate photographs.
    """
    detail = winery_details.get(slug)
    if not detail:
        raise ValueError('Add verified winery context before assigning discovery art: '+slug)
    siblings = [key for key,item in winery_details.items() if item['region']==detail['region']]
    index = siblings.index(slug)
    if index >= len(CARD_PHOTOS):
        raise ValueError('Add distinct discovery photography before adding more regional stops')
    return CARD_PHOTOS[index]
