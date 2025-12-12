"""
This is a standalone script to populate the database with a random assortment of reviews
for existing Shops and Dishes.

The script is designed to make the site feel more active and lived-in by:
1.  Fetching all existing tourist users.
2.  Fetching all existing shops and dishes.
3.  For each tourist, creating a random number of reviews for a random sample of
    shops and dishes.

This script is idempotent; it uses `get_or_create` to ensure that it will not
create a duplicate review from the same user for the same item.
"""
import os
import django
import random

# --- Django Setup ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
django.setup()

# --- Model Imports ---
from core.models import User, Shop, Dish, Review
from django.contrib.contenttypes.models import ContentType

def populate_reviews():
    """
    Populates the database with reviews from tourist users for shops and dishes.
    """
    print("Populating reviews...")

    # --- Data Fetching ---
    # Get all users who are marked as tourists.
    tourists = User.objects.filter(is_tourist=True)
    # Get all shops and dishes from the database.
    shops = Shop.objects.all()
    dishes = Dish.objects.all()

    # A list of generic review comments to be used randomly.
    review_comments = [
        "Absolutely amazing! A must-try.",
        "The food was delicious, and the service was excellent.",
        "A bit crowded, but the food was worth the wait.",
        "Good food, but the portion size was a bit small.",
        "I've had better, but it was still a decent meal.",
        "The ambiance was great, but the food was just okay.",
        "I would not recommend this place. The food was cold and tasteless.",
        "A hidden gem! I'll definitely be back.",
        "The best I've ever had!",
        "An unforgettable experience."
    ]

    # Get the ContentType objects for Shop and Dish models.
    # This is necessary for creating reviews with a GenericForeignKey.
    shop_content_type = ContentType.objects.get_for_model(Shop)
    dish_content_type = ContentType.objects.get_for_model(Dish)

    # --- Review Creation Loop ---
    for tourist in tourists:
        # For each tourist, create reviews for a random sample of shops.
        if shops:
            # `random.sample` selects a unique, random subset of shops to review.
            num_reviews = random.randint(2, min(5, len(shops)))
            for shop in random.sample(list(shops), k=num_reviews):
                # `get_or_create` prevents creating a review if one already exists
                # from this user for this shop.
                Review.objects.get_or_create(
                    user=tourist,
                    content_type=shop_content_type,
                    object_id=shop.pk,
                    defaults={
                        'rating': random.randint(3, 5),
                        'comment': random.choice(review_comments)
                    }
                )
                print(f"Added/verified review from {tourist.username} for shop '{shop.business_name}'")

        # For each tourist, create reviews for a random sample of dishes.
        if dishes:
            num_reviews = random.randint(3, min(7, len(dishes)))
            for dish in random.sample(list(dishes), k=num_reviews):
                Review.objects.get_or_create(
                    user=tourist,
                    content_type=dish_content_type,
                    object_id=dish.pk,
                    defaults={
                        'rating': random.randint(3, 5),
                        'comment': random.choice(review_comments)
                    }
                )
                print(f"Added/verified review from {tourist.username} for dish '{dish.name}'")

# --- Script Execution ---
if __name__ == "__main__":
    populate_reviews()
