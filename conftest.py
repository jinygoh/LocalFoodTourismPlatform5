"""
This file (`conftest.py`) is a special file used by the pytest testing framework.

Pytest automatically discovers and uses this file to configure the test environment
and to make fixtures (reusable test setup code) available to all tests in the
directory and its subdirectories.

In this project, its primary role is to ensure that the Django application is
properly configured and initialized before any tests are run.
"""
import os
import django

def pytest_configure():
    """
    A pytest hook that is called during the test collection phase.

    This function sets up the Django environment, which is a necessary
    step for tests that need to interact with Django's settings, models,
    or other components.
    """
    # Set the 'DJANGO_SETTINGS_MODULE' environment variable to point to our
    # project's settings file. This tells Django where to find its configuration.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')

    # Initialize the Django application. This loads the settings and populates
    # Django's application registry, making the models and other components
    # available for use in the tests.
    django.setup()
