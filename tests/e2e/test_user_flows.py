from playwright.sync_api import Page, expect
from django.urls import reverse
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture(scope="function", autouse=True)
def setup_users(django_db_setup, django_user_model):
    """Create test users for E2E tests."""
    try:
        django_user_model.objects.create_user(
            username="tourist_e2e", password="password123", email="tourist_e2e@example.com", is_tourist=True
        )
    except Exception:
        # User might already exist, ignore
        pass
    try:
        django_user_model.objects.create_user(
            username="vendor_e2e", password="password123", email="vendor_e2e@example.com", is_vendor=True
        )
    except Exception:
        # User might already exist, ignore
        pass

@pytest.mark.django_db
def test_tourist_registration_and_login_flow(page: Page, live_server):
    """
    Tests the full registration and login flow for a tourist user.
    """
    # Registration
    page.goto(f"{live_server.url}{reverse('register')}")
    page.get_by_label("Username").fill("new_tourist")
    page.get_by_label("Email").fill("new_tourist@example.com")
    page.locator('input[name="password"]').fill("password123")
    page.get_by_label("Tourist").check()
    page.get_by_role("button", name="Register").click()

    # Should be redirected to login page
    expect(page).to_have_url(f"{live_server.url}{reverse('login')}")

    # Login
    page.get_by_label("Username").fill("new_tourist")
    page.get_by_label("Password").fill("password123")
    page.get_by_role("button", name="Login").click()

    # Should be redirected to profile page after login
    expect(page).to_have_url(f"{live_server.url}{reverse('profile')}")
    expect(page.get_by_text("Welcome, new_tourist")).to_be_visible()

@pytest.mark.django_db
def test_vendor_login_and_dashboard_flow(page: Page, live_server):
    """
    Tests that a vendor is correctly redirected to their dashboard upon login.
    """
    page.goto(f"{live_server.url}{reverse('login')}")
    page.get_by_label("Username").fill("vendor_e2e")
    page.get_by_label("Password").fill("password123")
    page.get_by_role("button", name="Login").click()

    # Vendor should be redirected to the vendor dashboard
    expect(page).to_have_url(f"{live_server.url}{reverse('vendor_dashboard')}")
    expect(page.get_by_text("Vendor Dashboard")).to_be_visible()

@pytest.mark.django_db
def test_explore_page_search_and_filter(page: Page, live_server):
    """
    Tests the search and filter functionality on the explore page.
    This is a basic test to ensure the form submission works.
    """
    page.goto(f"{live_server.url}{reverse('explore')}")

    # Fill in a search query
    page.get_by_placeholder("Search by keyword").fill("Test Food")
    page.get_by_role("button", name="Search").click()

    # Check that the URL contains the search query
    expect(page).to_have_url(f"{live_server.url}{reverse('explore')}?q=Test+Food&active_tab=dishes")
