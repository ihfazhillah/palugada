from django.contrib import admin

# Register your models here.
from sembada.feeds.models import FeedUrl, FeedItem, FeedTag


class FeedUrlAdmin(admin.ModelAdmin):
    pass

class FeedItemAdmin(admin.ModelAdmin):
    pass

class FeedTagAdmin(admin.ModelAdmin):
    pass


admin.site.register(FeedUrl, FeedUrlAdmin)
admin.site.register(FeedItem, FeedItemAdmin)
admin.site.register(FeedTag, FeedTagAdmin)
