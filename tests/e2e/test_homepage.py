"""
End-to-end test for the homepage.

This test uses Playwright to visit the homepage and verify that key
elements of the navigation and branding are visible to an anonymous user.
"""
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.django_db
def test_homepage_elements_are_visible(page: Page, live_server):
    """
    Tests that essential navigation links and the site title are visible on the homepage.

    Args:
        page (Page): The Playwright page object.
        live_server: The pytest-django fixture that provides a running Django server.
    """
    # Navigate to the homepage using the live server's URL.
    page.goto(live_server.url)

    # --- Assertions ---
    # Use Playwright's `expect` to verify the visibility of key elements.

    # Check for the site title/brand name.
    expect(page.get_by_text("TasteLocal")).to_be_visible()

    # Check for the main navigation links.
    expect(page.get_by_role("link", name="Explore")).to_be_visible()
    expect(page.get_by_role("link", name="Login")).to_be_visible()
    expect(page.get_by_role("link", name="Register")).to_be_visible()
