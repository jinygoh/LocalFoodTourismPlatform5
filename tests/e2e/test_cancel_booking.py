"""
End-to-end test for the booking cancellation functionality.

This test uses Playwright to simulate a user logging in, navigating to their profile,
and cancelling an existing booking. It verifies that the UI updates correctly
to reflect the "cancelled" status.
"""
import pytest
from playwright.sync_api import Page, expect
from core.models import User, Experience, Booking
import datetime

@pytest.fixture(scope='function')
def create_booking(django_db_setup, django_db_blocker):
    """
    A pytest fixture that creates a specific booking for a test user.

    This fixture runs for each function that requires it (`scope='function'`).
    It ensures that a known booking exists in the database for the test to interact with.
    """
    with django_db_blocker.unblock():
        # Get the predefined test user and an experience.
        user = User.objects.get(username='tourist_john')
        experience = Experience.objects.get(title="Singapore Hawker Food Tour")

        # Create a new booking with a future date and 'confirmed' status.
        return Booking.objects.create(
            user=user,
            content_object=experience,
            date=datetime.date.today() + datetime.timedelta(days=1),
            guests=1,
            status='confirmed'
        )

@pytest.mark.django_db
def test_cancel_booking(page: Page, create_booking):
    """
    Tests the full user flow of cancelling a booking from the profile page.

    Args:
        page (Page): The Playwright page object provided by the `pytest-playwright` fixture.
        create_booking: The pytest fixture that provides the booking object to be cancelled.
    """
    # 1. Log in as the test user 'tourist_john'.
    page.goto("http://127.0.0.1:8000/login/")
    page.fill("input[name='username']", "tourist_john")
    page.fill("input[name='password']", "TestPass123!")
    page.click("button[type='submit']")
    page.wait_for_url("http://127.0.0.1:8000/profile/")

    # 2. Locate the specific booking on the profile page.
    # We use a data attribute `data-booking-id` for a robust selector.
    booking_card = page.locator(f"[data-booking-id='{create_booking.pk}']")

    # 3. Find and click the "Cancel" button within that booking's card.
    cancel_button = booking_card.locator("a", has_text="Cancel")
    expect(cancel_button).to_be_visible()
    cancel_button.click()

    # 4. Wait for the page to reload after the cancellation action.
    page.wait_for_url("http://127.0.0.1:8000/profile/")

    # 5. Assert that the booking's status text has changed to "cancelled".
    cancelled_status = booking_card.locator("span:text-is('cancelled')")
    expect(cancelled_status).to_be_visible()

    # 6. Assert that the "Cancel" button is now hidden, as the action is no longer possible.
    expect(cancel_button).not_to_be_visible()
