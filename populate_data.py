"""
This script populates the database with a set of realistic Singaporean food data.

NOTE: This script appears to be an older or alternative version of the more
comprehensive `populate_singapore_data.py` and `populate_test_data.py` scripts.
It may be deprecated or intended for a different purpose. It is less idempotent
and could potentially create duplicate data if not used carefully.

The script creates vendors, shops, dishes, experiences, and reviews.
"""
import os
import django
import random
from datetime import date

# --- Django Setup ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
django.setup()

# --- Model Imports ---
from core.models import User, Shop, Dish, Experience, Review

def populate():
    """Main function to run the data population."""
    print("Populating database with real Singaporean food data...")

    # --- 1. Create Shops and associated Vendor Users ---
    # This section contains hardcoded data for famous Singaporean food establishments.
    shops_data = [
        {"name": "Tian Tian Hainanese Chicken Rice", "loc": "Maxwell Food Centre", "desc": "Michelin-starred chicken rice famous for its fragrant rice and tender chicken.", "cat": "hawker_centre"},
        {"name": "Jumbo Seafood", "loc": "East Coast Seafood Centre", "desc": "Home of the award-winning Singapore Chilli Crab.", "cat": "fine_dining"},
        {"name": "328 Katong Laksa", "loc": "51 East Coast Road", "desc": "The original Katong Laksa, rich with coconut milk and spices.", "cat": "casual_cafe"},
        # ... (and so on for all shops)
    ]

    shops = []
    for i, s_data in enumerate(shops_data):
        username = f"vendor_{i+1}"
        # This check is not fully idempotent; it only checks for the user, not the shop.
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password='password123', is_vendor=True)
            shop = Shop.objects.create(
                user=user,
                business_name=s_data['name'],
                description=s_data['desc'],
                location=s_data['loc'],
                # Note: The 'category' field seems to be outdated, as the model uses 'dining_establishment_type'.
                # This may cause errors if the model has been updated.
                category=s_data['cat'],
                contact_number=f"65{random.randint(10000000, 99999999)}"
            )
            shops.append(shop)
            print(f"Created Shop: {s_data['name']}")
        else:
            shops.append(Shop.objects.get(user__username=username))

    # --- 2. Create Dishes ---
    # Dishes are created independently and linked to shops later.
    dishes_data = [
        {"name": "Hainanese Chicken Rice", "desc": "Steamed chicken with fragrant rice."},
        # ... (and so on for all dishes)
    ]

    dishes = []
    for d_data in dishes_data:
        if not Dish.objects.filter(name=d_data['name']).exists():
            dish = Dish.objects.create(name=d_data['name'], description=d_data['desc'])
            dishes.append(dish)
            print(f"Created Dish: {d_data['name']}")
        else:
            dishes.append(Dish.objects.get(name=d_data['name']))

    # --- 3. Create Experiences ---
    experiences_data = [
        {"vendor": shops[1], "title": "Chilli Crab Cooking Class", "price": 75.00, "desc": "Learn to cook Singapore's iconic Chilli Crab..."},
        # ... (and so on for all experiences)
    ]

    experiences = []
    for e_data in experiences_data:
        if not Experience.objects.filter(title=e_data['title']).exists():
            experience = Experience.objects.create(
                vendor=e_data['vendor'],
                title=e_data['title'],
                description=e_data['desc'],
                price=e_data['price']
            )
            experiences.append(experience)
            print(f"Created Experience: {e_data['title']}")
        else:
            experiences.append(Experience.objects.get(title=e_data['title']))

    # --- 4. Link Dishes to Shops (Many-to-Many Relationship) ---
    # This manually creates the relationships between the created shops and dishes.
    shops[0].dishes.add(dishes[0], dishes[1])
    # ... (and so on for all links)

    # --- 5. Link Dishes and Shops to Experiences ---
    experiences[0].dishes.add(dishes[2])
    experiences[0].shops.add(shops[1])
    # ... (and so on for all links)

    # --- 6. Create Reviews ---
    # Creates a single tourist user to be the author of all generated reviews.
    tourist_user, created = User.objects.get_or_create(username='tourist_john', defaults={'is_tourist': True})
    if created:
        tourist_user.set_password('password123')
        tourist_user.save()

    review_comments = [
        "The chicken rice was tender and fragrant, but the queue was a bit long.",
        "Jumbo's Chilli Crab is a must-try! The sauce is simply amazing.",
        # ... (and so on)
    ]

    # Create one review for each dish, shop, and experience.
    for item_list in [dishes, shops, experiences]:
        for item in item_list:
            # This check is not robust as it doesn't account for the ContentType.
            if not Review.objects.filter(object_id=item.pk).exists():
                Review.objects.create(
                    user=tourist_user,
                    content_object=item,
                    rating=random.randint(4, 5),
                    comment=random.choice(review_comments)
                )

    print("Successfully populated the database with realistic data.")

# --- Script Execution ---
if __name__ == '__main__':
    populate()
