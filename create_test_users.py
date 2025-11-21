import os
import django
from django.contrib.auth import get_user_model

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
django.setup()

from core.models import Vendor, Listing

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
        
        # Create Vendor Profile
        vendor_profile = Vendor.objects.create(
            user=vendor_user,
            business_name="Tina's Authentic Eats",
            description="Serving the best home-cooked local delights since 1990.",
            location="Chinatown, Singapore",
            contact_number="+65 9123 4567",
            opening_hours="Mon-Sat: 10am - 8pm",
            latitude=1.2848,
            longitude=103.8439
        )
        
        # Create a Listing
        Listing.objects.create(
            vendor=vendor_profile,
            title="Traditional Chicken Rice Workshop",
            description="Learn to cook authentic Hainanese Chicken Rice with Tina.",
            price=80.00,
            discount_price=75.00
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

if __name__ == "__main__":
    create_test_users()
