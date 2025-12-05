import os
import django
import random
from faker import Faker
from django.contrib.contenttypes.models import ContentType

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
django.setup()

from core.models import User, Shop, Dish, Experience, Review

fake = Faker()

def create_tourists(num_tourists):
    for _ in range(num_tourists):
        username = fake.user_name()
        password = 'password123'
        user, created = User.objects.get_or_create(username=username, defaults={'is_tourist': True})
        if created:
            user.set_password(password)
            user.save()

def populate_reviews():
    tourists = User.objects.filter(is_tourist=True)
    shops = Shop.objects.all()
    dishes = Dish.objects.all()
    experiences = Experience.objects.all()

    shop_content_type = ContentType.objects.get_for_model(Shop)
    dish_content_type = ContentType.objects.get_for_model(Dish)
    experience_content_type = ContentType.objects.get_for_model(Experience)

    review_comments = [
        "Absolutely delicious! A must-try when in Singapore.",
        "The flavours were authentic and the portions were generous.",
        "A bit of a wait, but totally worth it. I'll be back for more.",
        "Friendly staff and great food. What more could you ask for?",
        "An unforgettable culinary experience. Highly recommended."
    ]

    for tourist in tourists:
        for shop in shops:
            if not Review.objects.filter(user=tourist, content_type=shop_content_type, object_id=shop.pk).exists():
                Review.objects.create(
                    user=tourist,
                    content_object=shop,
                    rating=random.randint(3, 5),
                    comment=random.choice(review_comments)
                )

        for dish in dishes:
            if not Review.objects.filter(user=tourist, content_type=dish_content_type, object_id=dish.pk).exists():
                Review.objects.create(
                    user=tourist,
                    content_object=dish,
                    rating=random.randint(3, 5),
                    comment=random.choice(review_comments)
                )

        for experience in experiences:
            if not Review.objects.filter(user=tourist, content_type=experience_content_type, object_id=experience.pk).exists():
                Review.objects.create(
                    user=tourist,
                    content_object=experience,
                    rating=random.randint(3, 5),
                    comment=random.choice(review_comments)
                )

if __name__ == '__main__':
    num_tourists = 10
    create_tourists(num_tourists)
    populate_reviews()
    print(f"Successfully created {num_tourists} tourist accounts and populated reviews.")
