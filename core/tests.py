from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Vendor, Listing, Booking

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='password123')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.is_vendor)
        self.assertFalse(user.is_tourist)

class VendorModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='vendoruser', password='password123', is_vendor=True)

    def test_create_vendor_profile(self):
        vendor = Vendor.objects.create(
            user=self.user,
            business_name='Test Cafe',
            description='A great place.',
            location='Downtown',
            contact_number='1234567890'
        )
        self.assertEqual(vendor.business_name, 'Test Cafe')
        self.assertEqual(vendor.user, self.user)

class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_status(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_login_page_status(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_register_page_status(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

