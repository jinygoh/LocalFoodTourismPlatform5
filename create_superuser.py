"""
This is a standalone script to create a superuser for the Django application.

It is designed to be run from the command line, and it will create a user with
administrative privileges. This is useful for initial setup and for accessing
the Django admin interface.

The script is idempotent, meaning it can be run multiple times without
creating duplicate superusers.
"""
import os
import django
from django.contrib.auth import get_user_model

# Set the DJANGO_SETTINGS_MODULE environment variable to point to the project's settings.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
# Initialize the Django application. This must be done before importing any models.
django.setup()

# Get the custom User model defined in the project.
User = get_user_model()

# Define the superuser's credentials.
SUPERUSER_USERNAME = 'admin'
SUPERUSER_EMAIL = 'admin@example.com'
SUPERUSER_PASSWORD = 'admin123'

# Check if a user with the specified username already exists.
if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
    # If the user does not exist, create a new superuser.
    User.objects.create_superuser(SUPERUSER_USERNAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD)
    print(f'Superuser "{SUPERUSER_USERNAME}" created with password "{SUPERUSER_PASSWORD}"')
else:
    # If the user already exists, do nothing and print a message.
    print(f'Superuser "{SUPERUSER_USERNAME}" already exists')
