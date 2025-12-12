"""
This script populates the database with a smaller, more controlled set of test data
compared to `populate_singapore_data.py`.

It is designed to create a predictable environment for manual testing and demonstrations,
featuring specific users, vendors, and their interactions (reviews, bookings, favorites).
All data is hardcoded, ensuring consistency across runs.

The script is idempotent; it uses `get_or_create` and `update_or_create` to avoid
duplicating data if run multiple times.
"""
import os
import django
import random
from django.utils import timezone
from datetime import timedelta

# --- Django Setup ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
django.setup()

# --- Model Imports ---
from django.contrib.contenttypes.models import ContentType
from core.models import User, Shop, Dish, Experience, Review, Favorite, Booking, UserProfile

# A default password for all created test users.
DEFAULT_PASSWORD = 'TestPass123!'

def create_test_users():
    """Creates a set of test tourists and vendors with hardcoded data."""
    print("Creating test users...")

    # Define the data for the test tourists.
    tourist_data = [
        {'username': 'tourist_anna', 'first_name': 'Anna', 'last_name': 'Wong'},
        {'username': 'tourist_ben', 'first_name': 'Ben', 'last_name': 'Chen'},
        {'username': 'tourist_charlie', 'first_name': 'Charlie', 'last_name': 'Davis'},
    ]

    # Define the data for the test vendors.
    vendor_data = [
        {'username': 'vendor_david', 'first_name': 'David', 'last_name': 'Lim'},
        {'username': 'vendor_emily', 'first_name': 'Emily', 'last_name': 'Tan'},
    ]

    # --- Create Tourist Users ---
    for data in tourist_data:
        if not User.objects.filter(username=data['username']).exists():
            User.objects.create_user(
                username=data['username'],
                password=DEFAULT_PASSWORD,
                first_name=data['first_name'],
                last_name=data['last_name'],
                is_tourist=True
            )
            print(f"Created tourist: {data['username']}")
        else:
            print(f"Tourist {data['username']} already exists.")

    # --- Create Vendor Users ---
    for data in vendor_data:
        if not User.objects.filter(username=data['username']).exists():
            User.objects.create_user(
                username=data['username'],
                password=DEFAULT_PASSWORD,
                first_name=data['first_name'],
                last_name=data['last_name'],
                is_vendor=True
            )
            print(f"Created vendor: {data['username']}")
        else:
            print(f"Vendor {data['username']} already exists.")

def populate_vendor_data():
    """Populates vendor shops with hardcoded dishes and experiences."""
    print("Populating vendor data...")

    # --- Vendor David's Data ---
    vendor_david = User.objects.get(username='vendor_david')
    # `update_or_create` is used to ensure the shop's details are consistent even if it already exists.
    shop_david, _ = Shop.objects.update_or_create(
        user=vendor_david,
        defaults={
            'business_name': "David's Delicious Dumplings",
            'description': "Serving the best handmade dumplings in town.",
            'location': "123 Orchard Road, Singapore",
            'contact_number': "91234567",
            'opening_hours': "Tue-Sun: 11am - 9pm",
            'dining_establishment_type': 'high_demand_eatery',
        }
    )
    # Create dishes and experiences for David's shop.
    Dish.objects.get_or_create(shop=shop_david, name='Pork Dumplings', defaults={'description': 'Juicy and savory.', 'price': 12.50})
    Dish.objects.get_or_create(shop=shop_david, name='Shrimp Dumplings', defaults={'description': 'Fresh and light.', 'price': 14.00})
    Experience.objects.get_or_create(vendor=shop_david, title='Dumpling Making Workshop', defaults={'description': 'Learn to make your own.', 'price': 80.00})

    # --- Vendor Emily's Data ---
    vendor_emily = User.objects.get(username='vendor_emily')
    shop_emily, _ = Shop.objects.update_or_create(
        user=vendor_emily,
        defaults={
            'business_name': "Emily's Exquisite Eats",
            'description': "A modern take on traditional Singaporean cuisine.",
            'location': "456 Marina Bay, Singapore",
            'contact_number': "98765432",
            'opening_hours': "Mon-Sat: 12pm - 10pm",
            'dining_establishment_type': 'fine_dining',
        }
    )
    Dish.objects.get_or_create(shop=shop_emily, name='Chili Crab Pasta', defaults={'description': 'A fusion delight.', 'price': 28.00})
    Experience.objects.get_or_create(vendor=shop_emily, title='Secret Supper Club', defaults={'description': 'An exclusive dining experience.', 'price': 150.00})

    print("Vendor data population complete.")

def populate_tourist_data():
    """Creates favorites, reviews, and bookings for tourists with hardcoded data."""
    print("Populating tourist data...")

    # Get the user and item objects to link them.
    tourist_anna = User.objects.get(username='tourist_anna')
    tourist_ben = User.objects.get(username='tourist_ben')
    tourist_charlie = User.objects.get(username='tourist_charlie')

    pork_dumplings = Dish.objects.get(name='Pork Dumplings')
    chili_crab_pasta = Dish.objects.get(name='Chili Crab Pasta')
    dumpling_workshop = Experience.objects.get(title='Dumpling Making Workshop')

    # --- Anna's Interactions ---
    # Anna favorites and reviews the pork dumplings, and books the workshop.
    Favorite.objects.get_or_create(user=tourist_anna, content_type=ContentType.objects.get_for_model(pork_dumplings), object_id=pork_dumplings.pk)
    Review.objects.get_or_create(user=tourist_anna, content_type=ContentType.objects.get_for_model(pork_dumplings), object_id=pork_dumplings.pk, defaults={'rating': 5, 'comment': "Absolutely the best dumplings I've ever had!"})
    Booking.objects.get_or_create(user=tourist_anna, content_type=ContentType.objects.get_for_model(dumpling_workshop), object_id=dumpling_workshop.pk, defaults={'date': timezone.now().date() + timedelta(days=10), 'time': '14:00', 'guests': 2, 'status': 'confirmed'})

    # --- Ben's Interactions ---
    # Ben favorites and reviews the chili crab pasta.
    Favorite.objects.get_or_create(user=tourist_ben, content_type=ContentType.objects.get_for_model(chili_crab_pasta), object_id=chili_crab_pasta.pk)
    Review.objects.get_or_create(user=tourist_ben, content_type=ContentType.objects.get_for_model(chili_crab_pasta), object_id=chili_crab_pasta.pk, defaults={'rating': 4, 'comment': "A fantastic and unique dish. Highly recommended."})

    # --- Charlie's Interactions ---
    # Charlie has a past booking for the workshop.
    Booking.objects.get_or_create(user=tourist_charlie, content_type=ContentType.objects.get_for_model(dumpling_workshop), object_id=dumpling_workshop.pk, defaults={'date': timezone.now().date() - timedelta(days=5), 'time': '18:00', 'guests': 4, 'status': 'confirmed'})

    print("Tourist data population complete.")


# This block ensures the functions are called only when the script is executed directly.
if __name__ == '__main__':
    print("Starting test data population...")
    create_test_users()
    populate_vendor_data()
    populate_tourist_data()
    print("Test data population script finished.")
