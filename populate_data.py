import os
import django
import random
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
django.setup()

from core.models import User, Vendor, Listing

def populate():
    print("Populating database with real Singaporean food data...")

    # 1. Create Vendors (Real Singapore Food Brands/Hawkers)
    vendors_data = [
        {"name": "Tian Tian Hainanese Chicken Rice", "loc": "Maxwell Food Centre", "desc": "Michelin-starred chicken rice famous for its fragrant rice and tender chicken."},
        {"name": "Jumbo Seafood", "loc": "East Coast Seafood Centre", "desc": "Home of the award-winning Singapore Chilli Crab."},
        {"name": "328 Katong Laksa", "loc": "51 East Coast Road", "desc": "The original Katong Laksa, rich with coconut milk and spices."},
        {"name": "Song Fa Bak Kut Teh", "loc": "11 New Bridge Road", "desc": "Teochew-style pork rib soup, peppery and tender."},
        {"name": "Hill Street Tai Hwa Pork Noodle", "loc": "Crawford Lane", "desc": "One of the best Bak Chor Mee in Singapore, Michelin-starred."},
        {"name": "Singapore Zam Zam", "loc": "North Bridge Road", "desc": "Legendary Murtabak restaurant established in 1908."},
        {"name": "Old Chang Kee", "loc": "Multiple Locations", "desc": "Famous for their Curry O' and other local snacks."},
        {"name": "Ya Kun Kaya Toast", "loc": "Far East Square", "desc": "Traditional Singaporean breakfast of Kaya Toast and Kopi."},
        {"name": "Newton Food Centre (Ah Heng)", "loc": "Newton Circus", "desc": "Famous for BBQ Stingray and Satay."},
        {"name": "Lau Pa Sat Satay Street", "loc": "Raffles Quay", "desc": "The best open-air Satay experience in the CBD."}
    ]

    vendors = []
    for i, v_data in enumerate(vendors_data):
        username = f"vendor_{i+1}"
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password='password123', is_vendor=True)
            vendor = Vendor.objects.create(
                user=user,
                business_name=v_data['name'],
                description=v_data['desc'],
                location=v_data['loc'],
                contact_number=f"65{random.randint(10000000, 99999999)}"
            )
            vendors.append(vendor)
            print(f"Created Vendor: {v_data['name']}")
        else:
            vendors.append(Vendor.objects.get(user__username=username))

    # 2. Create Listings (30 Real Dishes)
    listings_data = [
        # Tian Tian
        {"vendor": 0, "title": "Signature Chicken Rice", "price": 5.00, "desc": "Steamed chicken served with fragrant oily rice and chili sauce."},
        {"vendor": 0, "title": "Chicken Rice Set", "price": 7.50, "desc": "Includes oyster sauce vegetables and soup."},
        {"vendor": 0, "title": "Whole Steamed Chicken", "price": 28.00, "desc": "Perfect for sharing with family."},
        # Jumbo
        {"vendor": 1, "title": "Award-Winning Chilli Crab", "price": 88.00, "desc": "Mud crab tossed in a sweet, savory, and spicy tomato-based sauce."},
        {"vendor": 1, "title": "Black Pepper Crab", "price": 88.00, "desc": "Stir-fried with robust black pepper and butter."},
        {"vendor": 1, "title": "Cereal Prawns", "price": 24.00, "desc": "Deep-fried prawns coated in crispy, sweet cereal flakes."},
        # 328 Katong
        {"vendor": 2, "title": "Laksa (Small)", "price": 5.50, "desc": "Rice noodles in spicy coconut soup with cockles and prawns."},
        {"vendor": 2, "title": "Laksa (Large)", "price": 7.50, "desc": "A larger serving of the famous Katong Laksa."},
        {"vendor": 2, "title": "Otah", "price": 1.50, "desc": "Spicy fish cake grilled in banana leaf."},
        # Song Fa
        {"vendor": 3, "title": "Pork Ribs Soup", "price": 8.50, "desc": "Signature peppery soup with tender pork ribs."},
        {"vendor": 3, "title": "Braised Pig's Trotter", "price": 9.00, "desc": "Tender trotter braised in dark soy sauce."},
        {"vendor": 3, "title": "Dough Fritters (You Tiao)", "price": 2.50, "desc": "Crispy fritters to dip in the soup."},
        # Tai Hwa
        {"vendor": 4, "title": "Bak Chor Mee (Dry)", "price": 6.00, "desc": "Noodles with minced pork, liver, and vinegar sauce."},
        {"vendor": 4, "title": "Bak Chor Mee (Soup)", "price": 6.00, "desc": "A comforting bowl of noodle soup with pork ingredients."},
        {"vendor": 4, "title": "Meatball Soup", "price": 5.00, "desc": "Handmade pork balls in clear broth."},
        # Zam Zam
        {"vendor": 5, "title": "Chicken Murtabak", "price": 10.00, "desc": "Prata stuffed with spiced chicken, onions, and egg."},
        {"vendor": 5, "title": "Mutton Murtabak", "price": 12.00, "desc": "The classic favorite, stuffed with minced mutton."},
        {"vendor": 5, "title": "Nasi Biryani", "price": 8.00, "desc": "Fragrant basmati rice served with chicken or mutton curry."},
        # Old Chang Kee
        {"vendor": 6, "title": "Curry O'", "price": 1.80, "desc": "Iconic curry puff with chicken, potato, and egg."},
        {"vendor": 6, "title": "Sotong Head Onstik", "price": 2.20, "desc": "Deep-fried squid head on a stick."},
        {"vendor": 6, "title": "Fishball Onstik", "price": 1.80, "desc": "Giant fishballs, bouncy and delicious."},
        # Ya Kun
        {"vendor": 7, "title": "Kaya Toast Set A", "price": 5.60, "desc": "Kaya toast with butter, soft-boiled eggs, and coffee."},
        {"vendor": 7, "title": "Steamed Bread Set", "price": 5.80, "desc": "Soft steamed bread with kaya and butter."},
        {"vendor": 7, "title": "Kopi O", "price": 1.80, "desc": "Traditional black coffee with sugar."},
        # Newton (Ah Heng)
        {"vendor": 8, "title": "Sambal Stingray", "price": 15.00, "desc": "Grilled stingray topped with spicy sambal sauce."},
        {"vendor": 8, "title": "Satay (10 sticks)", "price": 8.00, "desc": "Mixed chicken and beef satay with peanut sauce."},
        {"vendor": 8, "title": "Fried Oyster Omelette", "price": 8.00, "desc": "Crispy egg omelette with plump oysters."},
        # Lau Pa Sat
        {"vendor": 9, "title": "Best Satay Set A", "price": 28.00, "desc": "20 sticks of chicken/beef/mutton + rice cakes."},
        {"vendor": 9, "title": "Grilled Prawns", "price": 20.00, "desc": "Fresh prawns grilled over charcoal."},
        {"vendor": 9, "title": "BBQ Chicken Wings", "price": 1.50, "desc": "Juicy wings with a smoky char."}
    ]

    count = 0
    for item in listings_data:
        vendor = vendors[item['vendor']]
        if not Listing.objects.filter(title=item['title'], vendor=vendor).exists():
            Listing.objects.create(
                vendor=vendor,
                title=item['title'],
                description=item['desc'],
                price=item['price'],
                # We will use a placeholder image service for now to ensure they load
                image=None 
            )
            count += 1
    
    print(f"Successfully created {count} listings.")

if __name__ == '__main__':
    populate()
