"""
Django settings for the TasteLocal project.

This file contains the core configuration for the Django project, including database settings,
installed applications, middleware, template configuration, and static file handling.
It reads sensitive information, such as database credentials and the secret key, from a
`.env` file in the project's root directory for better security and portability.
"""
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from a .env file.
# This allows us to keep sensitive information out of version control.
load_dotenv()

# Define the project's base directory.
# `BASE_DIR` points to the root of the project (the directory containing `manage.py`).
BASE_DIR = Path(__file__).resolve().parent.parent


# --- Security Settings ---

# The secret key is used for cryptographic signing. It's crucial to keep this secret in production.
# It's loaded from the environment, with a default, insecure value for development.
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-for-dev')

# DEBUG mode should be False in production for security and performance reasons.
# It provides detailed error pages when enabled.
DEBUG = True

# A list of allowed hostnames for this site. In production, this should be set to the site's domain(s).
ALLOWED_HOSTS = []


# --- Application Definitions ---

# `INSTALLED_APPS` lists all Django applications that are activated for this project.
# This includes Django's built-in apps, third-party apps, and our own `core` app.
INSTALLED_APPS = [
    # Django's core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Our custom application
    'core',
    # Third-party apps
    'debug_toolbar',
]

# `MIDDLEWARE` is a list of hooks into Django's request/response processing.
# The order is important as each middleware layer depends on the previous ones.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware', # For the Django Debug Toolbar
]

# `INTERNAL_IPS` is used by the Django Debug Toolbar to determine which clients can see the toolbar.
INTERNAL_IPS = [
    "127.0.0.1",
]

# `ROOT_URLCONF` specifies the Python module where the root URL patterns for the project are defined.
ROOT_URLCONF = 'TasteLocal.urls'

# --- Template Configuration ---

# `TEMPLATES` configures how Django finds and renders HTML templates.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # `DIRS` tells Django to look for templates in a `templates` directory at the project root.
        'DIRS': [BASE_DIR / 'templates'],
        # `APP_DIRS': True` tells Django to also look for templates within each app's `templates` directory.
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# `WSGI_APPLICATION` specifies the path to the WSGI application object used by production web servers.
WSGI_APPLICATION = 'TasteLocal.wsgi.application'


# --- Database Configuration ---
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# The `DATABASES` setting configures the connection to the database.
# Credentials are read from environment variables for security.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'tastelocal'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}


# --- Password Validation ---
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

# A list of validators used to check the strength of user passwords.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# --- Internationalization & Localization ---
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- Static & Media File Handling ---
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# `STATIC_URL` is the URL prefix for static files (CSS, JS, images).
STATIC_URL = 'static/'
# `STATICFILES_DIRS` is a list of directories where Django will look for static files.
STATICFILES_DIRS = [BASE_DIR / 'static']

# `MEDIA_URL` is the URL prefix for user-uploaded media files.
MEDIA_URL = '/media/'
# `MEDIA_ROOT` is the absolute filesystem path to the directory for user-uploaded files.
MEDIA_ROOT = BASE_DIR / 'media'


# --- Model Configuration ---

# `DEFAULT_AUTO_FIELD` specifies the default primary key type for models.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# `AUTH_USER_MODEL` specifies our custom user model to be used for authentication.
AUTH_USER_MODEL = 'core.User'


# --- Authentication & Redirects ---

# The URL to redirect to after a successful logout.
LOGOUT_REDIRECT_URL = 'home'
# The URL to redirect to after a successful login (if no 'next' parameter is provided).
# This is overridden by our `CustomLoginView` for role-based redirects.
LOGIN_REDIRECT_URL = 'profile'


# --- Email Configuration ---

# These settings configure how Django sends emails.
# They are loaded from environment variables to allow for different configurations
# (e.g., console backend for development, SMTP for production) without code changes.
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() in ['true', '1', 't']
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
