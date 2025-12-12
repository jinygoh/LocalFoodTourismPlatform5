"""
Main URL configuration for the TasteLocal project.

This file is the primary URL router for the entire application. It defines the top-level
URL patterns and includes the URL configurations from other applications.

The `urlpatterns` list routes URLs to their corresponding views.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# The main list of URL patterns for the project.
urlpatterns = [
    # The URL for the Django admin site.
    path('admin/', admin.site.urls),

    # Includes all URL patterns defined in the `core` application's `urls.py` file.
    # This keeps the project's URL structure modular and organized.
    path('', include('core.urls')),
]

# This block is executed only when the project is in DEBUG mode.
# It's a common pattern for adding development-specific URLs.
if settings.DEBUG:
    import debug_toolbar

    # Add the URLs for the Django Debug Toolbar.
    # The toolbar provides detailed debugging information in the browser.
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    # Add a URL pattern for serving user-uploaded media files during development.
    # In a production environment, these files should be served by a dedicated web server.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
