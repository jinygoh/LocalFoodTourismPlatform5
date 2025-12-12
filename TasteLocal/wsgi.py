"""
WSGI config for the TasteLocal project.

This file provides the entry-point for WSGI-compatible web servers to serve the
Django application. WSGI (Web Server Gateway Interface) is a standard interface
between web servers and Python web applications.

When deploying the project to a production environment using a server like Gunicorn or uWSGI,
the server is configured to use the `application` callable defined in this file.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the 'DJANGO_SETTINGS_MODULE' environment variable to point to the project's settings file.
# This is crucial for the application to load its configuration correctly.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')

# The `get_wsgi_application()` function returns the WSGI callable.
# This callable is what the web server interacts with to handle requests.
application = get_wsgi_application()
