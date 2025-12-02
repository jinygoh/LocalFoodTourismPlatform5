import pytest
from playwright.sync_api import Page, expect

def test_homepage_elements_are_visible(page: Page):
    page.goto("http://127.0.0.1:8000/")

    # Assert that the "Discover Culinary Spots Nearby" section is visible
    discover_spots = page.locator("h2", has_text="Discover Culinary Spots Nearby")
    expect(discover_spots).to_be_visible()

    # Assert that the map is visible
    map_element = page.locator("#map")
    expect(map_element).to_be_visible()
