import datetime
from django.conf import settings
from django.shortcuts import get_object_or_404
from django import template
from django.core.urlresolvers import reverse
from wall.models import Wall

register = template.Library()

@register.inclusion_tag("wall/_recent_wall.html")
def recent_wall( wall, amount=5, days=7 ):
    """ Inclusion tag that displays a wall object (or a wall that
        is procured via the supplied slug.) Only recent items are
        displayed according to the addtional parameters:
            -- amount - maximum number of items to display
            -- days - items must be no more than this number of days old.
    """
    if not hasattr( wall, "get_recent_items" ):
        wall = get_object_or_404( Wall, slug=wall )
    items = wall.get_recent_items( amount, days )
    number = len(items)
    if number == 0:
        items = ["No items have been posted recently."]
    context = {
        'wall': wall,
        'items': items,
        'days': days,
        'number': number
    }
    return context

