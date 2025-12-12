"""
This is a standalone script to generate and save images for existing Shop and Experience
objects in the database that do not already have an image.

It uses an external AI image generation service (Pollinations.ai) to create images
based on the name and title of the models. This is useful for quickly populating
a development or demo database with visually appealing data.

The script is idempotent in that it will skip any model that already has an image.
"""
import os
import django
import urllib.request
import urllib.parse
from django.core.files.base import ContentFile

# --- Django Setup ---
# This is required to run the script in a standalone context.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
django.setup()

# --- Model Imports ---
from core.models import Experience, Shop

def save_image_from_url(model_instance, prompt, subfolder):
    """
    Fetches an image from the AI generation API and saves it to a model instance.

    Args:
        model_instance: The Django model instance (Shop or Experience).
        prompt (str): The text prompt for the image generation.
        subfolder (str): A subfolder name (not currently used in the URL but good practice).
    """
    # Construct a detailed prompt for better image quality.
    full_prompt = f"high quality photo of {prompt}, singapore food, delicious, 4k, realistic"
    encoded_prompt = urllib.parse.quote(full_prompt)
    # Use the model's primary key as a seed for consistent image generation.
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true&seed={model_instance.pk}"
    
    print(f"Fetching: {prompt}...")
    
    try:
        # Make the HTTP request with a user-agent header and a timeout.
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            image_content = response.read()
            
        # Create a safe filename from the prompt.
        safe_name = "".join([c if c.isalnum() else "_" for c in prompt])[:30]
        filename = f"{safe_name}_{model_instance.pk}.jpg"
        
        # Save the downloaded content to the model's ImageField.
        model_instance.image.save(filename, ContentFile(image_content), save=True)
        print(f"✅ Saved: {filename}")
        
    except Exception as e:
        # Catch any exceptions during the download or save process.
        print(f"❌ Error for {prompt}: {e}")

print("Starting image generation... This may take a few minutes.")

# --- Main Script Logic ---

# 1. Generate images for Shop models.
print("\n--- Processing Shops ---")
for shop in Shop.objects.all():
    # Only process shops that do not already have an image.
    if not shop.image:
        prompt = f"{shop.business_name} singapore hawker stall storefront"
        save_image_from_url(shop, prompt, "vendors")
    else:
        print(f"Skipping {shop.business_name} (already has image)")

# 2. Generate images for Experience models.
print("\n--- Processing Experiences ---")
for experience in Experience.objects.all():
    # Only process experiences that do not already have an image.
    if not experience.image:
        save_image_from_url(experience, experience.title, "listings")
    else:
        print(f"Skipping {experience.title} (already has image)")

print("\nAll done! Images have been generated and saved to the database.")
