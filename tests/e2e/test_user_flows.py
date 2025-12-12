"""
End-to-end tests for common user authentication and navigation flows.

This file contains tests for:
- Tourist registration and login.
- Vendor login and redirection to the dashboard.
- Basic search functionality on the Explore page.
"""
from playwright.sync_api import Page, expect
from django.urls import reverse
import pytest

@pytest.fixture(scope="function", autouse=True)
def setup_users(db, django_user_model):
    """
    A pytest fixture to create necessary test users before each test function.

    `autouse=True` ensures this fixture is automatically used for every test in this file.
    It's idempotent, ignoring errors if the users already exist from a previous run.
    """
    try:
        django_user_model.objects.create_user(
            username="vendor_e2e", password="password123", email="vendor_e2e@example.com", is_vendor=True
        )
    except Exception:
        # Ignore errors if the user already exists.
        pass

@pytest.mark.django_db
def test_tourist_registration_and_login_flow(page: Page, live_server):
    """
    Tests the full registration and login flow for a new tourist user.
    """
    # --- Registration Step ---
    page.goto(f"{live_server.url}{reverse('register')}")
    page.get_by_label("Username").fill("new_tourist")
    page.get_by_label("Email").fill("new_tourist@example.com")
    # Note: Passwords are not handled by `get_by_label` as their id/name can be complex.
    page.locator('input[name="password"]').fill("password123")
    page.get_by_label("Tourist").check() # Select the 'Tourist' user type.
    page.get_by_role("button", name="Register").click()

    # After registration, the user should be on the login page.
    expect(page).to_have_url(f"{live_server.url}{reverse('login')}")

    # --- Login Step ---
    page.get_by_label("Username").fill("new_tourist")
    page.get_by_label("Password").fill("password123")
    page.get_by_role("button", name="Login").click()

    # After login, a tourist should be redirected to their profile page.
    expect(page).to_have_url(f"{live_server.url}{reverse('profile')}")
    # Verify a welcome message is visible.
    expect(page.get_by_text("Welcome, new_tourist")).to_be_visible()

@pytest.mark.django_db
def test_vendor_login_and_dashboard_flow(page: Page, live_server):
    """
    Tests that a vendor user is correctly redirected to their dashboard upon login.
    """
    # --- Login Step ---
    page.goto(f"{live_server.url}{reverse('login')}")
    page.get_by_label("Username").fill("vendor_e2e")
    page.get_by_label("Password").fill("password123")
    page.get_by_role("button", name="Login").click()

    # --- Assertions ---
    # A vendor should be redirected to the vendor dashboard, not the regular profile.
    expect(page).to_have_url(f"{live_server.url}{reverse('vendor_dashboard')}")
    expect(page.get_by_text("Vendor Dashboard")).to_be_visible()

@pytest.mark.django_db
def test_explore_page_search_and_filter(page: Page, live_server):
    """
    Tests the basic search functionality on the Explore page.
    This test confirms that submitting the search form correctly updates the URL.
    """
    page.goto(f"{live_server.url}{reverse('explore')}")

    # --- Action ---
    # Fill in the search input and click the search button.
    page.get_by_placeholder("Search by keyword").fill("Test Food")
    page.get_by_role("button", name="Search").click()

    # --- Assertion ---
    # Verify that the page URL is updated with the correct query parameters.
    # This confirms the form submission is working as expected.
    expect(page).to_have_url(f"{live_server.url}{reverse('explore')}?q=Test+Food&active_tab=dishes")
