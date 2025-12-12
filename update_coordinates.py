"""
This is a standalone utility script to update the geographic coordinates (latitude and
longitude) and location text for all existing Shops in the database.

It uses a predefined list of real-world Singaporean food locations. The script
iterates through all the `Shop` objects and assigns them a location from the list
in a cyclical manner.

This is useful for ensuring that the data used for map functionalities is realistic
and corresponds to actual locations in Singapore.
"""
import os
import django

# --- Django Setup ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
django.setup()

# --- Model Imports ---
from core.models import Shop

def update_coordinates():
    """
    Updates all shops with coordinates and location names from a predefined list.
    """
    print("Updating vendor coordinates with real Singapore locations...")
    
    # A list of real Singapore food locations, containing tuples of
    # (latitude, longitude, area_name).
    locations = [
        (1.2848, 103.8439, "Chinatown Complex"),
        (1.3007, 103.8542, "Albert Centre Market & Food Centre"),
        (1.3075, 103.8631, "Golden Mile Food Centre"),
        (1.2726, 103.8168, "Alexandra Village Food Centre"),
        (1.3119, 103.7963, "Holland Village Market & Food Centre"),
        (1.3240, 103.9324, "Bedok Interchange Hawker Centre"),
        (1.3526, 103.8729, "Chomp Chomp Food Centre"),
        (1.3094, 103.8858, "Old Airport Road Food Centre"),
        (1.2816, 103.8442, "Maxwell Food Centre"),
        (1.2949, 103.8568, "Tekka Centre"),
        (1.2784, 103.8376, "Tiong Bahru Market"),
        (1.3323, 103.8482, "Toa Payoh West Market & Food Centre"),
        (1.3038, 103.9012, "East Coast Lagoon Food Village"),
        (1.2863, 103.8594, "Makansutra Gluttons Bay"),
        (1.2758, 103.8515, "Lau Pa Sat"),
    ]
    
    # Get all Shop objects from the database.
    shops = Shop.objects.all()

    # Iterate through all shops and assign a location from the list.
    for i, shop in enumerate(shops):
        # The modulo operator `%` ensures that we cycle through the `locations` list
        # if there are more shops than available locations.
        lat, lng, area_name = locations[i % len(locations)]
        
        # Update the latitude and longitude fields.
        shop.latitude = lat
        shop.longitude = lng

        # Also update the text-based location field for consistency in the UI.
        shop.location = f"{area_name}, Singapore"
        
        # Save the changes to the database.
        shop.save()
        print(f"Updated '{shop.business_name}' to: {area_name} ({lat}, {lng})")

# --- Script Execution ---
if __name__ == "__main__":
    update_coordinates()
