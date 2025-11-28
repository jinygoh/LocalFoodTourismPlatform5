print("Script execution started.")
import os
import django
import random
import urllib.request
import urllib.parse
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
django.setup()

from core.models import User, Shop, Dish, Experience, Review

def save_image_from_url(model_instance, prompt):
    full_prompt = f"high quality photo of {prompt}, singapore food, delicious, 4k, realistic"
    encoded_prompt = urllib.parse.quote(full_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true&seed={random.randint(1, 100000)}"

    print(f"Fetching: {prompt}...")

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=60) as response:
            image_content = response.read()

        safe_name = "".join([c if c.isalnum() else "_" for c in prompt])[:30]
        filename = f"{safe_name}_{model_instance.pk}.jpg"

        model_instance.image.save(filename, ContentFile(image_content), save=True)
        print(f"✅ Saved: {filename}")

    except Exception as e:
        print(f"❌ Error for {prompt}: {e}")

def populate():
    print("Populating database with real Singaporean food data...")
    print("Script started. About to define data.")

    shops_data = [
        {"name": "Hock Lai Seng Teochew Fishball Bak Chor Mee", "desc": "Run by the grandson of Ah Ter Teochew Fishball Noodles.", "cat": "hawker_centre"},
        {"name": "Lakeview (Upper Thomson) Kim Goreng Pisang", "desc": "A haven for lovers of fried fritters.", "cat": "hawker_centre"},
        {"name": "Somerset Delicacies", "desc": "Zi char stall with a variety of fried rice options.", "cat": "hawker_centre"},
        {"name": "Sichuan Cuisine", "desc": "Fiery and authentic Sichuan classics.", "cat": "hawker_centre"},
        {"name": "Welcome Ren Min", "desc": "Packaged and draft beers from local and international craft breweries.", "cat": "hawker_centre"}
    ]

    dishes_data = {
        "Hock Lai Seng Teochew Fishball Bak Chor Mee": [
            {"name": "Fishball Bak Chor Mee (Dry)", "desc": "Tossed with ketchup for a tangy-sweet finish."},
            {"name": "Fishball Bak Chor Mee (Soup)", "desc": "A comforting bowl of noodles in a savoury broth."},
            {"name": "Teochew Dumpling Soup", "desc": "A light and flavourful soup with handmade dumplings."},
            {"name": "Fishball Soup", "desc": "Bouncy fishballs in a clear broth."},
            {"name": "Minced Pork Noodles", "desc": "A simple yet satisfying bowl of noodles."}
        ],
        "Lakeview (Upper Thomson) Kim Goreng Pisang": [
            {"name": "Goreng Pisang (Fried Banana)", "desc": "Sweet and crispy fried banana fritters."},
            {"name": "Fried Cempedak", "desc": "A fragrant and sweet fried fruit fritter."},
            {"name": "Fried Nian Gao", "desc": "Chewy and sweet fried rice cake."},
            {"name": "Fried Sweet Potato Balls", "desc": "Crispy on the outside, soft and sweet on the inside."},
            {"name": "You Tiao", "desc": "A classic fried dough fritter."}
        ],
        "Somerset Delicacies": [
            {"name": "Belachan Fried Rice", "desc": "Spicy and flavourful fried rice with shrimp paste."},
            {"name": "Mixed Seafood Hor Fun", "desc": "A generous portion of seafood with smooth rice noodles."},
            {"name": "Salted Fish Fried Rice", "desc": "A classic Cantonese fried rice with a savoury kick."},
            {"name": "Sweet and Sour Pork Rice", "desc": "A popular zi char dish with a perfect balance of flavours."},
            {"name": "Har Cheong Gai (Prawn Paste Chicken)", "desc": "Crispy and aromatic fried chicken marinated in prawn paste."}
        ],
        "Sichuan Cuisine": [
            {"name": "Grilled Fish on Paper", "desc": "Comes in spicy, sauerkraut and tomato flavours."},
            {"name": "La Zi Ji (Spicy Fried Chicken)", "desc": "Fiery and addictive fried chicken with dried chillies."},
            {"name": "Cumin Beef", "desc": "Tender beef slices stir-fried with cumin and spices."},
            {"name": "Mapo Tofu", "desc": "A classic Sichuan dish with a spicy and numbing sauce."},
            {"name": "Mala Baby Lobster", "desc": "A spicy and flavourful dish with baby lobsters."}
        ],
        "Welcome Ren Min": [
            {"name": "Local Craft Beer", "desc": "A rotating selection of beers from Singaporean breweries."},
            {"name": "International Craft Beer", "desc": "A curated selection of beers from around the world."},
            {"name": "Ren Min's Own Brew", "desc": "The stall's very own craft beer."},
            {"name": "Cider", "desc": "A refreshing alternative to beer."},
            {"name": "Bar Snacks", "desc": "A selection of snacks to go with your beer."}
        ]
    }
    print("Data defined. Starting to create shops.")

    shops = []
    for i, s_data in enumerate(shops_data):
        username = f"vendor_singapore_{i+26}"
        user, created = User.objects.get_or_create(username=username, defaults={'is_vendor': True})
        if created:
            user.set_password('password123')
            user.save()

        shop, created = Shop.objects.get_or_create(
            user=user,
            defaults={
                'business_name': s_data['name'],
                'description': s_data['desc'],
                'location': 'Maxwell Food Centre',
                'category': s_data['cat'],
                'contact_number': f"65{random.randint(10000000, 99999999)}"
            }
        )
        if created:
            print(f"Created Shop: {s_data['name']}")
            save_image_from_url(shop, f"{s_data['name']} singapore hawker stall storefront")

        shops.append(shop)

        shop_dishes = []
        for d_data in dishes_data.get(s_data['name'], []):
            dish, created = Dish.objects.get_or_create(
                name=d_data['name'],
                defaults={'description': d_data['desc']}
            )
            if created:
                print(f"  Created Dish: {d_data['name']}")
                save_image_from_url(dish, d_data['name'])

            shop_dishes.append(dish)

        shop.dishes.add(*shop_dishes)

    print("Shops and dishes created. Starting to create experiences.")
    experiences_data = [
    ]

    for e_data in experiences_data:
        try:
            vendor_shop = Shop.objects.get(business_name=e_data['vendor_name'])
            experience, created = Experience.objects.get_or_create(
                title=e_data['title'],
                defaults={
                    'vendor': vendor_shop,
                    'description': e_data['desc'],
                    'price': e_data['price']
                }
            )
            if created:
                print(f"Created Experience: {e_data['title']}")
                save_image_from_url(experience, e_data['title'])

                # Link some relevant dishes and shops to the experience
                experience.shops.add(vendor_shop)
                for dish in vendor_shop.dishes.all():
                    experience.dishes.add(dish)
        except Shop.DoesNotExist:
            print(f"Could not find shop with name {e_data['vendor_name']} to create experience.")

    print("Experiences created. Starting to create reviews.")

    # Create Reviews
    tourist_user, created = User.objects.get_or_create(username='tourist_john', defaults={'is_tourist': True})
    if created:
        tourist_user.set_password('password123')
        tourist_user.save()

    review_comments = [
        "Absolutely delicious! A must-try when in Singapore.",
        "The flavours were authentic and the portions were generous.",
        "A bit of a wait, but totally worth it. I'll be back for more.",
        "Friendly staff and great food. What more could you ask for?",
        "An unforgettable culinary experience. Highly recommended."
    ]

    for shop in Shop.objects.all():
        for dish in shop.dishes.all():
            if not Review.objects.filter(user=tourist_user, object_id=dish.pk).exists():
                Review.objects.create(
                    user=tourist_user,
                    content_object=dish,
                    rating=random.randint(4, 5),
                    comment=random.choice(review_comments)
                )

    print("Successfully populated the database with realistic Singaporean data.")

if __name__ == '__main__':
    populate()
