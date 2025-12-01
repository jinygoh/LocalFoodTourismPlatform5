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
        {"name": "Tian Tian Hainanese Chicken Rice", "desc": "Famous for its tender chicken and fragrant rice.", "cat": "hawker_centre"},
        {"name": "Margaret Drive Sin Kee Chicken Rice", "desc": "A popular choice for chicken rice lovers.", "cat": "hawker_centre"},
        {"name": "Ji De Lai Hainanese Chicken Rice", "desc": "Known for its traditional Hainanese chicken rice.", "cat": "hawker_centre"},
        {"name": "Heng Heng Cooked Food", "desc": "Serving delicious Laksa and Prawn Noodles.", "cat": "hawker_centre"},
        {"name": "Da Shi Jia Big Prawn Mee", "desc": "A must-try for prawn noodle enthusiasts.", "cat": "hawker_centre"},
        {"name": "Jalan Sultan Prawn Mee", "desc": "Famous for its rich and flavorful prawn broth.", "cat": "hawker_centre"},
        {"name": "Fei Fei Roasted • Noodle", "desc": "Serving delicious Wantan Mee.", "cat": "hawker_centre"},
        {"name": "Joo Siah Bak Koot Teh", "desc": "A popular spot for Bak Kut Teh.", "cat": "hawker_centre"},
        {"name": "Song Fa Bak Kut Teh", "desc": "A well-known Bak Kut Teh chain.", "cat": "hawker_centre"},
        {"name": "Ann Chin Handmade Popiah", "desc": "Serving delicious handmade Popiah.", "cat": "hawker_centre"},
        {"name": "Hong Heng Fried Sotong Prawn Mee", "desc": "Famous for its Fried Hokkien Mee.", "cat": "hawker_centre"},
        {"name": "Chey Sua Carrot Cake", "desc": "A must-try for carrot cake lovers.", "cat": "hawker_centre"},
        {"name": "Hill Street Tai Hwa Pork Noodle", "desc": "A Michelin-starred Bak Chor Mee stall.", "cat": "hawker_centre"},
        {"name": "Ru Ji Kitchen", "desc": "Famous for its fishball noodles.", "cat": "hawker_centre"},
        {"name": "Jian Bo Tiong Bahru Shui Kueh", "desc": "A popular spot for Chwee Kueh.", "cat": "hawker_centre"},
        {"name": "Beach Road Fish Head Bee Hoon", "desc": "Famous for its fish head bee hoon.", "cat": "hawker_centre"},
        {"name": "Han Kee", "desc": "Serving delicious fish soup.", "cat": "hawker_centre"},
        {"name": "C.M.Y. Satay", "desc": "A popular spot for satay.", "cat": "hawker_centre"},
        {"name": "Chomp Chomp Satay", "desc": "Another great option for satay.", "cat": "hawker_centre"},
        {"name": "Liao Fan Hawker Chan", "desc": "The cheapest Michelin-starred meal in the world.", "cat": "hawker_centre"},
        {"name": "A Noodle Story", "desc": "Singapore's first and only Michelin-starred ramen.", "cat": "hawker_centre"},
        {"name": "The Blue Ginger", "desc": "A Michelin-starred Peranakan restaurant.", "cat": "restaurant"},
        {"name": "Candlenut", "desc": "The world's first Michelin-starred Peranakan restaurant.", "cat": "restaurant"},
        {"name": "Odette", "desc": "A three-Michelin-starred modern French restaurant.", "cat": "restaurant"},
        {"name": "Les Amis", "desc": "A three-Michelin-starred French restaurant.", "cat": "restaurant"},
        {"name": "Burnt Ends", "desc": "A one-Michelin-starred modern Australian barbecue restaurant.", "cat": "restaurant"},
        {"name": "JAAN by Kirk Westaway", "desc": "A two-Michelin-starred modern British restaurant.", "cat": "restaurant"},
        {"name": "Shoukouwa", "desc": "A two-Michelin-starred sushi restaurant.", "cat": "restaurant"},
        {"name": "Waku Ghin", "desc": "A two-Michelin-starred Japanese restaurant.", "cat": "restaurant"},
        {"name": "Zen", "desc": "A three-Michelin-starred modern European restaurant.", "cat": "restaurant"},
    ]

    dishes_data = {
        "Tian Tian Hainanese Chicken Rice": [
            {"name": "Hainanese Chicken Rice", "desc": "The star dish, poached chicken with fragrant rice."},
            {"name": "Roasted Chicken Rice", "desc": "A crispy alternative to the classic."},
            {"name": "Bean Sprouts with Oyster Sauce", "desc": "A common side dish."},
            {"name": "Chicken Innards", "desc": "For the more adventurous diners."},
            {"name": "Oyster Sauce Vegetables", "desc": "A healthy and delicious side."}
        ],
        "Margaret Drive Sin Kee Chicken Rice": [
            {"name": "Hainanese Chicken Rice", "desc": "Tender poached chicken with flavorful rice."},
            {"name": "Chicken Porridge", "desc": "A comforting and savory porridge."},
            {"name": "Chicken Feet", "desc": "A delicacy for some."},
            {"name": "Braised Egg", "desc": "A simple yet delicious side."},
            {"name": "Soup of the Day", "desc": "A daily selection of comforting soups."}
        ],
        "Ji De Lai Hainanese Chicken Rice": [
            {"name": "Hainanese Chicken Rice", "desc": "A traditional and authentic version of the dish."},
            {"name": "Lemon Chicken", "desc": "A zesty and refreshing alternative."},
            {"name": "Thai Style Tofu", "desc": "A flavorful and spicy tofu dish."},
            {"name": "Salted Vegetable Duck Soup", "desc": "A tangy and savory soup."},
            {"name": "Gado Gado", "desc": "An Indonesian salad with peanut sauce."}
        ],
        "Heng Heng Cooked Food": [
            {"name": "Laksa", "desc": "A rich and spicy coconut milk-based noodle soup."},
            {"name": "Prawn Noodles", "desc": "A flavorful noodle soup with prawns and pork ribs."},
            {"name": "Curry Chicken Noodles", "desc": "A spicy and savory curry noodle dish."},
            {"name": "Fishball Noodles", "desc": "A classic Singaporean noodle dish."},
            {"name": "Mee Siam", "desc": "A sweet and sour noodle dish."}
        ],
        "Da Shi Jia Big Prawn Mee": [
            {"name": "Big Prawn Mee", "desc": "A flavorful noodle soup with large prawns."},
            {"name": "Pork Ribs Prawn Mee", "desc": "A combination of prawns and pork ribs in a rich broth."},
            {"name": "Prawn Noodle Dry", "desc": "A dry version of the popular noodle dish."},
            {"name": "Ngoh Hiang", "desc": "A deep-fried meat roll."},
            {"name": "Fried Wantons", "desc": "Crispy and delicious fried dumplings."}
        ],
        "Jalan Sultan Prawn Mee": [
            {"name": "Prawn Mee", "desc": "A rich and flavorful prawn noodle soup."},
            {"name": "King Prawn Mee", "desc": "A more luxurious version with king prawns."},
            {"name": "Pork Ribs Noodle", "desc": "A savory noodle soup with tender pork ribs."},
            {"name": "Pig's Tail Noodle", "desc": "A unique and flavorful noodle dish."},
            {"name": "Gyoza", "desc": "Japanese-style dumplings."}
        ],
        "Fei Fei Roasted • Noodle": [
            {"name": "Wanton Mee", "desc": "A popular noodle dish with wontons and char siu."},
            {"name": "Roasted Duck Rice", "desc": "Crispy roasted duck with rice."},
            {"name": "Roasted Pork Rice", "desc": "Savory roasted pork with rice."},
            {"name": "Soya Sauce Chicken Rice", "desc": "Tender chicken in a savory soy sauce."},
            {"name": "Dumpling Soup", "desc": "A comforting soup with handmade dumplings."}
        ],
        "Joo Siah Bak Koot Teh": [
            {"name": "Bak Kut Teh", "desc": "A peppery pork rib soup."},
            {"name": "Braised Pig's Trotter", "desc": "A tender and flavorful pork dish."},
            {"name": "Salted Vegetables", "desc": "A tangy and savory side dish."},
            {"name": "You Tiao", "desc": "Fried dough fritters, perfect for dipping in the soup."},
            {"name": "Tau Pok", "desc": "Fried tofu puffs."}
        ],
        "Song Fa Bak Kut Teh": [
            {"name": "Bak Kut Teh", "desc": "A popular peppery pork rib soup."},
            {"name": "Pork Ribs Soup", "desc": "A classic and comforting soup."},
            {"name": "Pork Liver Soup", "desc": "A nutritious and flavorful soup."},
            {"name": "Pork Kidney Soup", "desc": "A unique and flavorful soup."},
            {"name": "Braised Peanuts", "desc": "A simple yet delicious side dish."}
        ],
        "Ann Chin Handmade Popiah": [
            {"name": "Popiah", "desc": "A fresh spring roll with a variety of fillings."},
            {"name": "Kueh Pie Tee", "desc": "A crispy pastry cup filled with similar ingredients to popiah."},
            {"name": "Muah Chee", "desc": "A sticky rice cake coated in peanuts."},
            {"name": "Laksa", "desc": "A rich and spicy coconut milk-based noodle soup."},
            {"name": "Satay", "desc": "Grilled meat skewers with peanut sauce."}
        ],
        "Hong Heng Fried Sotong Prawn Mee": [
            {"name": "Fried Hokkien Mee", "desc": "A stir-fried noodle dish with prawns and squid."},
            {"name": "Char Kway Teow", "desc": "Stir-fried rice noodles with a sweet and savory sauce."},
            {"name": "Oyster Omelette", "desc": "A savory omelette with oysters."},
            {"name": "Satay", "desc": "Grilled meat skewers with peanut sauce."},
            {"name": "Sugarcane Juice", "desc": "A refreshing and sweet drink."}
        ],
        "Chey Sua Carrot Cake": [
            {"name": "Carrot Cake", "desc": "A savory fried radish cake."},
            {"name": "Black Carrot Cake", "desc": "A sweeter version with dark soy sauce."},
            {"name": "White Carrot Cake", "desc": "The classic savory version."},
            {"name": "Oyster Omelette", "desc": "A savory omelette with oysters."},
            {"name": "Popiah", "desc": "A fresh spring roll with a variety of fillings."}
        ],
        "Hill Street Tai Hwa Pork Noodle": [
            {"name": "Bak Chor Mee", "desc": "A popular noodle dish with minced pork and mushrooms."},
            {"name": "Pork Noodle Soup", "desc": "A comforting and savory noodle soup."},
            {"name": "Meatball Soup", "desc": "A simple and delicious soup with meatballs."},
            {"name": "Dumpling Soup", "desc": "A comforting soup with handmade dumplings."},
            {"name": "Seaweed Soup", "desc": "A light and healthy soup."}
        ],
        "Ru Ji Kitchen": [
            {"name": "Fishball Noodles", "desc": "A classic Singaporean noodle dish with fishballs."},
            {"name": "Minced Meat Noodles", "desc": "A savory noodle dish with minced meat."},
            {"name": "Fishball Soup", "desc": "A simple and delicious soup with fishballs."},
            {"name": "Yong Tau Foo", "desc": "A variety of tofu and vegetables stuffed with fish paste."},
            {"name": "Laksa", "desc": "A rich and spicy coconut milk-based noodle soup."}
        ],
        "Jian Bo Tiong Bahru Shui Kueh": [
            {"name": "Chwee Kueh", "desc": "Steamed rice cakes with preserved radish."},
            {"name": "Chee Cheong Fun", "desc": "Steamed rice noodle rolls with a sweet sauce."},
            {"name": "Yam Cake", "desc": "A savory steamed cake made with yam."},
            {"name": "Soon Kueh", "desc": "A steamed dumpling with a turnip filling."},
            {"name": "Peng Kueh", "desc": "A steamed glutinous rice cake with a savory filling."}
        ],
        "Beach Road Fish Head Bee Hoon": [
            {"name": "Fish Head Bee Hoon", "desc": "A milky and flavorful noodle soup with fish head."},
            {"name": "Fried Fish Bee Hoon", "desc": "A version with fried fish slices."},
            {"name": "Fish Soup", "desc": "A clear and light fish soup."},
            {"name": "Tom Yum Soup", "desc": "A spicy and sour Thai soup."},
            {"name": "Prawn Paste Chicken", "desc": "Crispy and savory fried chicken."}
        ],
        "Han Kee": [
            {"name": "Fish Soup", "desc": "A clear and light fish soup with fresh fish slices."},
            {"name": "Fish Porridge", "desc": "A comforting and savory porridge with fish."},
            {"name": "Seafood Soup", "desc": "A flavorful soup with a variety of seafood."},
            {"name": "Sliced Fish Bee Hoon", "desc": "A noodle soup with sliced fish."},
            {"name": "Fish Head Steamboat", "desc": "A communal hot pot with fish head."}
        ],
        "C.M.Y. Satay": [
            {"name": "Chicken Satay", "desc": "Grilled chicken skewers with peanut sauce."},
            {"name": "Mutton Satay", "desc": "Grilled mutton skewers with peanut sauce."},
            {"name": "Pork Satay", "desc": "Grilled pork skewers with peanut sauce."},
            {"name": "Ketupat", "desc": "Rice cakes, a perfect accompaniment to satay."},
            {"name": "Cucumber and Onion", "desc": "A refreshing side for satay."}
        ],
        "Chomp Chomp Satay": [
            {"name": "Chicken Satay", "desc": "Grilled chicken skewers with peanut sauce."},
            {"name": "Beef Satay", "desc": "Grilled beef skewers with peanut sauce."},
            {"name": "Mutton Satay", "desc": "Grilled mutton skewers with peanut sauce."},
            {"name": "Rice Dumplings", "desc": "A savory glutinous rice dumpling."},
            {"name": "Sugarcane Juice", "desc": "A refreshing and sweet drink."}
        ],
        "Liao Fan Hawker Chan": [
            {"name": "Soya Sauce Chicken Rice", "desc": "The famous Michelin-starred dish."},
            {"name": "Roasted Pork Rice", "desc": "Crispy and savory roasted pork."},
            {"name": "Char Siew Rice", "desc": "Sweet and savory barbecued pork."},
            {"name": "Pork Ribs", "desc": "Tender and flavorful pork ribs."},
            {"name": "Wonton Noodles", "desc": "A classic noodle dish with wontons."}
        ],
        "A Noodle Story": [
            {"name": "Singapore-style Ramen", "desc": "A unique fusion of ramen and local flavors."},
            {"name": "Pork Belly Cha-shu", "desc": "Tender and flavorful pork belly."},
            {"name": "Onsen Egg", "desc": "A perfectly cooked soft-boiled egg."},
            {"name": "Potato-wrapped Prawn", "desc": "A crispy and savory side dish."},
            {"name": "Hong Kong-style Wontons", "desc": "Delicious handmade wontons."}
        ],
        "The Blue Ginger": [
            {"name": "Ayam Buah Keluak", "desc": "A classic Peranakan chicken dish."},
            {"name": "Babi Pongteh", "desc": "A savory pork stew."},
            {"name": "Ngo Heong", "desc": "A deep-fried meat roll."},
            {"name": "Chap Chye", "desc": "A mixed vegetable stew."},
            {"name": "Durian Chendol", "desc": "A popular dessert with a modern twist."}
        ],
        "Candlenut": [
            {"name": "Kueh Pie Tee", "desc": "A crispy pastry cup with a savory filling."},
            {"name": "Wing Bean Salad", "desc": "A refreshing and spicy salad."},
            {"name": "Beef Rendang", "desc": "A rich and flavorful beef stew."},
            {"name": "Assam Sotong", "desc": "A tangy and spicy squid dish."},
            {"name": "Buah Keluak Ice Cream", "desc": "A unique and adventurous dessert."}
        ],
        "Odette": [
            {"name": "Pigeon", "desc": "A signature dish, cooked to perfection."},
            {"name": "Foie Gras", "desc": "A luxurious and decadent dish."},
            {"name": "Scallop", "desc": "Fresh and delicate scallops."},
            {"name": "Cheese Trolley", "desc": "A selection of fine cheeses."},
            {"name": "Dessert Trolley", "desc": "A variety of exquisite desserts."}
        ],
        "Les Amis": [
            {"name": "Caviar", "desc": "A luxurious and indulgent dish."},
            {"name": "Lobster", "desc": "Fresh and succulent lobster."},
            {"name": "Wagyu Beef", "desc": "High-quality Japanese beef."},
            {"name": "Wine Pairing", "desc": "An extensive wine list to complement your meal."},
            {"name": "Grand Dessert", "desc": "A spectacular dessert to end your meal."}
        ],
        "Burnt Ends": [
            {"name": "Sanger", "desc": "A delicious and messy pulled pork sandwich."},
            {"name": "King Crab and Garlic", "desc": "A simple yet flavorful dish."},
            {"name": "Beef Marmalade and Pickles", "desc": "A unique and delicious dish."},
            {"name": "Smoked Quail Egg and Caviar", "desc": "A luxurious and smoky bite."},
            {"name": "Wagyu", "desc": "High-quality Japanese beef, cooked to perfection."}
        ],
        "JAAN by Kirk Westaway": [
            {"name": "English Garden", "desc": "A beautiful and delicate vegetable dish."},
            {"name": "Devonshire Cream Tea", "desc": "A modern take on a classic."},
            {"name": "Fish and Chips", "desc": "A refined version of the British classic."},
            {"name": "Pigeon", "desc": "A perfectly cooked pigeon dish."},
            {"name": "Cheese Selection", "desc": "A selection of British cheeses."}
        ],
        "Shoukouwa": [
            {"name": "Omakase", "desc": "A chef's tasting menu of the freshest sushi."},
            {"name": "Uni", "desc": "Fresh and creamy sea urchin."},
            {"name": "Toro", "desc": "Fatty and delicious tuna belly."},
            {"name": "Sake Pairing", "desc": "A selection of fine sakes to complement your meal."},
            {"name": "Japanese Musk Melon", "desc": "A sweet and juicy dessert."}
        ],
        "Waku Ghin": [
            {"name": "Marinated Botan Shrimp with Sea Urchin and Caviar", "desc": "A luxurious and decadent dish."},
            {"name": "Wagyu with Wasabi and Citrus Soy", "desc": "High-quality Japanese beef with a zesty sauce."},
            {"name": "Abalone with Fregola and Tomato", "desc": "A tender and flavorful abalone dish."},
            {"name": "Teppanyaki", "desc": "A variety of grilled dishes, cooked to perfection."},
            {"name": "Japanese Desserts", "desc": "A selection of exquisite Japanese desserts."}
        ],
        "Zen": [
            {"name": "Tasting Menu", "desc": "A multi-course tasting menu of modern European cuisine."},
            {"name": "Scallop and Truffle", "desc": "A luxurious and flavorful dish."},
            {"name": "Pigeon and Foie Gras", "desc": "A rich and decadent dish."},
            {"name": "Wine Pairing", "desc": "An extensive wine list to complement your meal."},
            {"name": "Petit Fours", "desc": "A selection of small sweets to end your meal."}
        ]
    }
    print("Data defined. Starting to create shops.")

    shops = []
    for i, s_data in enumerate(shops_data):
        username = f"vendor_singapore_{i+1}"
        user, created = User.objects.get_or_create(username=username, defaults={'is_vendor': True})
        if created:
            user.set_password('password123')
            user.save()

        shop, created = Shop.objects.get_or_create(
            user=user,
            defaults={
                'business_name': s_data['name'],
                'description': s_data['desc'],
                'location': 'Singapore',
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
        {"title": "Singapore Hawker Food Tour", "desc": "Explore the best of Singapore's hawker culture with our guided food tour.", "price": 50.00, "vendor_name": "Tian Tian Hainanese Chicken Rice"},
        {"title": "Chinatown Food Adventure", "desc": "A guided tour of the best food stalls in Chinatown.", "price": 60.00, "vendor_name": "Liao Fan Hawker Chan"},
        {"title": "Little India Culinary Journey", "desc": "Discover the vibrant flavors of Little India's street food.", "price": 55.00, "vendor_name": "The Blue Ginger"}
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
