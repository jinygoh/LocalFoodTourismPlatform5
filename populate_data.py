import os
import django
import random
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
django.setup()

from core.models import User, Shop, Dish, Experience, Review

def populate():
    print("Populating database with real Singaporean food data...")

    # 1. Create Shops (Real Singapore Food Brands/Hawkers)
    shops_data = [
        {"name": "Tian Tian Hainanese Chicken Rice", "loc": "Maxwell Food Centre", "desc": "Michelin-starred chicken rice famous for its fragrant rice and tender chicken.", "cat": "hawker_centre"},
        {"name": "Jumbo Seafood", "loc": "East Coast Seafood Centre", "desc": "Home of the award-winning Singapore Chilli Crab.", "cat": "fine_dining"},
        {"name": "328 Katong Laksa", "loc": "51 East Coast Road", "desc": "The original Katong Laksa, rich with coconut milk and spices.", "cat": "casual_cafe"},
        {"name": "Song Fa Bak Kut Teh", "loc": "11 New Bridge Road", "desc": "Teochew-style pork rib soup, peppery and tender.", "cat": "casual_cafe"},
        {"name": "Hill Street Tai Hwa Pork Noodle", "loc": "Crawford Lane", "desc": "One of the best Bak Chor Mee in Singapore, Michelin-starred.", "cat": "hawker_centre"},
        {"name": "Singapore Zam Zam", "loc": "North Bridge Road", "desc": "Legendary Murtabak restaurant established in 1908.", "cat": "casual_cafe"},
        {"name": "Old Chang Kee", "loc": "Multiple Locations", "desc": "Famous for their Curry O' and other local snacks.", "cat": "fast_food"},
        {"name": "Ya Kun Kaya Toast", "loc": "Far East Square", "desc": "Traditional Singaporean breakfast of Kaya Toast and Kopi.", "cat": "casual_cafe"},
        {"name": "Newton Food Centre (Alliance Seafood)", "loc": "Newton Circus", "desc": "Famous for BBQ Stingray and Satay.", "cat": "hawker_centre"},
        {"name": "Lau Pa Sat (Stall 7 & 8)", "loc": "Raffles Quay", "desc": "The best open-air Satay experience in the CBD.", "cat": "hawker_centre"}
    ]

    shops = []
    for i, s_data in enumerate(shops_data):
        username = f"vendor_{i+1}"
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password='password123', is_vendor=True)
            shop = Shop.objects.create(
                user=user,
                business_name=s_data['name'],
                description=s_data['desc'],
                location=s_data['loc'],
                category=s_data['cat'],
                contact_number=f"65{random.randint(10000000, 99999999)}"
            )
            shops.append(shop)
            print(f"Created Shop: {s_data['name']}")
        else:
            shops.append(Shop.objects.get(user__username=username))

    # 2. Create Dishes
    dishes_data = [
        # Tian Tian
        {"name": "Hainanese Chicken Rice", "desc": "Steamed chicken with fragrant rice."},
        {"name": "Roasted Chicken Rice", "desc": "Roasted chicken with fragrant rice."},
        # Jumbo Seafood
        {"name": "Chilli Crab", "desc": "Crab in a sweet and spicy sauce."},
        {"name": "Black Pepper Crab", "desc": "Crab in a black pepper sauce."},
        # 328 Katong Laksa
        {"name": "Laksa", "desc": "Spicy coconut noodle soup."},
        # Song Fa Bak Kut Teh
        {"name": "Bak Kut Teh", "desc": "Peppery pork rib soup."},
        # Hill Street Tai Hwa Pork Noodle
        {"name": "Bak Chor Mee", "desc": "Minced pork noodles."},
        # Singapore Zam Zam
        {"name": "Mutton Murtabak", "desc": "Stuffed prata pancake with mutton."},
        {"name": "Chicken Murtabak", "desc": "Stuffed prata pancake with chicken."},
        # Old Chang Kee
        {"name": "Curry'O", "desc": "A baked pastry with a savory filling."},
        # Ya Kun Kaya Toast
        {"name": "Kaya Toast", "desc": "Toast with coconut jam."},
        # Newton Food Centre
        {"name": "BBQ Stingray", "desc": "Stingray grilled with sambal."},
        # Lau Pa Sat
        {"name": "Satay", "desc": "Grilled meat skewers."}
    ]

    dishes = []
    for d_data in dishes_data:
        if not Dish.objects.filter(name=d_data['name']).exists():
            dish = Dish.objects.create(name=d_data['name'], description=d_data['desc'])
            dishes.append(dish)
            print(f"Created Dish: {d_data['name']}")
        else:
            dishes.append(Dish.objects.get(name=d_data['name']))

    # 3. Create Experiences
    experiences_data = [
        {"vendor": shops[1], "title": "Chilli Crab Cooking Class", "price": 75.00, "desc": "Learn to cook Singapore's iconic Chilli Crab from the masters at Jumbo Seafood."},
        {"vendor": shops[7], "title": "Kaya Toast & Kopi Workshop", "price": 45.00, "desc": "Master the art of traditional Singaporean breakfast with Ya Kun Kaya Toast."},
        {"vendor": shops[0], "title": "Maxwell Food Centre Hawker Tour", "price": 60.00, "desc": "A guided food tour of one of Singapore's most famous hawker centres, featuring Tian Tian Hainanese Chicken Rice and more."},
        {"vendor": shops[8], "title": "Newton Food Centre Seafood Feast", "price": 80.00, "desc": "A curated feast of the best seafood dishes at Newton Food Centre, including the famous BBQ Stingray from Alliance Seafood."},
        {"vendor": shops[9], "title": "Lau Pa Sat Satay Street Adventure", "price": 70.00, "desc": "Experience the vibrant atmosphere and delicious satay of Lau Pa Sat's famous Satay Street."}
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

    # 4. Link Dishes to Shops
    shops[0].dishes.add(dishes[0], dishes[1])
    shops[1].dishes.add(dishes[2], dishes[3])
    shops[2].dishes.add(dishes[4])
    shops[3].dishes.add(dishes[5])
    shops[4].dishes.add(dishes[6])
    shops[5].dishes.add(dishes[7], dishes[8])
    shops[6].dishes.add(dishes[9])
    shops[7].dishes.add(dishes[10])
    shops[8].dishes.add(dishes[11])
    shops[9].dishes.add(dishes[12])

    # 5. Link Dishes and Shops to Experiences
    experiences[0].dishes.add(dishes[2])
    experiences[0].shops.add(shops[1])
    experiences[1].dishes.add(dishes[10])
    experiences[1].shops.add(shops[7])
    experiences[2].dishes.add(dishes[0], dishes[1])
    experiences[2].shops.add(shops[0])
    experiences[3].dishes.add(dishes[11])
    experiences[3].shops.add(shops[8])
    experiences[4].dishes.add(dishes[12])
    experiences[4].shops.add(shops[9])

    # 6. Create Reviews
    tourist_user, created = User.objects.get_or_create(username='tourist_john', defaults={'is_tourist': True})
    if created:
        tourist_user.set_password('password123')
        tourist_user.save()

    review_comments = [
        "The chicken rice was tender and fragrant, but the queue was a bit long.",
        "Jumbo's Chilli Crab is a must-try! The sauce is simply amazing.",
        "328 Katong Laksa is the best laksa in Singapore, hands down.",
        "Song Fa's Bak Kut Teh is the perfect comfort food on a rainy day.",
        "The Bak Chor Mee at Tai Hwa is worth the wait. The vinegar and chili sauce is a perfect combination.",
    ]

    for dish in dishes:
        if not Review.objects.filter(object_id=dish.pk).exists():
            Review.objects.create(
                user=tourist_user,
                content_object=dish,
                rating=random.randint(4, 5),
                comment=random.choice(review_comments)
            )

    for shop in shops:
        if not Review.objects.filter(object_id=shop.pk).exists():
            Review.objects.create(
                user=tourist_user,
                content_object=shop,
                rating=random.randint(4, 5),
                comment=random.choice(review_comments)
            )

    for experience in experiences:
        if not Review.objects.filter(object_id=experience.pk).exists():
            Review.objects.create(
                user=tourist_user,
                content_object=experience,
                rating=random.randint(4, 5),
                comment=random.choice(review_comments)
            )

    print("Successfully populated the database with realistic data.")

if __name__ == '__main__':
    populate()
