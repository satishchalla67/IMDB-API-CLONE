from django.contrib import admin
from watchlist_app.models import WatchList, StreamingPlatform, Review


# Register your models here.
admin.site.register(WatchList)
admin.site.register(StreamingPlatform)
admin.site.register(Review)