import pytest
from playwright.sync_api import Page, expect
from core.models import Experience


@pytest.mark.django_db
def test_vendor_ui_is_hidden(page: Page):
    experience = Experience.objects.get(title="Singapore Hawker Food Tour")
    page.goto("http://127.0.0.1:8000/login/")
    page.fill("input[name='username']", "vendor_tina")
    page.fill("input[name='password']", "TestPass123!")
    page.click("button[type='submit']")
    page.wait_for_url("http://127.0.0.1:8000/shop/")
    page.goto(f"http://127.0.0.1:8000/experiences/{experience.pk}/")

    # Assert that the review form shows the correct message
    review_form_message = page.locator("p", has_text="Only tourists can write a review.")
    expect(review_form_message).to_be_visible()

    # Assert that the booking form shows the correct message
    booking_form_message = page.locator("p", has_text="Only tourists can book experiences.")
    expect(booking_form_message).to_be_visible()

@pytest.mark.django_db
def test_tourist_ui_is_visible(page: Page):
    experience = Experience.objects.get(title="Singapore Hawker Food Tour")
    page.goto("http://127.0.0.1:8000/login/")
    page.fill("input[name='username']", "tourist_john")
    page.fill("input[name='password']", "TestPass123!")
    page.click("button[type='submit']")
    page.wait_for_url("http://127.0.0.1:8000/profile/")
    page.goto(f"http://127.0.0.1:8000/experiences/{experience.pk}/")

    # Assert that the review form is visible
    review_form = page.locator("form", has_text="Submit Review")
    expect(review_form).to_be_visible()

    # Assert that the booking form is visible
    booking_form = page.locator("form", has_text="Proceed to Payment")
    expect(booking_form).to_be_visible()
