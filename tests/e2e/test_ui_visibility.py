import pytest
from playwright.sync_api import Page, expect

def test_vendor_ui_is_hidden(page: Page):
    page.goto("http://127.0.0.1:8000/login/")
    page.fill("input[name='username']", "vendor_tina")
    page.fill("input[name='password']", "TestPass123!")
    page.click("button[type='submit']")
    page.wait_for_url("http://127.0.0.1:8000/vendor/")
    page.goto("http://127.0.0.1:8000/experiences/1/")

    # Assert that the review form is not visible
    review_form = page.locator("form[method='post']", has_text="Submit Review")
    expect(review_form).not_to_be_visible()

    # Assert that the booking form is not visible
    booking_form = page.locator("form[method='post']", has_text="Proceed to Payment")
    expect(booking_form).not_to_be_visible()

    # Assert that the "Only tourists can book experiences." message is visible
    tourist_only_message = page.locator("p", has_text="Only tourists can book experiences.")
    expect(tourist_only_message).to_be_visible()

def test_tourist_ui_is_visible(page: Page):
    page.goto("http://127.0.0.1:8000/login/")
    page.fill("input[name='username']", "tourist_john")
    page.fill("input[name='password']", "TestPass123!")
    page.click("button[type='submit']")
    page.wait_for_url("http://127.0.0.1:8000/profile/")
    page.goto("http://127.0.0.1:8000/experiences/1/")

    # Assert that the review form is visible
    review_form = page.locator("form[method='post']", has_text="Submit Review")
    expect(review_form).to_be_visible()

    # Assert that the booking form is visible
    booking_form = page.locator("form[method='post']", has_text="Proceed to Payment")
    expect(booking_form).to_be_visible()
