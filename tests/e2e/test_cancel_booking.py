import pytest
from playwright.sync_api import Page, expect
from django.core.management import call_command
from core.models import User, Experience, Booking
import datetime

@pytest.fixture(scope='function')
def create_booking():
    user = User.objects.get(username='tourist_john')
    experience = Experience.objects.get(title="Singapore Hawker Food Tour")
    return Booking.objects.create(
        user=user,
        content_object=experience,
        date=datetime.date.today() + datetime.timedelta(days=1),
        guests=1,
        status='confirmed'
    )

@pytest.mark.django_db
def test_cancel_booking(page: Page, create_booking):
    page.goto("http://127.0.0.1:8000/login/")
    page.fill("input[name='username']", "tourist_john")
    page.fill("input[name='password']", "TestPass123!")
    page.click("button[type='submit']")
    page.wait_for_url("http://127.0.0.1:8000/profile/")

    # Find the booking card
    booking_card = page.locator(f"[data-booking-id='{create_booking.pk}']")

    # Find and click the "Cancel" button within the card
    cancel_button = booking_card.locator("a", has_text="Cancel")
    expect(cancel_button).to_be_visible()
    cancel_button.click()

    # Wait for the page to reload or update
    page.wait_for_url("http://127.0.0.1:8000/profile/")

    # Assert that the booking status is now "cancelled"
    cancelled_status = booking_card.locator("span:text-is('cancelled')")
    expect(cancelled_status).to_be_visible()

    # Assert that the "Cancel" button is no longer visible
    expect(cancel_button).not_to_be_visible()
