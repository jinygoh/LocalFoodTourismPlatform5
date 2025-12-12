"""
This is a standalone script to create a set of test users and associated data.

It is designed to populate the database with a consistent set of users, shops,
experiences, and bookings, which is essential for manual testing and for providing
a consistent state for automated end-to-end tests.

The script is idempotent, meaning it can be run multiple times without creating
duplicate data. It uses `get_or_create` to either fetch existing objects or create
them if they don't exist.
"""
import os
import django
import datetime

# --- Django Setup ---
# This block is necessary to run the script in a standalone context.
# It configures the Django environment and initializes the application.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
django.setup()

# --- Model Imports ---
# Models are imported after `django.setup()` has been called.
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from core.models import Shop, Experience, Booking

# Get the custom User model for this project.
User = get_user_model()

def create_test_users():
    """
    Main function to create all test users and their related data.
    """
    print("Creating/updating test users and data...")
    
    # Define a common password for all test users for convenience.
    password = "TestPass123!"
    
    # --- 1. Admin User ---
    # Ensures a superuser account exists.
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', password)
        print(f"Created Admin: admin / {password}")
    else:
        print("Admin user already exists.")

    # --- 2. Vendor User: Tina ---
    # Creates a vendor user and an associated shop profile with experiences.
    vendor_user, created = User.objects.get_or_create(username='vendor_tina', defaults={
        'email': 'tina@example.com',
        'is_vendor': True
    })
    if created:
        vendor_user.set_password(password)
        vendor_user.save()
        print(f"Created Vendor: vendor_tina / {password}")
    else:
        print("Vendor user 'vendor_tina' already exists.")

    # Create a Shop profile for Tina.
    shop_profile, _ = Shop.objects.get_or_create(
        user=vendor_user,
        defaults={
            'business_name': "Tina's Authentic Eats",
            'description': "Serving the best home-cooked local delights since 1990.",
            'location': "Chinatown, Singapore",
            'contact_number': "+65 9123 4567",
            'opening_hours': "Mon-Sat: 10am - 8pm",
            'latitude': 1.2848,
            'longitude': 103.8439
        }
    )

    # Create a few Experience listings for Tina's shop.
    Experience.objects.get_or_create(
        vendor=shop_profile,
        title="Traditional Chicken Rice Workshop",
        defaults={'description': "Learn to cook authentic Hainanese Chicken Rice with Tina.", 'price': 80.00}
    )
    Experience.objects.get_or_create(
        vendor=shop_profile,
        title="Nyonya Kueh Making Class",
        defaults={'description': "A hands-on session to create colorful and delicious Peranakan sweets.", 'price': 65.00}
    )
    Experience.objects.get_or_create(
        vendor=shop_profile,
        title="Singapore Hawker Food Tour",
        defaults={'description': "Explore the best of Singapore's hawker culture with our guided food tour.", 'price': 50.00}
    )

    # --- 3. Tourist User: John ---
    # Creates a tourist user who will have a booking.
    tourist_user, created = User.objects.get_or_create(username='tourist_john', defaults={
        'email': 'john@example.com',
        'is_tourist': True
    })
    if created:
        tourist_user.set_password(password)
        tourist_user.save()
        print(f"Created Tourist: tourist_john / {password}")
    else:
        print("Tourist user 'tourist_john' already exists.")

    # --- 4. Vendor User: Raj ---
    # Creates a second vendor user with a different shop.
    vendor_raj, created = User.objects.get_or_create(username='vendor_raj', defaults={
        'email': 'raj@example.com',
        'is_vendor': True
    })
    if created:
        vendor_raj.set_password(password)
        vendor_raj.save()
        Shop.objects.create(
            user=vendor_raj,
            business_name="Raj's Modern Indian",
            description="A contemporary twist on classic Indian dishes.",
            location="Little India, Singapore",
            contact_number="+65 8765 4321",
            opening_hours="Tue-Sun: 12pm - 10pm",
            latitude=1.3064,
            longitude=103.8525
        )
        print(f"Created Vendor: vendor_raj / {password}")
    else:
        print("Vendor user 'vendor_raj' already exists.")

    # --- 5. & 6. Additional Tourist Users ---
    # Create more tourist users for variety in testing.
    for username, email in [('tourist_emily', 'emily@example.com'), ('tourist_mike', 'mike@example.com')]:
        user, created = User.objects.get_or_create(username=username, defaults={'email': email, 'is_tourist': True})
        if created:
            user.set_password(password)
            user.save()
            print(f"Created Tourist: {username} / {password}")
        else:
            print(f"Tourist user '{username}' already exists.")

    # --- 7. Create a Booking for Tourist John ---
    # This ensures there is at least one active booking in the system.
    try:
        experience_to_book, _ = Experience.objects.get_or_create(
            vendor=shop_profile,
            title="Traditional Chicken Rice Workshop",
            defaults={'description': "Learn to cook authentic Hainanese Chicken Rice with Tina.", 'price': 80.00}
        )

        # Get the content type for the Experience model to create a generic relationship.
        experience_content_type = ContentType.objects.get_for_model(Experience)

        # Set a future date to ensure the booking is active and visible.
        future_date = datetime.date.today() + datetime.timedelta(days=10)

        # Create or update the booking.
        booking, created = Booking.objects.get_or_create(
            user=tourist_user,
            content_type=experience_content_type,
            object_id=experience_to_book.pk,
            defaults={
                'date': future_date,
                'time': datetime.time(14, 0),  # 2:00 PM
                'guests': 2,
                'status': 'confirmed'
            }
        )

        if created:
            print(f"Created booking for tourist_john for experience: {experience_to_book.title}")
        else:
            # If the booking already exists, ensure it's not cancelled and its date is in the future.
            # This is useful for re-running the script to reset the test state.
            booking.status = 'confirmed'
            booking.date = future_date
            booking.save()
            print(f"Updated existing booking for tourist_john for experience: {experience_to_book.title}")

    except Experience.DoesNotExist:
        print("Could not find the 'Traditional Chicken Rice Workshop' to create a booking.")

# This block ensures the `create_test_users` function is called only when
# the script is executed directly (e.g., `python create_test_users.py`).
if __name__ == "__main__":
    create_test_users()
