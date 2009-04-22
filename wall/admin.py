from django.contrib import admin
from wall.models import WallItem, Wall

class WallItemAdmin(admin.ModelAdmin):
    list_display = ('wall', 'author', 'created_at', 'body')


admin.site.register(WallItem, WallItemAdmin)


admin.site.register(Wall)

