import pytest
from playwright.sync_api import Page, expect

def test_profile_picture_upload(page: Page):
    page.goto("http://127.0.0.1:8000/login/")
    page.fill("input[name='username']", "tourist")
    page.fill("input[name='password']", "password")
    page.click("button[type='submit']")
    page.wait_for_url("http://127.0.0.1:8000/profile/")

    page.set_input_files("input[type='file']", "tests/assets/default.png")
    page.click("button[name='update_picture']")
    page.wait_for_load_state("networkidle")

    # Take a screenshot for verification
    page.screenshot(path="verification/profile_picture_after_upload.png")

    # Assert that the user is still on the profile page
    expect(page).to_have_url("http://127.0.0.1:8000/profile/")

    # Assert that the new profile picture is visible
    profile_picture = page.locator("img[alt='Profile Picture']")
    expect(profile_picture).to_be_visible()
