from django.contrib import admin
from .models import Auction

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','image',   'registration_fee', 'current_bid', 'end_time')  # Display the image field in admin
admin.site.register(Auction)
 