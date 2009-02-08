import datetime
from django.conf import settings
from django import template
from django.core.urlresolvers import reverse
from wall.models import Wall

register = template.Library()

@register.inclusion_tag("wall/_recent_wall.html")
def recent_wall( wall, amount=5, days=7 ):
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

