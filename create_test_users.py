import os
import django
import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from core.models import Shop, Experience, Booking

User = get_user_model()

def create_test_users():
    print("Creating test users...")
    
    # Common password
    password = "TestPass123!"
    
    # 1. Admin User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', password)
        print(f"Created Admin: admin / {password}")
    else:
        print("Admin user already exists.")

    # 2. Vendor User
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

    # Create a few Experiences
    Experience.objects.get_or_create(
        vendor=shop_profile,
        title="Traditional Chicken Rice Workshop",
        defaults={
            'description': "Learn to cook authentic Hainanese Chicken Rice with Tina.",
            'price': 80.00
        }
    )
    Experience.objects.get_or_create(
        vendor=shop_profile,
        title="Nyonya Kueh Making Class",
        defaults={
            'description': "A hands-on session to create colorful and delicious Peranakan sweets.",
            'price': 65.00
        }
    )
    Experience.objects.get_or_create(
        vendor=shop_profile,
        title="Singapore Hawker Food Tour",
        defaults={
            'description': "Explore the best of Singapore's hawker culture with our guided food tour.",
            'price': 50.00
        }
    )

    # 3. Tourist User 1
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

    # 4. New Vendor User
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

    # 5. New Tourist User 2
    tourist_emily, created = User.objects.get_or_create(username='tourist_emily', defaults={
        'email': 'emily@example.com',
        'is_tourist': True
    })
    if created:
        tourist_emily.set_password(password)
        tourist_emily.save()
        print(f"Created Tourist: tourist_emily / {password}")
    else:
        print("Tourist user 'tourist_emily' already exists.")

    # 6. New Tourist User 3
    tourist_mike, created = User.objects.get_or_create(username='tourist_mike', defaults={
        'email': 'mike@example.com',
        'is_tourist': True
    })
    if created:
        tourist_mike.set_password(password)
        tourist_mike.save()
        print(f"Created Tourist: tourist_mike / {password}")
    else:
        print("Tourist user 'tourist_mike' already exists.")

    # Create a booking for the tourist user for a specific experience
    try:
        experience_to_book, _ = Experience.objects.get_or_create(
            vendor=shop_profile,
            title="Traditional Chicken Rice Workshop",
            defaults={
                'description': "Learn to cook authentic Hainanese Chicken Rice with Tina.",
                'price': 80.00
            }
        )
        experience_content_type = ContentType.objects.get_for_model(Experience)

        # Use a future date for the booking to ensure it's active
        future_date = datetime.date.today() + datetime.timedelta(days=10)

        booking, created = Booking.objects.get_or_create(
            user=tourist_user,
            content_type=experience_content_type,
            object_id=experience_to_book.pk,
            defaults={
                'date': future_date,
                'time': datetime.time(14, 0),  # Example time
                'guests': 2,
                'status': 'confirmed'
            }
        )

        if created:
            print(f"Created booking for tourist_john for experience: {experience_to_book.title}")
        elif booking.status == 'cancelled':
            booking.status = 'confirmed'
            booking.date = future_date # Ensure date is in the future
            booking.save()
            print(f"Reset and updated booking for tourist_john for experience: {experience_to_book.title}")
        else:
            # If booking already exists, ensure its date is in the future
            booking.date = future_date
            booking.save()
            print(f"Updated booking date for tourist_john for experience: {experience_to_book.title}")

    except Experience.DoesNotExist:
        print("Could not find the 'Traditional Chicken Rice Workshop' to create a booking.")

if __name__ == "__main__":
    create_test_users()
