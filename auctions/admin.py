from django.contrib import admin
from auctions.models import *

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Comments)
admin.site.register(Bids)