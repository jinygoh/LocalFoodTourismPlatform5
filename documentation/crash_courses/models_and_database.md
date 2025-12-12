# Crash Course: Models and Databases

This document explains how Django models work and how they interact with the database, using examples from the TasteLocal project.

## What is a Model?

A Django model is a Python class that represents a table in your database. Each attribute of the class represents a column in that table. Django uses this model to perform database queries without you needing to write any SQL. This is called an Object-Relational Mapper (ORM).

All models for our application are defined in `core/models.py`.

---

## Example: The `Shop` Model

Let's break down the `Shop` model from our project.

```python
# core/models.py

from django.db import models
from django.contrib.auth.models import User

class Shop(models.Model):
    # This creates a one-to-one link to Django's built-in User model.
    # Each shop is owned by one specific user.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop_profile')

    # A simple text field with a maximum length.
    business_name = models.CharField(max_length=255)

    # A larger text field for longer descriptions.
    description = models.TextField()

    # A field for storing location as text.
    location = models.CharField(max_length=255)

    # A field for storing decimal numbers, essential for latitude/longitude.
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    # A field for uploading images. Django handles the file upload process.
    image = models.ImageField(upload_to='shops/', blank=True, null=True)

    # This method defines how the object will be displayed, for example in the admin panel.
    def __str__(self):
        return self.business_name
```

### Field Types

Django has many different field types to represent different kinds of data:
*   `CharField`: For small- to large-sized strings.
*   `TextField`: For large amounts of text.
*   `DecimalField`: For fixed-precision decimal numbers.
*   `BooleanField`: For true/false values.
*   `DateField`, `TimeField`, `DateTimeField`: For dates and times.
*   `ImageField`, `FileField`: For uploading files.
*   `JSONField`: For storing structured JSON data.

### Relationships

Models can also define their relationships to other models.
*   **`OneToOneField`**: As seen in the `Shop` model, this creates a one-to-one relationship. A `User` can only have one `Shop`, and a `Shop` can only belong to one `User`.
*   **`ForeignKey`**: This creates a many-to-one relationship. For example, the `Dish` model has a `ForeignKey` to the `Shop` model, because one `Shop` can have many `Dishes`.
    ```python
    # core/models.py
    class Dish(models.Model):
        shop = models.ForeignKey('Shop', on_delete=models.CASCADE, related_name='dishes', null=True)
        # ... other fields
    ```
*   **`ManyToManyField`**: This creates a many-to-many relationship. For example, an `Experience` can involve many `Dishes`.

---

## Migrations: Syncing Models with the Database

After you define or change a model, you need to tell the database about it. Django handles this with a two-step migration system.

1.  **`python manage.py makemigrations`**
    This command looks at your models and compares them to the current state of the database schema recorded in the migration files. It then generates new migration files (e.g., `core/migrations/0001_initial.py`) which contain the Python code to apply the changes.

2.  **`python manage.py migrate`**
    This command takes any unapplied migration files and runs them, executing the necessary SQL commands to update the database schema.

---

## Querying the Database

The real power of Django's ORM is in how it lets you retrieve data. You don't write SQL; you write Python. This is usually done inside your `views.py` files.

Here are some common query examples:

*   **Get all shops:**
    ```python
    all_shops = Shop.objects.all()
    ```

*   **Get a single shop by its primary key (ID):**
    ```python
    my_shop = Shop.objects.get(pk=1)
    ```

*   **Filter shops by location:**
    ```python
    singapore_shops = Shop.objects.filter(location='Singapore')
    ```

*   **Filter shops with "Chicken" in their name (case-insensitive):**
    ```python
    chicken_shops = Shop.objects.filter(business_name__icontains='Chicken')
    ```

*   **Order shops by business name:**
    ```python
    alphabetical_shops = Shop.objects.order_by('business_name')
    ```

*   **Get the first 5 shops:**
    ```python
    first_five_shops = Shop.objects.all()[:5]
    ```

*   **Get dishes related to a shop:**
    Once you have a shop object, you can easily access its related dishes.
    ```python
    shop = Shop.objects.get(pk=1)
    dishes_at_this_shop = shop.dishes.all() # 'dishes' comes from the 'related_name'
    ```

This ORM makes database operations intuitive and Pythonic, forming the backbone of the application's data handling.
