import os
import django
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
django.setup()

from core.models import User, Shop, Dish, Review
from django.contrib.contenttypes.models import ContentType

def populate_reviews():
    """
    Populates the database with reviews from tourist users for shops and dishes.
    """
    print("Populating reviews...")

    tourists = User.objects.filter(is_tourist=True)
    shops = Shop.objects.all()
    dishes = Dish.objects.all()

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

    shop_content_type = ContentType.objects.get_for_model(Shop)
    dish_content_type = ContentType.objects.get_for_model(Dish)

    for tourist in tourists:
        # Each tourist reviews 2-5 shops
        if shops:
            for shop in random.sample(list(shops), k=random.randint(2, min(5, len(shops)))):
                Review.objects.get_or_create(
                    user=tourist,
                    content_type=shop_content_type,
                    object_id=shop.pk,
                    defaults={
                        'rating': random.randint(3, 5),
                        'comment': random.choice(review_comments)
                    }
                )
                print(f"Added review from {tourist.username} for shop {shop.business_name}")

        # Each tourist reviews 3-7 dishes
        if dishes:
            for dish in random.sample(list(dishes), k=random.randint(3, min(7, len(dishes)))):
                Review.objects.get_or_create(
                    user=tourist,
                    content_type=dish_content_type,
                    object_id=dish.pk,
                    defaults={
                        'rating': random.randint(3, 5),
                        'comment': random.choice(review_comments)
                    }
                )
                print(f"Added review from {tourist.username} for dish {dish.name}")

if __name__ == "__main__":
    populate_reviews()
