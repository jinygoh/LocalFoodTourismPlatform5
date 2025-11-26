import pytest
from playwright.sync_api import Page, expect

def test_vendor_login_redirect(page: Page):
    page.goto("http://127.0.0.1:8000/login/")
    page.fill("input[name='username']", "vendor_tina")
    page.fill("input[name='password']", "TestPass123!")
    page.click("button[type='submit']")
    page.wait_for_url("http://127.0.0.1:8000/vendor/")
    expect(page).to_have_url("http://127.0.0.1:8000/vendor/")
