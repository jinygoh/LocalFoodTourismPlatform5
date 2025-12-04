import os
import django
import random
import urllib.request
import urllib.parse
import time
import argparse
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
django.setup()

from core.models import User, Shop, Dish, Experience, Review

def save_image_from_url(model_instance, prompt):
    full_prompt = f"high quality photo of {prompt}, singapore food, delicious, 4k, realistic"
    encoded_prompt = urllib.parse.quote(full_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true&seed={random.randint(1, 100000)}"

    print(f"Fetching: {prompt}...")

    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as response:
                image_content = response.read()

            safe_name = "".join([c if c.isalnum() else "_" for c in prompt])[:30]
            filename = f"{safe_name}_{model_instance.pk}.jpg"

            model_instance.image.save(filename, ContentFile(image_content), save=True)
            print(f"✅ Saved: {filename}")
            return # Exit the function on success

        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed for {prompt}: {e}")
            if attempt < 2:
                print("Retrying in 5 seconds...")
                time.sleep(5)

    print(f"❌ Failed to download image for {prompt} after 3 attempts.")


def populate(start, end):
    print("Populating database with real Singaporean food data...")
    print(f"Processing shops from index {start} to {end}")

    # Create test users
    tourist_user, created = User.objects.get_or_create(username='tourist_john', defaults={'is_tourist': True})
    if created:
        tourist_user.set_password('TestPass123!')
        tourist_user.save()

    vendor_user, created = User.objects.get_or_create(username='vendor_tina', defaults={'is_vendor': True})
    if created:
        vendor_user.set_password('TestPass123!')
        vendor_user.save()

    shops_data = [
        {"name": "Tian Tian Hainanese Chicken Rice", "desc": "Famous for its tender chicken and fragrant rice.", "cat": "hawker_centre", "contact": "9691 4852", "hours": "Tue to Sun: 10am - 8pm", "location": "Maxwell Food Centre, 1 Kadayanallur St, #01-10/11, Singapore 069184", "lat": 1.2803, "lon": 103.8449},
        {"name": "Margaret Drive Sin Kee Chicken Rice", "desc": "A popular choice for chicken rice lovers.", "cat": "hawker_centre", "contact": "9691 4852", "hours": "Tue-Sun 11am-8pm", "location": "40 Holland Dr, #01-39, Singapore 270040", "lat": 1.3065, "lon": 103.7946},
        {"name": "Ji De Lai Hainanese Chicken Rice", "desc": "Known for its traditional Hainanese chicken rice.", "cat": "hawker_centre", "contact": "9691 4852", "hours": "8am – 8pm (Mon – Sun)", "location": "Chinatown Complex Market & Food Centre, 335 Smith St, #02-170, Singapore 050335", "lat": 1.2818, "lon": 103.8431},
        {"name": "Heng Heng Cooked Food", "desc": "Serving delicious Laksa and Prawn Noodles.", "cat": "hawker_centre", "contact": "9181 8181", "hours": "8am – 2pm (Mon – Tues, Fri – Sun), Closed Wed, Thurs", "location": "Hong Lim Market & Food Centre, 531A Upper Cross St, #02-09, Singapore 051531", "lat": 1.2841, "lon": 103.8451},
        {"name": "Da Shi Jia Big Prawn Mee", "desc": "A must-try for prawn noodle enthusiasts.", "cat": "hawker_centre", "contact": "+65 6732 1085", "hours": "Daily 11am to 10pm", "location": "89 Killiney Rd, Singapore 239534", "lat": 1.2989, "lon": 103.8436},
        {"name": "Jalan Sultan Prawn Mee", "desc": "Famous for its rich and flavorful prawn broth.", "cat": "hawker_centre", "contact": "+65 6748 2488", "hours": "Daily 8am to 3.30pm (CLOSED on Tuesdays)", "location": "2 Jalan Ayer, Singapore 389141", "lat": 1.3126, "lon": 103.8687},
        {"name": "Fei Fei Roasted • Noodle", "desc": "Serving delicious Wantan Mee.", "cat": "hawker_centre", "contact": "9691 4852", "hours": "Mon-Sat 9:15 AM to 1:00 PM. Closed: Sundays", "location": "Yuhua Village Market and Food Centre, 254 Jurong East St 24, #01-28, Singapore 600254", "lat": 1.3468, "lon": 103.7381},
        {"name": "Joo Siah Bak Koot Teh", "desc": "A popular spot for Bak Kut Teh.", "cat": "hawker_centre", "contact": "9691 4852", "hours": "Tue-Sat 8am to 7.15pm. Sun 8am to 3.30pm. Closed on Mondays", "location": "347 Jurong East Ave 1, #01-220, Singapore 600347", "lat": 1.3475, "lon": 103.7332},
        {"name": "Song Fa Bak Kut Teh", "desc": "A well-known Bak Kut Teh chain.", "cat": "hawker_centre", "contact": "+65 6377 6311", "hours": "10:30am-9:30pm, daily", "location": "11 New Bridge Rd, #01-01, Singapore 059383", "lat": 1.2858, "lon": 103.8463},
        {"name": "Ann Chin Handmade Popiah", "desc": "Serving delicious handmade Popiah.", "cat": "hawker_centre", "contact": "+65 8189 4699", "hours": "8am to 7pm daily", "location": "Chinatown Complex Market & Food Centre, 335 Smith St, #02-112, Singapore 050335", "lat": 1.2818, "lon": 103.8431},
        {"name": "Hong Heng Fried Sotong Prawn Mee", "desc": "Famous for its Fried Hokkien Mee.", "cat": "hawker_centre", "contact": "9691 4852", "hours": "10.30am-2.30pm, 4.30pm-6pm (closed on Sundays & Mondays)", "location": "Tiong Bahru Market, 30 Seng Poh Rd, #02-01, Singapore 168898", "lat": 1.2850, "lon": 103.8329},
        {"name": "Chey Sua Carrot Cake", "desc": "A must-try for carrot cake lovers.", "cat": "hawker_centre", "contact": "9691 4852", "hours": "Tue – Sun 6am to 1pm, closed on Mon", "location": "Toa Payoh West Market and Food Court, 127 Lor 1 Toa Payoh, #02-30, Singapore 310127", "lat": 1.3323, "lon": 103.8459},
        {"name": "Hill Street Tai Hwa Pork Noodle", "desc": "A Michelin-starred Bak Chor Mee stall.", "cat": "hawker_centre", "contact": "+65 9272 3920", "hours": "Monday to Sunday 9:00 Am - 8:30 Pm (close 1st and 3rd Monday every month)", "location": "466 Crawford Ln, #01-12, Singapore 190466", "lat": 1.3065, "lon": 103.8617},
        {"name": "Ru Ji Kitchen", "desc": "Famous for its fishball noodles.", "cat": "hawker_centre", "contact": "94350820", "hours": "7am – 1pm (Tue – Sun), Closed Mon", "location": "Old Airport Road Food Centre, 51 Old Airport Rd, #01-37, Singapore 390051", "lat": 1.3085, "lon": 103.8850},
        {"name": "Jian Bo Tiong Bahru Shui Kueh", "desc": "A popular spot for Chwee Kueh.", "cat": "hawker_centre", "contact": "+65 6384 5379", "hours": "5.30am - 8.30pm", "location": "Tiong Bahru Market, 30 Seng Poh Rd, #02-05, Singapore 168898", "lat": 1.2850, "lon": 103.8329},
        {"name": "Beach Road Fish Head Bee Hoon", "desc": "Famous for its fish head bee hoon.", "cat": "hawker_centre", "contact": "9691 4852", "hours": "9am to 2pm daily. Closed on Wednesdays and Saturdays.", "location": "Whampoa Makan Place, 91 Whampoa Dr, #01-46, Singapore 320091", "lat": 1.3218, "lon": 103.8557},
        {"name": "Han Kee", "desc": "Serving delicious fish soup.", "cat": "hawker_centre", "contact": "9691 4852", "hours": "Mon – Fri. 10:30AM - 3:00PM. Closed Sat, Sun", "location": "Amoy Street Food Centre, 7 Maxwell Rd, #02-129, Singapore 069111", "lat": 1.2785, "lon": 103.8465},
        {"name": "C.M.Y. Satay", "desc": "A popular spot for satay.", "cat": "hawker_centre", "contact": "9475 2907", "hours": "Tues-Sun 9am to 7pm, Closed on Mondays", "location": "Lau Pa Sat, 18 Raffles Quay, Singapore 048582", "lat": 1.2798, "lon": 103.8505},
        {"name": "Chomp Chomp Satay", "desc": "Another great option for satay.", "cat": "hawker_centre", "contact": "9691 4852", "hours": "5:30pm – Late about midnight (Mon – Sun)", "location": "Chomp Chomp Food Centre, 20 Kensington Park Rd, Singapore 557269", "lat": 1.3639, "lon": 103.8631},
        {"name": "Liao Fan Hawker Chan", "desc": "The cheapest Michelin-starred meal in the world.", "cat": "hawker_centre", "contact": "+65 6272 2000", "hours": "Open daily 10.30am – 8pm", "location": "78 Smith St, Singapore 058972", "lat": 1.2825, "lon": 103.8433},
        {"name": "A Noodle Story", "desc": "Singapore's first and only Michelin-starred ramen.", "cat": "hawker_centre", "contact": "+65 9027 6289", "hours": "Monday to Friday: 11:15am to 2pm, 5:15pm to 7pm. Saturday: 10:45am to 1:15pm. Closed on Sunday.", "location": "Amoy Street Food Centre, 7 Maxwell Rd, #01-39, Singapore 069111", "lat": 1.2785, "lon": 103.8465},
        {"name": "The Blue Ginger", "desc": "A Michelin-starred Peranakan restaurant.", "cat": "restaurant", "contact": "(+65) 6222 3928", "hours": "Mondays – Sundays Lunch : 12pm – 3pm, Dinner : 6.30pm – 10.30pm", "location": "97 Tanjong Pagar Rd, Singapore 088518", "lat": 1.2783, "lon": 103.8434},
        {"name": "Candlenut", "desc": "The world's first Michelin-starred Peranakan restaurant.", "cat": "restaurant", "contact": "1800 304 2288", "hours": "LUNCH, MON – SUN 12:00PM – 3:00PM, DINNER, MON – SUN AND EVE OF PUBLIC HOLIDAYS 6:00PM – 10:00PM", "location": "17A Dempsey Rd, Singapore 249676", "lat": 1.3046, "lon": 103.8073},
        {"name": "Odette", "desc": "A three-Michelin-starred modern French restaurant.", "cat": "restaurant", "contact": "+65 6385 0498", "hours": "LUNCH TUESDAY TO SATURDAY 12.00pm to 1.15pm, DINNER MONDAY TO SATURDAY 6.30pm to 8.15pm, Closed on Sunday", "location": "1 St Andrew's Rd, #01-04 National Gallery, Singapore 178957", "lat": 1.2896, "lon": 103.8520},
        {"name": "Les Amis", "desc": "A three-Michelin-starred French restaurant.", "cat": "restaurant", "contact": "+65 6733 2225", "hours": "Daily 12.00 to 14.00, 19.00 to 21.30", "location": "1 Scotts Rd, #01-16 Shaw Centre, Singapore 228208", "lat": 1.3050, "lon": 103.8322},
        {"name": "Burnt Ends", "desc": "A one-Michelin-starred modern Australian barbecue restaurant.", "cat": "restaurant", "contact": "+65 6224 3933", "hours": "Lunch: Fri – Sat, Dinner: Tues – Sat", "location": "7 Dempsey Rd, #01-04, Singapore 249671", "lat": 1.3046, "lon": 103.8073},
        {"name": "JAAN by Kirk Westaway", "desc": "A two-Michelin-starred modern British restaurant.", "cat": "restaurant", "contact": "+65 9199 9008", "hours": "Lunch (Tue to Sat): 11:45am to 2:30pm, Dinner (Tues to Sat): 6:30pm to 10:30pm", "location": "2 Stamford Rd, Level 70, Swissôtel The Stamford, Singapore 178882", "lat": 1.2929, "lon": 103.8526},
        {"name": "Shoukouwa", "desc": "A two-Michelin-starred sushi restaurant.", "cat": "restaurant", "contact": "+65 6423 9939", "hours": "Lunch Tuesday to Saturday 12.30pm to 3pm, Dinner Tuesday to Saturday 1st seating: 6pm to 8pm 2nd seating: 8.15pm to 10.30pm. Closed on Sunday and Monday.", "location": "1 Fullerton Rd, #02-02A One Fullerton, Singapore 049213", "lat": 1.2856, "lon": 103.8550},
        {"name": "Waku Ghin", "desc": "A two-Michelin-starred Japanese restaurant.", "cat": "restaurant", "contact": "+65 6688 8507", "hours": "Tuesday – Sunday: 5.30pm & 8pm ( 2 seatings)", "location": "2 Bayfront Ave, #02-01, The Shoppes at Marina Bay Sands, Singapore 018972", "lat": 1.2830, "lon": 103.8602},
        {"name": "Zen", "desc": "A three-Michelin-starred modern European restaurant.", "cat": "restaurant", "contact": "+65 6534 8880", "hours": "Tuesday – Saturday: 7:00pm – 10:30pm", "location": "41 Bukit Pasoh Rd, Singapore 089855", "lat": 1.2796, "lon": 103.8415},
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
            {"name": "Wine Pairing", "desc": "An extensive wine list to complement your meal."},
            {"name": "Petit Fours", "desc": "A selection of small sweets to end your meal."}
        ]
    }

    shops_to_process = shops_data[start:end]

    print(f"Data defined. Starting to create {len(shops_to_process)} shops.")

    shops = []
    for i, s_data in enumerate(shops_to_process):
        username = f"vendor_singapore_{start + i + 1}"
        user, created = User.objects.get_or_create(username=username, defaults={'is_vendor': True})
        if created:
            user.set_password('password123')
            user.save()

        shop, created = Shop.objects.get_or_create(
            user=user,
            defaults={
                'business_name': s_data['name'],
                'description': s_data['desc'],
                'location': s_data['location'],
                'latitude': s_data['lat'],
                'longitude': s_data['lon'],
                'category': s_data['cat'],
                'contact_number': s_data['contact'],
                'opening_hours': s_data['hours']
            }
        )
        if created:
            print(f"Created Shop: {s_data['name']}")
            save_image_from_url(shop, f"{s_data['name']} singapore hawker stall storefront")
        else:
             # Update existing shop
            shop.business_name = s_data['name']
            shop.description = s_data['desc']
            shop.location = s_data['location']
            shop.latitude = s_data['lat']
            shop.longitude = s_data['lon']
            shop.category = s_data['cat']
            shop.contact_number = s_data['contact']
            shop.opening_hours = s_data['hours']
            shop.save()
            print(f"Updated Shop: {s_data['name']}")

        shops.append(shop)

        for d_data in dishes_data.get(s_data['name'], []):
            dish, created = Dish.objects.get_or_create(
                shop=shop,
                name=d_data['name'],
                defaults={
                    'description': d_data['desc'],
                    'price': round(random.uniform(5.0, 50.0), 2)
                }
            )
            if created:
                print(f"  Created Dish: {d_data['name']} for {shop.business_name}")
                save_image_from_url(dish, f"{d_data['name']} from {shop.business_name}")

    # Only create experiences and reviews on the final run to avoid duplicates
    if end >= len(shops_data):
        print("Shops and dishes created. Starting to create experiences.")
        experiences_data = [
            {"title": "Singapore Hawker Food Tour", "desc": "Explore the best of Singapore's hawker culture with our guided food tour.", "price": 50.00, "vendor_name": "Tian Tian Hainanese Chicken Rice"},
            {"title": "Chinatown Food Adventure", "desc": "A guided tour of the best food stalls in Chinatown.", "price": 60.00, "vendor_name": "Liao Fan Hawker Chan"},
            {"title": "Little India Culinary Journey", "desc": "Discover the vibrant flavors of Little India's street food.", "price": 55.00, "vendor_name": "The Blue Ginger"},
            {"title": "Michelin Starred Hawker Crawl", "desc": "Taste the cheapest Michelin-starred meals in the world.", "price": 75.00, "vendor_name": "Hill Street Tai Hwa Pork Noodle"},
            {"title": "Seafood Discovery Tour", "desc": "A tour dedicated to Singapore's best seafood dishes.", "price": 80.00, "vendor_name": "Da Shi Jia Big Prawn Mee"},
            {"title": "Peranakan Cuisine Workshop", "desc": "Learn to cook authentic Peranakan dishes.", "price": 90.00, "vendor_name": "Candlenut"},
            {"title": "Late Night Supper Trail", "desc": "Explore Singapore's vibrant late-night food scene.", "price": 45.00, "vendor_name": "Chomp Chomp Satay"},
            {"title": "Bak Kut Teh Bonanza", "desc": "A tour for lovers of the iconic pork rib soup.", "price": 50.00, "vendor_name": "Song Fa Bak Kut Teh"},
            {"title": "The Ultimate Chicken Rice Challenge", "desc": "Taste and compare the best chicken rice in Singapore.", "price": 65.00, "vendor_name": "Margaret Drive Sin Kee Chicken Rice"},
            {"title": "Noodle Nirvana Tour", "desc": "A journey through the best noodle dishes Singapore has to offer.", "price": 60.00, "vendor_name": "A Noodle Story"},
            {"title": "Sweet Treats and Desserts Tour", "desc": "Discover Singapore's best local desserts.", "price": 40.00, "vendor_name": "Jian Bo Tiong Bahru Shui Kueh"},
            {"title": "Vegetarian Foodie Walk", "desc": "A tour of the best vegetarian-friendly hawker stalls.", "price": 55.00, "vendor_name": "Ann Chin Handmade Popiah"},
            {"title": "Tiong Bahru Market Exploration", "desc": "A deep dive into one of Singapore's most iconic markets.", "price": 50.00, "vendor_name": "Hong Heng Fried Sotong Prawn Mee"},
            {"title": "Fine Dining Experience", "desc": "A curated evening at one of Singapore's top restaurants.", "price": 250.00, "vendor_name": "Odette"},
            {"title": "Modern Singaporean Food Tour", "desc": "Explore the innovative and modern side of Singaporean cuisine.", "price": 85.00, "vendor_name": "Burnt Ends"},
            {"title": "Sushi Masterclass", "desc": "Learn the art of sushi making from a master.", "price": 150.00, "vendor_name": "Shoukouwa"},
            {"title": "French Gastronomy in Singapore", "desc": "Experience the best of French cuisine in the heart of Singapore.", "price": 200.00, "vendor_name": "Les Amis"},
            {"title": "British Classics with a Twist", "desc": "A unique dining experience of modern British cuisine.", "price": 180.00, "vendor_name": "JAAN by Kirk Westaway"},
            {"title": "Japanese Teppanyaki Spectacle", "desc": "Enjoy a spectacular teppanyaki performance and meal.", "price": 120.00, "vendor_name": "Waku Ghin"},
            {"title": "A Culinary Journey with Zen", "desc": "An unforgettable multi-course tasting menu.", "price": 300.00, "vendor_name": "Zen"}
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

                    experience.shops.add(vendor_shop)
                    for dish in vendor_shop.dishes.all():
                        experience.dishes.add(dish)
            except Shop.DoesNotExist:
                print(f"Could not find shop with name {e_data['vendor_name']} to create experience.")

        print("Experiences created. Starting to create reviews.")
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0, help="Starting index of shops to process")
    parser.add_argument("--end", type=int, default=30, help="Ending index of shops to process")
    args = parser.parse_args()
    populate(args.start, args.end)
