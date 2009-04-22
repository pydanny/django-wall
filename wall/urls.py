from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$', 'wall.views.home', name="wall_home"),
    url(r'^recent/(?P<slug>[-\w]+)/$', 'wall.views.home', { 'template_name':'wall/recent.html' }, name="wall_recent"),
    url(r'^add/(?P<slug>[-\w]+)/$', 'wall.views.add', name="add_wall_item"),
    url(r'^edit/(?P<id>\d+)/$', 'wall.views.edit', name="edit_wall_item"),
)
