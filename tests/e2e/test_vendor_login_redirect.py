import pytest
from playwright.sync_api import Page, expect
from django.urls import reverse

@pytest.mark.django_db
def test_vendor_login_redirect(page: Page, live_server):
    page.goto(f"{live_server.url}{reverse('login')}")
    page.fill("input[name='username']", "vendor_tina")
    page.fill("input[name='password']", "TestPass123!")
    page.click("button[type='submit']")
    page.wait_for_url(f"{live_server.url}{reverse('vendor_dashboard')}", timeout=60000)
    expect(page).to_have_url(f"{live_server.url}{reverse('vendor_dashboard')}")
