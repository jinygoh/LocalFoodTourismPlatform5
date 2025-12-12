"""
This file (`core/apps.py`) is used to configure the `core` application itself.

The `AppConfig` class allows Django to discover the application and its
configuration. While often minimal, it can be used for more advanced
application setup, such as defining application-ready hooks, signals,
or custom administrative settings.
"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Configuration class for the 'core' application.
    """
    # `default_auto_field` specifies the type of primary key to use for models
    # in this application that do not explicitly define a primary key.
    # 'BigAutoField' is a 64-bit integer, which is a safe default for most applications.
    default_auto_field = 'django.db.models.BigAutoField'

    # `name` is the full Python path to the application.
    name = 'core'
