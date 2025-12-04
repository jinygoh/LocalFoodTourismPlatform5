from playwright.sync_api import Page, expect

def test_new_vendor_dashboard(page: Page):
    page.goto("http://localhost:8000/login/")
    page.fill("input[name='username']", "test_vendor_2")
    page.fill("input[name='password']", "password123")
    page.click("button[type='submit']")
    expect(page).to_have_url("http://localhost:8000/vendor/dashboard/")
    expect(page.locator("h1:has-text('Welcome')")).to_be_visible()

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    test_new_vendor_dashboard(page)
    browser.close()
