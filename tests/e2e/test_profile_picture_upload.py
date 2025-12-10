import pytest
from playwright.sync_api import Page, expect
from django.urls import reverse

@pytest.mark.django_db
def test_profile_picture_upload(page: Page, live_server):
    page.goto(f"{live_server.url}{reverse('login')}")
    page.fill("input[name='username']", "tourist_john")
    page.fill("input[name='password']", "TestPass123!")
    page.click("button[type='submit']")
    page.wait_for_url(f"{live_server.url}{reverse('profile')}", timeout=60000)

    # The profile edit form is on a separate page
    page.click("a[href*='profile/edit']")
    page.wait_for_url(f"{live_server.url}{reverse('profile_edit')}")

    page.set_input_files("input#id_image", "tests/assets/default.png")
    page.click("button:has-text('Save Changes')")
    page.wait_for_url(f"{live_server.url}{reverse('profile')}", timeout=60000)

    # Take a screenshot for verification
    page.screenshot(path="verification/profile_picture_after_upload.png")

    # Assert that the user is still on the profile page
    expect(page).to_have_url(f"{live_server.url}{reverse('profile')}")

    # Assert that the new profile picture is visible
    profile_picture = page.locator("img[src*='user_avatars']")
    expect(profile_picture).to_be_visible()
