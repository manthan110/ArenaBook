from django.contrib import admin
from .models import (
    Country, State, City, AppUser, UserProfile, 
    SportCategory,Venue, Turf, Booking, Payment, Review, ContactUs
)

admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)

admin.site.register(AppUser)
admin.site.register(UserProfile)

admin.site.register(SportCategory)
admin.site.register(Venue)
admin.site.register(Turf)

admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(ContactUs)
