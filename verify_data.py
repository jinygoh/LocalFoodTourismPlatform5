import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TasteLocal.settings')
django.setup()

from core.models import Shop, Dish, Experience

print(f"Shops: {Shop.objects.count()}")
print(f"Dishes: {Dish.objects.count()}")
print(f"Experiences: {Experience.objects.count()}")
