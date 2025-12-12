# Project Structure and Reading Guide

This document provides a comprehensive overview of the TasteLocal project's structure. It is designed to help you understand the purpose of each folder and file, and how they interact with each other.

## High-Level Overview

The project is a standard Django web application. Django follows the Model-View-Template (MVT) architectural pattern:

*   **Model:** Defines the data structure. These are essentially the tables in the database.
*   **View:** Contains the business logic. It handles user requests, interacts with the models, and renders the templates.
*   **Template:** The presentation layer. These are the HTML files that the user sees in their browser.

## Folder and File Structure

Here is a breakdown of the key folders and files in the project:

```
TasteLocal/
├── core/                   # Main Django app with core functionality
│   ├── migrations/         # Database migration files
│   ├── templates/          # HTML templates specific to the core app
│   ├── __init__.py         # Initializes the core app as a Python package
│   ├── admin.py            # Registers models with the Django admin site
│   ├── apps.py             # Configuration for the core app
│   ├── forms.py            # Contains the forms used in the application
│   ├── models.py           # Defines the database models (data structure)
│   ├── tests.py            # Contains tests for the application
│   ├── urls.py             # URL routing for the core app
│   └── views.py            # Contains the application's business logic
├── documentation/          # Project documentation
├── media/                  # User-uploaded files (e.g., images)
├── static/                 # Static assets (CSS, JavaScript, images)
├── templates/              # Global HTML templates
├── tests/                  # End-to-end tests
├── TasteLocal/             # Main Django project configuration
│   ├── __init__.py         # Initializes the project as a Python package
│   ├── asgi.py             # ASGI configuration for deployment
│   ├── settings.py         # Django project settings
│   ├── urls.py             # Main URL routing for the project
│   └── wsgi.py             # WSGI configuration for deployment
├── .gitignore              # Files and folders to be ignored by Git
├── manage.py               # Django's command-line utility
├── populate_data.py        # Scripts to populate the database
├── README.md               # Project overview and setup instructions
└── requirements.txt        # Python package dependencies
```

### Key Files and Their Roles

*   **`manage.py`**: This is a command-line utility that lets you interact with your Django project. You use it to run the development server, apply database migrations, and more.

*   **`TasteLocal/settings.py`**: This file contains all the configuration for the Django project, such as database settings, installed apps, and template directories.

*   **`TasteLocal/urls.py`**: This is the main URL router for the project. It includes the URLs from the `core` app.

*   **`core/models.py`**: This is one of the most important files. It defines the structure of the application's data. Each class in this file represents a table in the database.

*   **`core/views.py`**: This file contains the core logic of the application. Each function or class-based view handles a specific user request, such as rendering a page, processing a form, or performing an action.

*   **`core/urls.py`**: This file maps URLs to views. When a user navigates to a specific URL, this file tells Django which view function to execute.

*   **`templates/` and `core/templates/`**: These folders contain the HTML templates that are rendered by the views. The main `templates` folder contains base templates that are shared across the application, while the `core/templates` folder contains templates specific to the `core` app.

*   **`static/`**: This folder contains static files like CSS, JavaScript, and images that are used in the templates.

*   **`populate_..._data.py` scripts**: These are standalone scripts used to populate the database with initial data for testing and development.

## How to Read the Code to Understand the Project

To understand the project from scratch, we recommend reading the files in the following order. This will take you through the entire request-response cycle, from the data models to the final rendered HTML.

**1. Understand the Data Structure (`core/models.py`)**

Start by reading `core/models.py`. This file defines the database schema and is the foundation of the entire application. Understanding the models will help you understand the data that the application works with.

**2. Follow the URL Routing (`TasteLocal/urls.py` -> `core/urls.py`)**

Next, look at how URLs are routed. Start with `TasteLocal/urls.py`, which is the entry point for all URLs. This file will then direct you to `core/urls.py`, which contains the app-specific URL patterns. This will show you which views are triggered by which URLs.

**3. Analyze the Business Logic (`core/views.py`)**

Once you understand the URL routing, you can dive into `core/views.py`. This is where the magic happens. Pick a view function and trace its logic. You will see how it interacts with the models to fetch data and how it uses the templates to render the final output.

**4. Examine the Forms (`core/forms.py`)**

Many of the views will use forms to handle user input. The forms are defined in `core/forms.py`. Looking at this file will help you understand how user data is collected and validated.

**5. Review the Templates (`templates/` and `core/templates/`)**

Finally, look at the HTML templates. These files determine what the user sees in their browser. Start with the base templates in the main `templates` folder, and then look at the specific templates in `core/templates/`. You will see how the data from the views is displayed to the user.

By following this order, you will gain a comprehensive understanding of how the TasteLocal application is structured and how it works.
