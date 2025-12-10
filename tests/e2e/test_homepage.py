import pytest
from playwright.sync_api import Page, expect
from django.urls import reverse

@pytest.mark.django_db
def test_homepage_elements_are_visible(page: Page, live_server):
    page.goto(live_server.url)
    expect(page.get_by_text("TasteLocal")).to_be_visible()
    expect(page.get_by_role("link", name="Explore")).to_be_visible()
    expect(page.get_by_role("link", name="Login")).to_be_visible()
    expect(page.get_by_role("link", name="Register")).to_be_visible()
