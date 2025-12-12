#
# This file (`core/models.py`) defines the database structure for the TasteLocal application.
# It uses Django's Object-Relational Mapper (ORM) to create Python classes that map directly
# to database tables. Each class represents a table, and each attribute of a class
# represents a column in that table.
#
# These models are the single, definitive source of truth for the application's data.
# They are used by the views (`core/views.py`) to query and manipulate data, and they
# are referenced by forms (`core/forms.py`) to create and validate user input.
#
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

#
# Represents a user in the system.
# Extends Django's built-in AbstractUser to add custom fields.
#
class User(AbstractUser):
    # Boolean flag to identify if the user is a tourist.
    is_tourist = models.BooleanField(default=False)
    # Boolean flag to identify if the user is a vendor.
    is_vendor = models.BooleanField(default=False)

#
# Stores additional, non-authentication-related information for a User.
# This creates a separate profile linked to each user.
#
class UserProfile(models.Model):
    # A one-to-one link to the main User model. If a User is deleted, their profile is also deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # The user's contact phone number. Optional.
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    # The user's profile picture. Uploaded to the 'user_avatars/' directory. Optional.
    image = models.ImageField(upload_to='user_avatars/', blank=True, null=True)

    # Defines the string representation of the UserProfile object.
    def __str__(self):
        return self.user.username

#
# Represents a single food dish offered by a Shop.
#
class Dish(models.Model):
    # A many-to-one relationship to the Shop model. One shop can have multiple dishes.
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, related_name='dishes', null=True)
    # The name of the dish (e.g., "Chicken Rice").
    name = models.CharField(max_length=255)
    # A detailed description of the dish.
    description = models.TextField()
    # An image of the dish. Uploaded to the 'dishes/' directory. Optional.
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    # The price of the dish. DecimalField is used to avoid floating-point errors.
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Defines the string representation of the Dish object.
    def __str__(self):
        return f"{self.name} at {self.shop.business_name}"

#
# Represents a vendor's business, such as a restaurant or food stall.
#
class Shop(models.Model):
    # A one-to-one link to the vendor's User account.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop_profile')
    # The name of the business (e.g., "Maxwell Food Centre").
    business_name = models.CharField(max_length=255)
    # A detailed description of the shop.
    description = models.TextField()
    # The physical address or location of the shop.
    location = models.CharField(max_length=255)
    # The shop's contact phone number.
    contact_number = models.CharField(max_length=20)
    # A free-text field for opening hours.
    opening_hours = models.CharField(max_length=255, blank=True, null=True, help_text="e.g. Mon-Sun: 10am - 10pm")
    # A structured JSON field for storing opening hours, used for programmatic checks.
    opening_hours_structured = models.JSONField(blank=True, null=True)
    # The geographic latitude of the shop for map functionality.
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    # The geographic longitude of the shop for map functionality.
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    # An image of the shop. Uploaded to the 'shops/' directory. Optional.
    image = models.ImageField(upload_to='shops/', blank=True, null=True)
    # The type of dining establishment, used for filtering and booking logic.
    dining_establishment_type = models.CharField(max_length=50, choices=[
        ('fine_dining', 'Fine-dining restaurant'),
        ('popular_themed_cafe', 'Popular themed café'),
        ('high_demand_eatery', 'High-demand eatery (Michelin-starred or celebrity-chef)'),
        ('hawker_centre', 'Hawker centre'),
        ('food_court', 'Food court'),
        ('casual_cafe', 'Casual café'),
        ('fast_food_outlet', 'Fast-food outlet'),
    ], default='casual_cafe')

    # Defines the string representation of the Shop object.
    def __str__(self):
        return self.business_name

#
# Represents a bookable experience, such as a food tour or cooking class.
#
class Experience(models.Model):
    # A many-to-one relationship to the Shop model, indicating which vendor offers this experience.
    vendor = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='experiences')
    # The title of the experience.
    title = models.CharField(max_length=255)
    # A detailed description of the experience.
    description = models.TextField()
    # The price of the experience.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # An image for the experience. Uploaded to the 'experiences/' directory. Optional.
    image = models.ImageField(upload_to='experiences/', blank=True, null=True)
    # The date and time the experience was created. Automatically set on creation.
    created_at = models.DateTimeField(auto_now_add=True)
    # A many-to-many relationship to Dish, for experiences that feature specific dishes.
    dishes = models.ManyToManyField(Dish, related_name='experiences', blank=True)
    # A many-to-many relationship to Shop, for experiences that involve multiple shops.
    shops = models.ManyToManyField(Shop, related_name='participating_in', blank=True)

    # Defines the string representation of the Experience object.
    def __str__(self):
        return self.title

#
# Represents a booking made by a user for a Shop or Experience.
#
class Booking(models.Model):
    # The user who made the booking.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    # The date of the booking.
    date = models.DateField()
    # The time of the booking.
    time = models.TimeField(null=True)
    # The number of guests for the booking.
    guests = models.PositiveIntegerField()
    # The status of the booking (e.g., pending, confirmed, cancelled).
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending')
    # The date and time the booking was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # The following three fields create a "Generic Foreign Key".
    # This allows a Booking to be associated with any other model (e.g., a Shop or an Experience).
    # 1. A ForeignKey to the ContentType model, which represents the model being booked.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 2. The primary key of the object being booked.
    object_id = models.PositiveIntegerField()
    # 3. The GenericForeignKey field, which combines the two above to create a direct link.
    content_object = GenericForeignKey('content_type', 'object_id')

    # A property to get the name of the booked item, regardless of its type.
    @property
    def content_object_name(self):
        if isinstance(self.content_object, Experience):
            return self.content_object.title
        if isinstance(self.content_object, Dish):
            return self.content_object.name
        if isinstance(self.content_object, Shop):
            return self.content_object.business_name
        return "Unknown"

    # Defines the string representation of the Booking object.
    def __str__(self):
        return f"{self.user.username} - {self.content_object_name}"

#
# Represents a review left by a user for a Shop, Dish, or Experience.
#
class Review(models.Model):
    # The user who wrote the review.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # The rating given, from 1 to 5.
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    # The text content of the review.
    comment = models.TextField()
    # The date and time the review was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # Generic relationship for reviewing different types of items (Shop, Dish, Experience).
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # A property to get the name of the reviewed item.
    @property
    def content_object_name(self):
        if isinstance(self.content_object, Experience):
            return self.content_object.title
        if isinstance(self.content_object, Dish):
            return self.content_object.name
        if isinstance(self.content_object, Shop):
            return self.content_object.business_name
        return "Unknown"

    # Defines the string representation of the Review object.
    def __str__(self):
        return f"{self.user.username} - {self.content_object_name}"

#
# Represents a user's "favorite" or "saved" item.
#
class Favorite(models.Model):
    # The user who favorited the item.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # The date and time the item was favorited.
    created_at = models.DateTimeField(auto_now_add=True)

    # Generic relationship for favoriting different types of items (Shop, Dish, Experience).
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Meta options for the model.
    class Meta:
        # Ensures that a user can only favorite a specific item once.
        unique_together = ('user', 'content_type', 'object_id')

    # A property to get the name of the favorited item.
    @property
    def content_object_name(self):
        if isinstance(self.content_object, Experience):
            return self.content_object.title
        if isinstance(self.content_object, Dish):
            return self.content_object.name
        if isinstance(self.content_object, Shop):
            return self.content_object.business_name
        return "Unknown"

    # Defines the string representation of the Favorite object.
    def __str__(self):
        return f"{self.user.username} likes {self.content_object_name}"
