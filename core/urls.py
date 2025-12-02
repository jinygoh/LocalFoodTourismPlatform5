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
    path('explore/', views.explore, name='explore'),
    path('dishes/<int:pk>/', views.dish_detail, name='dish_detail'),
    path('shops/<int:pk>/', views.shop_detail, name='shop_detail'),
    path('experiences/<int:pk>/', views.experience_detail, name='experience_detail'),
    path('experiences/<int:pk>/payment/', views.payment_page, name='payment_page'),
    path('experiences/<int:pk>/process_payment/', views.process_payment, name='process_payment'),
    path('booking/confirmation/<int:pk>/', views.booking_confirmation, name='booking_confirmation'),
    path('booking/cancel/<int:pk>/', views.cancel_booking, name='cancel_booking'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('favorites/', views.favorites_page, name='favorites'),
    path('shop/', views.vendor_dashboard, name='vendor_dashboard'),
    path('shop/<int:pk>/', views.vendor_detail, name='vendor_detail'),
    path('shop/profile/edit/', views.edit_vendor_profile, name='edit_vendor_profile'),
    path('shop/experiences/add/', views.add_listing, name='add_listing'),
    path('shop/experiences/edit/<int:pk>/', views.edit_listing, name='edit_listing'),
    path('shop/delete/<int:pk>/', views.delete_listing, name='delete_listing'),
    path('experiences/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('api/toggle_favorite/<str:model_name>/<int:pk>/', views.toggle_favorite_api, name='toggle_favorite_api'),
]
