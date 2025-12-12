"""
End-to-end test for vendor login redirection.

This test verifies that a user identified as a 'vendor' is correctly
redirected to their vendor dashboard after a successful login, rather than
the default user profile page.
"""
import pytest
from playwright.sync_api import Page, expect
from django.urls import reverse

@pytest.mark.django_db
def test_vendor_login_redirect(page: Page, live_server):
    """
    Tests the login flow for a vendor user and verifies the redirect.

    Args:
        page (Page): The Playwright page object.
        live_server: The pytest-django fixture providing a running server.
    """
    # 1. Navigate to the login page.
    page.goto(f"{live_server.url}{reverse('login')}")

    # 2. Fill in the credentials for a predefined vendor user.
    #    The 'vendor_tina' user is created by the `create_test_users.py` script.
    page.fill("input[name='username']", "vendor_tina")
    page.fill("input[name='password']", "TestPass123!")

    # 3. Submit the login form.
    page.click("button[type='submit']")

    # 4. Wait for the page to navigate and assert the final URL.
    #    The user should be redirected to the vendor dashboard.
    page.wait_for_url(f"{live_server.url}{reverse('vendor_dashboard')}", timeout=60000)
    expect(page).to_have_url(f"{live_server.url}{reverse('vendor_dashboard')}")
