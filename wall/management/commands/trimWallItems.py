from django.core.management.base import NoArgsCommand
from optparse import make_option
import csv
from wall.models import Wall

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
       make_option('--wall_size', dest='wall_size', default="-1",
           help='Override the wall max_items limit with this number.'),
    )
    help = "Trim excess wall items from all walls."

    requires_model_validation = False

    def handle_noargs(self, **options):
        try:
            item_limit = int(options.get('wall_size', "-1"))
        except:
            item_limit = -1
        walls = Wall.objects.all()
        for wall in walls:
            items = wall.wallitem_set.select_related()
            if item_limit < 0:
                 wall_limit = wall.max_items
            else:
                 wall_limit = item_limit
            if len(items) > wall_limit:
                for item in items[wall_limit:]:
                    # print "delete item", item
                    item.delete()
