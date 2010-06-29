from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatewords

class WallItem(models.Model):
    """
    A simple note to post on a shared wall.
    """
    wall       = models.ForeignKey('Wall')
    author     = models.ForeignKey(User, related_name="wall_item_author")
    body       = models.TextField(_('item_body'))
    created_at = models.DateTimeField(_('created at'), default=datetime.now)

    class Meta:
        verbose_name        = _('wallitem')
        verbose_name_plural = _('wallitems')
        ordering            = ('-created_at',) 
        get_latest_by       = 'created_at'

    def __unicode__(self):
        return 'wall item created by %s on %s ( %s )' % ( self.author.username, self.created_at, truncatewords(self.body, 9 ))

class Wall(models.Model):
    """
    A shared place to post items.

    The management command "trimWallItems" will trim the number of saved
    wall items back down to the limit set by max_items (although this
    command also provides an optional override of that limit.)
    Other than that, this limit is not actively enforced as users are
    generally allowed to edit or delete their previously posted items.

    At the end of the editing process, the user supplied body for an
    item is silently trimmed to 'max_item_length'.

    The allow_html setting is reflected in help_text for the user and
    injects the use of 'striptags' in the wall home template as required.
    """
    name = models.CharField(_('name'), max_length=80)
    slug = models.SlugField(_("slug"), unique=True )
    max_items = models.IntegerField( default=50 )
    max_item_length = models.IntegerField( default = 250 )
    allow_html = models.BooleanField( default=False )

    class Meta:
        verbose_name = _('wall')
        verbose_name_plural = _('wall')

    def __unicode__(self):
        return self.name

    def get_recent_items( self, amount=5, days=7):
        """
        This shortcut function allows you to get recent items.
        -- amount is the max number of items to fetch.
        -- days optionally specifies how many days to go back. 
            (if days is <= 0, don't worry abot how old the items are.)
        """
        if days <= 0:
            # get most recent items regardless of how old
            return WallItem.objects.filter(wall=self)[:amount]
        td = timedelta(days=days)
        dt = datetime.now() - td
        return WallItem.objects.filter(wall=self,created_at__gt=dt)[:amount]

