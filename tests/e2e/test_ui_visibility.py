"""
End-to-end tests for UI visibility based on user roles.

These tests verify that certain UI elements, like booking and review forms,
are correctly shown or hidden depending on whether the logged-in user is a
'tourist' or a 'vendor'.
"""
import pytest
from playwright.sync_api import Page, expect
from core.models import Experience


@pytest.mark.django_db
def test_vendor_ui_is_hidden(page: Page, live_server):
    """
    Tests that a logged-in vendor does NOT see the booking and review forms
    on an experience detail page.
    """
    # Get a specific experience from the test database.
    experience = Experience.objects.get(title="Singapore Hawker Food Tour")

    # --- Login as Vendor ---
    page.goto(f"{live_server.url}/login/")
    page.fill("input[name='username']", "vendor_tina")
    page.fill("input[name='password']", "TestPass123!")
    page.click("button[type='submit']")
    page.wait_for_url(f"{live_server.url}/vendor/dashboard/") # Wait for vendor dashboard redirect

    # --- Navigate to Experience Page ---
    page.goto(f"{live_server.url}/experiences/{experience.pk}/")

    # --- Assertions ---
    # Verify that placeholder messages are shown instead of the forms.
    review_form_message = page.locator("p", has_text="Only tourists can write a review.")
    expect(review_form_message).to_be_visible()

    booking_form_message = page.locator("p", has_text="Only tourists can book experiences.")
    expect(booking_form_message).to_be_visible()

@pytest.mark.django_db
def test_tourist_ui_is_visible(page: Page, live_server):
    """
    Tests that a logged-in tourist DOES see the booking and review forms
    on an experience detail page.
    """
    # Get a specific experience from the test database.
    experience = Experience.objects.get(title="Singapore Hawker Food Tour")

    # --- Login as Tourist ---
    page.goto(f"{live_server.url}/login/")
    page.fill("input[name='username']", "tourist_john")
    page.fill("input[name='password']", "TestPass123!")
    page.click("button[type='submit']")
    page.wait_for_url(f"{live_server.url}/profile/") # Wait for profile redirect

    # --- Navigate to Experience Page ---
    page.goto(f"{live_server.url}/experiences/{experience.pk}/")

    # --- Assertions ---
    # Verify that the actual forms are visible.
    review_form = page.locator("form", has_text="Submit Review")
    expect(review_form).to_be_visible()

    booking_form = page.locator("form", has_text="Proceed to Payment")
    expect(booking_form).to_be_visible()
