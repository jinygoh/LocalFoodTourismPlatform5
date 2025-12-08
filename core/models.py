from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class User(AbstractUser):
    is_tourist = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='user_avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Dish(models.Model):
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, related_name='dishes', null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name} at {self.shop.business_name}"

class Shop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop_profile')
    business_name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    opening_hours = models.CharField(max_length=255, blank=True, null=True, help_text="e.g. Mon-Sun: 10am - 10pm")
    opening_hours_structured = models.JSONField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    image = models.ImageField(upload_to='shops/', blank=True, null=True)
    dining_establishment_type = models.CharField(max_length=50, choices=[
        ('fine_dining', 'Fine-dining restaurant'),
        ('popular_themed_cafe', 'Popular themed café'),
        ('high_demand_eatery', 'High-demand eatery (Michelin-starred or celebrity-chef)'),
        ('hawker_centre', 'Hawker centre'),
        ('food_court', 'Food court'),
        ('casual_cafe', 'Casual café'),
        ('fast_food_outlet', 'Fast-food outlet'),
    ], default='casual_cafe')

    def __str__(self):
        return self.business_name

class Experience(models.Model):
    vendor = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='experiences/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    dishes = models.ManyToManyField(Dish, related_name='experiences', blank=True)
    shops = models.ManyToManyField(Shop, related_name='participating_in', blank=True)

    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    time = models.TimeField(null=True)
    guests = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    # Generic relationship for booking different types of items
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    @property
    def content_object_name(self):
        if isinstance(self.content_object, Experience):
            return self.content_object.title
        if isinstance(self.content_object, Dish):
            return self.content_object.name
        if isinstance(self.content_object, Shop):
            return self.content_object.business_name
        return "Unknown"

    def __str__(self):
        return f"{self.user.username} - {self.content_object_name}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Generic relationship for reviewing different types of items
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    @property
    def content_object_name(self):
        if isinstance(self.content_object, Experience):
            return self.content_object.title
        if isinstance(self.content_object, Dish):
            return self.content_object.name
        if isinstance(self.content_object, Shop):
            return self.content_object.business_name
        return "Unknown"

    def __str__(self):
        return f"{self.user.username} - {self.content_object_name}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # Generic relationship for favoriting different types of items
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    @property
    def content_object_name(self):
        if isinstance(self.content_object, Experience):
            return self.content_object.title
        if isinstance(self.content_object, Dish):
            return self.content_object.name
        if isinstance(self.content_object, Shop):
            return self.content_object.business_name
        return "Unknown"

    def __str__(self):
        return f"{self.user.username} likes {self.content_object_name}"
