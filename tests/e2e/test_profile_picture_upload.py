"""
End-to-end test for the profile picture upload functionality.

This test simulates a user logging in, navigating to the profile edit page,
uploading a new profile picture, and verifying that the new picture is
displayed on their profile.
"""
import pytest
from playwright.sync_api import Page, expect
from django.urls import reverse

@pytest.mark.django_db
def test_profile_picture_upload(page: Page, live_server):
    """
    Tests the full user flow of uploading a profile picture.

    Args:
        page (Page): The Playwright page object.
        live_server: The pytest-django fixture providing a running server.
    """
    # 1. Log in as a test tourist user.
    # We use Django's `reverse` to get the URL by its name, which is more robust than hardcoding.
    page.goto(f"{live_server.url}{reverse('login')}")
    page.fill("input[name='username']", "tourist_john")
    page.fill("input[name='password']", "TestPass123!")
    page.click("button[type='submit']")
    page.wait_for_url(f"{live_server.url}{reverse('profile')}", timeout=60000)

    # 2. Navigate to the separate profile edit page.
    page.click("a[href*='profile/edit']")
    page.wait_for_url(f"{live_server.url}{reverse('profile_edit')}")

    # 3. Upload a test image file.
    # `set_input_files` simulates a user selecting a file from their local machine.
    # The test asset 'default.png' is located in the `tests/assets` directory.
    page.set_input_files("input#id_image", "tests/assets/default.png")

    # 4. Submit the form and wait for the redirect back to the profile page.
    page.click("button:has-text('Save Changes')")
    page.wait_for_url(f"{live_server.url}{reverse('profile')}", timeout=60000)

    # 5. Take a screenshot for manual verification if needed.
    page.screenshot(path="verification/profile_picture_after_upload.png")

    # --- Assertions ---

    # 6. Verify that the user is back on the main profile page.
    expect(page).to_have_url(f"{live_server.url}{reverse('profile')}")

    # 7. Verify that an image is now visible on the page with a `src` attribute
    #    pointing to the 'user_avatars' media directory.
    profile_picture = page.locator("img[src*='user_avatars']")
    expect(profile_picture).to_be_visible()
