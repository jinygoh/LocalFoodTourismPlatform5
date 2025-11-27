import pytest
from playwright.sync_api import Page, expect

def test_homepage_elements_are_visible(page: Page):
    page.goto("http://127.0.0.1:8000/")

    # Assert that the "Browse by Experience" section is visible
    browse_by_experience = page.locator("h2", has_text="Explore by Experience")
    expect(browse_by_experience).to_be_visible()

    # Assert that the "Browse More" button is visible
    browse_more_button = page.locator("a", has_text="Browse More")
    expect(browse_more_button).to_be_visible()

    # Assert that the map is visible
    map_element = page.locator("#map")
    expect(map_element).to_be_visible()
