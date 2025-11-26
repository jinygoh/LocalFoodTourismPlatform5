from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('experiences/', views.listing_list, name='listing_list'),
    path('experiences/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('experiences/<int:pk>/payment/', views.payment_page, name='payment_page'),
    path('experiences/<int:pk>/process_payment/', views.process_payment, name='process_payment'),
    path('booking/confirmation/<int:pk>/', views.booking_confirmation, name='booking_confirmation'),
    path('booking/cancel/<int:pk>/', views.cancel_booking, name='cancel_booking'),
    path('profile/', views.profile, name='profile'),
    path('vendor/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/profile/edit/', views.edit_vendor_profile, name='edit_vendor_profile'),
    path('vendor/add/', views.add_listing, name='add_listing'),
    path('vendor/edit/<int:pk>/', views.edit_listing, name='edit_listing'),
    path('vendor/delete/<int:pk>/', views.delete_listing, name='delete_listing'),
    path('experiences/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
]
