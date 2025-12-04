from playwright.sync_api import Page, expect

def test_tourist_booking_form(page: Page):
    page.goto("http://localhost:8000/login/")
    page.fill("input[name='username']", "tourist_john")
    page.fill("input[name='password']", "TestPass123!")
    page.click("button[type='submit']")
    expect(page).to_have_url("http://localhost:8000/profile/")

    # Find the first experience and click on it
    page.goto("http://localhost:8000/explore/")
    page.click("a[href='#experiences']")
    page.click("#experiences a.listing-card")

    # Attempt to make a booking
    page.fill("input[name='date']", "2025-12-25")
    page.fill("input[name='time']", "12:00")
    page.click("button:has-text('Proceed to Payment')")

    expect(page).to_have_url("http://localhost:8000/experiences/1/payment/")


from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    test_tourist_booking_form(page)
    browser.close()
