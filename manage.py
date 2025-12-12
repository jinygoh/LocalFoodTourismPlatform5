#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This script is the primary way to interact with a Django project from the command line.
It allows you to perform tasks such as running the development server (`runserver`),
creating database migrations (`makemigrations`), applying migrations (`migrate`),
running tests (`test`), and more.

It works by setting the `DJANGO_SETTINGS_MODULE` environment variable so that Django
knows which project's settings to use.
"""
import os
import sys


def main():
    """Run administrative tasks."""
    # Set the 'DJANGO_SETTINGS_MODULE' environment variable. This points Django to the
    # project's settings file, which is essential for all management commands.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
    try:
        # Attempt to import Django's main management utility.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django can't be imported, it's likely not installed or the
        # virtual environment is not activated. This error message provides
        # helpful guidance to the user.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Pass the command-line arguments (e.g., 'runserver', 'migrate') to Django's
    # command-line executor.
    execute_from_command_line(sys.argv)


# This standard Python construct ensures that the `main()` function is called
# only when this script is executed directly from the command line.
if __name__ == '__main__':
    main()
