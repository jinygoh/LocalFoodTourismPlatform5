#
# This file (`core/urls.py`) is the URL configuration for the `core` application.
# It maps URL patterns to specific view functions defined in `core/views.py`.
# When a user navigates to a URL, Django's URL dispatcher checks these patterns
# to determine which view should handle the request.
#
# The main project's URL configuration (`TasteLocal/urls.py`) includes this file,
# making these patterns accessible to the entire application.
# The `name` argument in each `path` function is crucial as it allows us to
# refer to the URL by a unique name in our templates and views, avoiding hardcoded URLs.
#
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView

# A list of URL patterns for the core application.
urlpatterns = [
    # General Site Pages
    path('', views.home, name='home'), # The home page
    path('about/', views.about, name='about'), # The about page
    path('explore/', views.explore, name='explore'), # The main exploration/search page

    # Authentication
    path('register/', views.register, name='register'), # User registration page
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'), # Custom login page
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # Logout functionality

    # Detail Pages for Core Models
    # The <int:pk> syntax captures an integer from the URL (the primary key) and passes it to the view.
    path('dishes/<int:pk>/', views.dish_detail, name='dish_detail'),
    path('shops/<int:pk>/', views.shop_detail, name='shop_detail'),
    path('experiences/<int:pk>/', views.experience_detail, name='experience_detail'),

    # Booking and Payment Flow for Experiences
    path('experiences/<int:pk>/payment/', views.payment_page, name='payment_page'),
    path('experiences/<int:pk>/process_payment/', views.process_payment, name='process_payment'),
    path('booking/confirmation/<int:pk>/', views.booking_confirmation, name='booking_confirmation'),
    path('booking/cancel/<int:pk>/', views.cancel_booking, name='cancel_booking'),

    # User Profile
    path('profile/', views.profile, name='profile'), # Main user profile page
    path('profile/edit/', views.profile_edit_view, name='profile_edit'), # Page for editing the user's profile

    # Vendor Dashboard and Management
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'), # The main dashboard for vendors
    path('shop/<int:pk>/', views.vendor_detail, name='vendor_detail'), # Public detail page for a vendor's shop
    path('shop/profile/edit/', views.edit_vendor_profile, name='edit_vendor_profile'), # Page for vendors to edit their shop profile

    # CRUD (Create, Read, Update, Delete) URLs for Experiences
    path('shop/experiences/add/', views.add_listing, name='add_experience'),
    path('shop/experiences/edit/<int:pk>/', views.edit_listing, name='edit_experience'),
    path('shop/experiences/delete/<int:pk>/', views.delete_listing, name='delete_experience'),

    # CRUD URLs for Dishes
    path('shop/dishes/add/', views.add_dish, name='add_dish'),
    path('shop/dishes/edit/<int:pk>/', views.edit_dish, name='edit_dish'),
    path('shop/dishes/delete/<int:pk>/', views.delete_dish, name='delete_dish'),

    # Favorites Functionality
    # This is a legacy URL, the API endpoint below is now used.
    path('experiences/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    # API endpoint for adding/removing favorites asynchronously with JavaScript.
    # It captures the model type (shop, dish, experience) and the object's primary key.
    path('api/toggle_favorite/<str:model_name>/<int:pk>/', views.toggle_favorite_api, name='toggle_favorite_api'),
]
