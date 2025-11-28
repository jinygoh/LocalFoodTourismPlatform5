import os
import django
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
import django
django.setup()

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
        
        # Create Shop Profile
        shop_profile = Shop.objects.create(
            user=vendor_user,
            business_name="Tina's Authentic Eats",
            description="Serving the best home-cooked local delights since 1990.",
            location="Chinatown, Singapore",
            contact_number="+65 9123 4567",
            opening_hours="Mon-Sat: 10am - 8pm",
            latitude=1.2848,
            longitude=103.8439
        )
        
        # Create a few Experiences
        Experience.objects.create(
            vendor=shop_profile,
            title="Traditional Chicken Rice Workshop",
            description="Learn to cook authentic Hainanese Chicken Rice with Tina.",
            price=80.00,
            discount_price=75.00
        )
        Experience.objects.create(
            vendor=shop_profile,
            title="Nyonya Kueh Making Class",
            description="A hands-on session to create colorful and delicious Peranakan sweets.",
            price=65.00
        )
        print(f"Created Vendor: vendor_tina / {password}")
    else:
        print("Vendor user 'vendor_tina' already exists.")

    # 3. Tourist User
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

    # Create a couple of bookings for the tourist user
    first_experience = Experience.objects.first()
    second_experience = Experience.objects.last()
    experience_content_type = ContentType.objects.get_for_model(Experience)

    booking1, created = Booking.objects.get_or_create(
        user=tourist_user,
        content_type=experience_content_type,
        object_id=first_experience.pk,
        defaults={
            'date': datetime.date(2025, 11, 27),
            'guests': 2,
            'status': 'confirmed'
        }
    )
    if created:
        print(f"Created booking for tourist_john for experience: {first_experience.title}")
    elif booking1.status == 'cancelled':
        booking1.status = 'confirmed'
        booking1.save()
        print(f"Reset booking for tourist_john for experience: {first_experience.title}")

    booking2, created = Booking.objects.get_or_create(
        user=tourist_user,
        content_type=experience_content_type,
        object_id=second_experience.pk,
        defaults={
            'date': datetime.date(2025, 11, 30),
            'guests': 4,
            'status': 'confirmed'
        }
    )
    if created:
        print(f"Created booking for tourist_john for experience: {second_experience.title}")
    elif booking2.status == 'cancelled':
        booking2.status = 'confirmed'
        booking2.save()
        print(f"Reset booking for tourist_john for experience: {second_experience.title}")

if __name__ == "__main__":
    create_test_users()
