import pytest
from django.core.management import call_command
from core.models import User, Experience, Shop


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        # Create test users
        User.objects.create_user(username='tourist_john', password='TestPass123!', is_tourist=True)
        vendor_tina_user = User.objects.create_user(username='vendor_tina', password='TestPass123!', is_vendor=True)

        # Create a shop for vendor_tina
        shop = Shop.objects.create(
            user=vendor_tina_user,
            business_name="Tina's Traditional Treats",
            description="Authentic Singaporean sweets and snacks.",
            location="123 Orchard Road, Singapore",
            contact_number="91234567",
            opening_hours="Mon-Sun: 10am - 10pm"
        )

        # Create an experience for the shop
        Experience.objects.create(
            vendor=shop,
            title="Singapore Hawker Food Tour",
            description="A guided tour of the best hawker stalls.",
            price=50.00
        )
