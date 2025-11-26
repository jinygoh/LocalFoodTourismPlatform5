import pytest
from playwright.sync_api import Page, expect

def test_registration_form_labels(page: Page):
    page.goto("http://127.0.0.1:8000/register/")

    # Assert that the correct labels are visible
    expect(page.locator("label[for='id_username']")).to_have_text("Username:")
    expect(page.locator("label[for='id_password1']")).to_have_text("Password:")
    expect(page.locator("label[for='id_password2']")).to_have_text("Password confirmation:")
    expect(page.locator("label[for='id_is_tourist']")).to_have_text("Is tourist:")
    expect(page.locator("label[for='id_is_vendor']")).to_have_text("Is vendor:")
