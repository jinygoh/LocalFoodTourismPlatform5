"""
ASGI config for the TasteLocal project.

This file provides the entry-point for ASGI-compatible web servers to serve the
Django application. ASGI (Asynchronous Server Gateway Interface) is the successor
to WSGI and is designed to handle asynchronous Python web applications.

While this project does not currently use asynchronous features extensively,
this file is included by default for future compatibility and can be used by
servers like Daphne or Uvicorn.
"""

import os
from django.core.asgi import get_asgi_application

# Set the 'DJANGO_SETTINGS_MODULE' environment variable to point to the project's settings file.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')

# The `get_asgi_application()` function returns the ASGI callable.
# This callable is what the web server interacts with to handle requests asynchronously.
application = get_asgi_application()
