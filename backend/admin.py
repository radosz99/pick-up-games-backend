from django.contrib import admin

# Register your models here.

from .models import CourtDetails, PlayingTimeFrame, Address, Court, CourtImage, Rating

admin.site.register(Court)
admin.site.register(CourtDetails)
admin.site.register(PlayingTimeFrame)
admin.site.register(Address)
admin.site.register(CourtImage)
admin.site.register(Rating)
