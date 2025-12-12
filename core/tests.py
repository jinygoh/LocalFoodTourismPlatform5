"""
This file (`core/tests.py`) contains the unit tests for the `core` application.

Unit tests are designed to test individual components (or "units") of the application
in isolation. This includes testing models to ensure they store data correctly and
testing views to ensure they respond to requests as expected.

NOTE: The primary testing strategy for this project has shifted towards end-to-end
tests located in the `tests/e2e/` directory. This file may contain older or less
comprehensive tests.
"""
from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Shop, Dish, Experience, Booking

class UserModelTest(TestCase):
    """Tests for the custom User model."""
    def test_create_user(self):
        """Ensures a new user can be created with default roles."""
        user = User.objects.create_user(username='testuser', password='password123')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('password123'))
        # By default, new users should not be vendors or tourists.
        self.assertFalse(user.is_vendor)
        self.assertFalse(user.is_tourist)

class ShopModelTest(TestCase):
    """Tests for the Shop model."""
    def setUp(self):
        """Set up a vendor user to be the owner of the shop."""
        self.user = User.objects.create_user(username='vendoruser', password='password123', is_vendor=True)

    def test_create_shop_profile(self):
        """Ensures a Shop can be created and linked to a vendor user."""
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
    """Tests for the Dish model."""
    def test_create_dish(self):
        """Ensures a basic Dish object can be created."""
        dish = Dish.objects.create(name='Test Dish', description='A delicious dish.')
        self.assertEqual(dish.name, 'Test Dish')

class ViewTest(TestCase):
    """
    Tests for the application's views.
    These tests use Django's test client to make HTTP requests to the views
    and check the responses.
    """
    def setUp(self):
        """Set up the test client for all view tests."""
        self.client = Client()

    def test_home_page_status(self):
        """Tests that the home page loads correctly."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200) # Asserts a successful response
        self.assertTemplateUsed(response, 'home.html') # Asserts the correct template is used

    def test_login_page_status(self):
        """Tests that the login page loads correctly."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_register_page_status(self):
        """Tests that the registration page loads correctly."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_explore_page_status(self):
        """Tests that the explore page loads correctly."""
        response = self.client.get(reverse('explore'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/explore.html')
