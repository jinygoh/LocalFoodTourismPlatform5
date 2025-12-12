# Crash Course: Views and Templates

This document explains the role of Views and Templates in a Django project, using examples from TasteLocal to illustrate how they work together to create the pages a user sees.

## The Role of a View

A **view** is a Python function (or class) that takes a web request and returns a web response. It's the "logic" part of the Model-View-Template pattern.

A view's responsibilities include:
1.  Receiving and processing the user's request (e.g., handling form data).
2.  Interacting with the models to get data from the database.
3.  Passing that data to a template.
4.  Returning a rendered HTML response to the user.

All our application's views are in `core/views.py`.

### Example: The `shop_detail` View

Let's look at a simplified version of the `shop_detail` view.

```python
# core/views.py

from django.shortcuts import render, get_object_or_404
from .models import Shop, Review

def shop_detail(request, pk):
    # 1. Get the specific shop from the database using the 'pk' (primary key)
    #    that was captured from the URL. get_object_or_404 is a handy shortcut
    #    that will return a "404 Not Found" error if no shop with that pk exists.
    shop = get_object_or_404(Shop, pk=pk)

    # 2. Get all reviews related to this specific shop.
    reviews = Review.objects.filter(content_object=shop).order_by('-created_at')

    # 3. Prepare the context dictionary. This is how we send data to the template.
    #    The keys ('shop', 'reviews') are the variable names we will use in the HTML.
    context = {
        'shop': shop,
        'reviews': reviews,
    }

    # 4. Render the template. Django combines the 'shop_detail.html' template
    #    with our context data to generate the final HTML.
    return render(request, 'core/shop_detail.html', context)
```

## The Role of a Template

A **template** is an HTML file with some special Django-specific syntax. It's responsible for the "presentation" part of the application. It defines the structure of the page and how the data from the view should be displayed.

Our templates are located in the `templates/` and `core/templates/` folders.

### Example: The `shop_detail.html` Template

Here's a simplified version of what `core/templates/shop_detail.html` might look like.

```html
<!-- We inherit the basic structure (navbar, footer, etc.) from a base template -->
{% extends "base.html" %}

<!-- This is where the unique content for this page goes -->
{% block content %}

  <!-- Displaying a variable from the context -->
  <h1>{{ shop.business_name }}</h1>

  <!-- Accessing attributes of the 'shop' object -->
  <p>{{ shop.description }}</p>
  <p>Location: {{ shop.location }}</p>

  <hr>

  <h2>Reviews</h2>

  <!-- Looping through a list of items from the context -->
  {% for review in reviews %}
    <div class="review">
      <p><strong>Rating: {{ review.rating }}/5</strong></p>
      <p>{{ review.comment }}</p>
      <small>By: {{ review.user.username }} on {{ review.created_at|date:"F j, Y" }}</small>
    </div>
  {% empty %}
    <!-- This is shown if the 'reviews' list is empty -->
    <p>Be the first to leave a review!</p>
  {% endfor %}

{% endblock %}
```

### Key Template Syntax

*   **`{{ variable }}`**: This is a **variable tag**. It gets replaced with the value of the variable from the context. You can access attributes of objects using dot notation, like `{{ shop.business_name }}`.

*   **`{% tag %}`**: This is a **template tag**. It performs some logic.
    *   `{% extends "base.html" %}`: Tells Django that this template inherits from `base.html`.
    *   `{% block content %}...{% endblock %}`: Defines a block of content that will be inserted into the parent template.
    *   `{% for item in list %}...{% endfor %}`: A standard for-loop.
    *   `{% if condition %}...{% else %}...{% endif %}`: A standard if/else block.

*   **Filters (`|`)**: You can modify variables with filters.
    *   `{{ review.created_at|date:"F j, Y" }}`: This takes the `created_at` date object and formats it in a more readable way (e.g., "September 20, 2024").

Together, the view and the template form a powerful system. The view handles the complex logic and data preparation, while the template focuses solely on presenting that data, keeping the concerns separate and the code clean.
