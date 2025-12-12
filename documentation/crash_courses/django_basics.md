# Crash Course: Django Basics

This document provides a crash course on the basic concepts of the Django framework, using examples from the TasteLocal project.

## What is Django?

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It follows the Model-View-Template (MVT) architectural pattern.

*   **Model:** The data you want to present, usually data from a database.
*   **View:** The logic that processes a user's request and prepares the data.
*   **Template:** The file that formats the data and presents it to the user (usually an HTML file).

Let's look at how these concepts are applied in the TasteLocal project.

---

## The Request-Response Cycle

1.  A user's browser sends a **request** to a specific URL.
2.  Django's URL dispatcher (`urls.py`) matches the URL to a specific **view** function.
3.  The **view** function processes the request. This might involve reading from or writing to the database (via the **models**).
4.  The view then loads a **template**, fills it with the data it prepared, and renders it.
5.  This rendered content is sent back as a **response** to the user's browser.

---

## `settings.py`: The Project's Configuration

The `TasteLocal/settings.py` file is the control panel for the entire project.

*   **`INSTALLED_APPS`**: This list tells Django which applications are active in the project. You'll see our `core` app listed here.
    ```python
    # TasteLocal/settings.py

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        # ... other apps
        'core', # Our main application
    ]
    ```

*   **`DATABASES`**: This dictionary configures the connection to our MySQL database.

---

## `urls.py`: The URL Dispatcher

When a request comes in for a URL, Django needs to know which view function should handle it. This is the job of the `urls.py` files.

*   **Project `urls.py` (`TasteLocal/urls.py`):** This is the main URL file. It mostly just includes the URL configuration from our `core` app.
    ```python
    # TasteLocal/urls.py

    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('core.urls')), # Includes all URLs from the core app
    ]
    ```

*   **App `urls.py` (`core/urls.py`):** This file contains the specific URL patterns for the `core` app.
    ```python
    # core/urls.py

    from django.urls import path
    from . import views

    urlpatterns = [
        # When a user visits the root URL (''), call the 'home' view
        path('', views.home, name='home'),
        # When a user visits '/about/', call the 'about' view
        path('about/', views.about, name='about'),
        # This pattern captures an integer from the URL and passes it to the view
        path('dishes/<int:pk>/', views.dish_detail, name='dish_detail'),
    ]
    ```
    The `name` argument is very important. It allows us to refer to this URL by a simple name in our templates and views, which is much cleaner than hardcoding the URL path.

---

## `views.py`: The Business Logic

Views are the heart of a Django application. They contain the Python code that runs when a URL is requested.

Here is a simplified version of the `home` view from `core/views.py`:

```python
# core/views.py

from django.shortcuts import render
from .models import Experience, Shop, Dish

def home(request):
    # 1. Get some data from the database
    featured_experiences = Experience.objects.all().order_by('-created_at')[:3]
    all_shops = Shop.objects.all()
    featured_dishes = Dish.objects.order_by('?')[:4]

    # 2. Prepare the context dictionary to pass data to the template
    context = {
        'featured_experiences': featured_experiences,
        'all_shops': all_shops,
        'featured_dishes': featured_dishes
    }

    # 3. Render the template with the context and return it as a response
    return render(request, 'home.html', context)
```

This view does three things:
1.  It fetches some objects from the database using the models.
2.  It puts these objects into a dictionary called `context`.
3.  It calls the `render` function, which combines the `home.html` template with the `context` dictionary to generate the final HTML.

This crash course has covered the fundamental components of a Django project. To learn more, proceed to the crash courses on Models & Databases and Views & Templates.
