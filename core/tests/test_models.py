from django.test import TestCase
from ..models import User, Shop, Dish

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='password123')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.is_vendor)
        self.assertFalse(user.is_tourist)

class ShopModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='vendoruser', password='password123', is_vendor=True)

    def test_create_shop_profile(self):
        shop = Shop.objects.create(
            user=self.user,
            business_name='Test Cafe',
            description='A great place.',
            location='Downtown',
            contact_number='1234567890'
        )
        self.assertEqual(shop.business_name, 'Test Cafe')
        self.assertEqual(shop.user, self.user)

class DishModelTest(TestCase):
    def test_create_dish(self):
        dish = Dish.objects.create(name='Test Dish', description='A delicious dish.')
        self.assertEqual(dish.name, 'Test Dish')
