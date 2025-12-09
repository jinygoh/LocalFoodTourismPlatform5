from django.contrib import admin
from .models import User, UserProfile, Dish, Shop, Experience, Booking, Review, Favorite

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Dish)
admin.site.register(Shop)
admin.site.register(Experience)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Favorite)
