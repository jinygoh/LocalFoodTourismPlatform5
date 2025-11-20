import os
import django
import urllib.request
import urllib.parse
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
django.setup()

from core.models import Listing, Vendor

from django.core.files.base import ContentFile

def save_image_from_url(model_instance, prompt, subfolder):
    # Construct a descriptive prompt for better results
    full_prompt = f"high quality photo of {prompt}, singapore food, delicious, 4k, realistic"
    encoded_prompt = urllib.parse.quote(full_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true&seed={model_instance.pk}"
    
    print(f"Fetching: {prompt}...")
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            image_content = response.read()
            
        # Create filename
        safe_name = "".join([c if c.isalnum() else "_" for c in prompt])[:30]
        filename = f"{safe_name}_{model_instance.pk}.jpg"
        
        # Save to model
        model_instance.image.save(filename, ContentFile(image_content), save=True)
        print(f"✅ Saved: {filename}")
        
    except Exception as e:
        print(f"❌ Error for {prompt}: {e}")

print("Starting image generation... This may take a few minutes.")

# 1. Generate for Vendors
print("\n--- Processing Vendors ---")
for vendor in Vendor.objects.all():
    if not vendor.image:
        prompt = f"{vendor.business_name} singapore hawker stall storefront"
        save_image_from_url(vendor, prompt, "vendors")
    else:
        print(f"Skipping {vendor.business_name} (already has image)")

# 2. Generate for Listings
print("\n--- Processing Listings ---")
for listing in Listing.objects.all():
    if not listing.image:
        save_image_from_url(listing, listing.title, "listings")
    else:
        print(f"Skipping {listing.title} (already has image)")

print("\nAll done! Images have been generated and saved to the database.")
