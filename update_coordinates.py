import os
import django
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
django.setup()

from core.models import Shop

def update_coordinates():
    print("Updating vendor coordinates with real Singapore locations...")
    
    # List of real Singapore food locations (Lat, Lng, Area Name)
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
    
    vendors = Shop.objects.all()
    for i, vendor in enumerate(vendors):
        # Cycle through the location list
        lat, lng, area_name = locations[i % len(locations)]
        
        vendor.latitude = lat
        vendor.longitude = lng
        # Optionally update the text location to match the coordinates for consistency
        vendor.location = f"{area_name}, Singapore"
        
        vendor.save()
        print(f"Updated {vendor.business_name}: {area_name} ({lat}, {lng})")

if __name__ == "__main__":
    update_coordinates()
