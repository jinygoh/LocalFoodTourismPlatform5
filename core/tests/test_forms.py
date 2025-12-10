from django.test import TestCase
from ..forms import CustomUserCreationForm, ReviewForm, BookingForm
from ..models import Shop, User
import datetime

class CustomUserCreationFormTest(TestCase):

    def test_valid_tourist_form(self):
        form_data = {
            'username': 'touristuser',
            'email': 'tourist@example.com',
            'user_type': 'tourist',
            'password': 'password123'
        }
        form = CustomUserCreationForm(data=form_data)
        # Manually trigger cleaning since it's a UserCreationForm
        form.is_valid()
        form.clean()
        self.assertTrue(form.is_valid())
        self.assertTrue(form.instance.is_tourist)
        self.assertFalse(form.instance.is_vendor)

    def test_valid_vendor_form(self):
        form_data = {
            'username': 'vendoruser',
            'email': 'vendor@example.com',
            'user_type': 'vendor',
            'password': 'password123'
        }
        form = CustomUserCreationForm(data=form_data)
        form.is_valid()
        form.clean()
        self.assertTrue(form.is_valid())
        self.assertFalse(form.instance.is_tourist)
        self.assertTrue(form.instance.is_vendor)

    def test_missing_user_type(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('user_type', form.errors)

class ReviewFormTest(TestCase):

    def test_valid_review_form(self):
        form_data = {'rating': 5, 'comment': 'Excellent!'}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_rating(self):
        form_data = {'rating': 6, 'comment': 'Too high a rating'}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

class BookingFormTest(TestCase):

    def setUp(self):
        self.vendor_user = User.objects.create_user(username='testvendor', password='password123', is_vendor=True)
        self.shop = Shop.objects.create(
            user=self.vendor_user,
            business_name='Test Shop',
            opening_hours_structured=[
                {'day_of_week': 1, 'open_time': '09:00', 'close_time': '17:00'} # Monday
            ]
        )
        self.tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        # Find the next Monday to ensure the booking is valid
        while self.tomorrow.isoweekday() != 1:
            self.tomorrow += datetime.timedelta(days=1)

    def test_valid_booking_form(self):
        form_data = {
            'date': self.tomorrow,
            'time': '14:00',
            'guests': 2
        }
        form = BookingForm(data=form_data, shop=self.shop)
        self.assertTrue(form.is_valid())

    def test_booking_in_the_past(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        form_data = {
            'date': yesterday,
            'time': '14:00',
            'guests': 2
        }
        form = BookingForm(data=form_data, shop=self.shop)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn('You cannot book a date in the past.', form.errors['__all__'])

    def test_booking_outside_opening_hours(self):
        form_data = {
            'date': self.tomorrow,
            'time': '18:00', # After closing time
            'guests': 2
        }
        form = BookingForm(data=form_data, shop=self.shop)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn("You must book a time during the shop's opening hours.", form.errors['__all__'])
