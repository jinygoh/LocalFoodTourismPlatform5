"""
This file (`core/admin.py`) is used to configure the Django admin interface
for the `core` application.

By registering models with the Django admin, we can easily create, read,
update, and delete (CRUD) records for those models through a web-based
interface provided by Django. This is incredibly useful for site administrators
to manage the application's data without needing direct database access.
"""
from django.contrib import admin
from .models import User, UserProfile, Dish, Shop, Experience, Booking, Review, Favorite

# --- Model Registrations ---
# Each `admin.site.register()` call makes the corresponding model available
# in the Django admin panel.

# Register the custom User model.
admin.site.register(User)

# Register the UserProfile model to manage user-specific data.
admin.site.register(UserProfile)

# Register the Dish model.
admin.site.register(Dish)

# Register the Shop model for vendors.
admin.site.register(Shop)

# Register the Experience model for bookable events.
admin.site.register(Experience)

# Register the Booking model to view and manage bookings.
admin.site.register(Booking)

# Register the Review model to manage user reviews.
admin.site.register(Review)

# Register the Favorite model.
admin.site.register(Favorite)
