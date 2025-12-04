
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/login/")
        page.fill("input[name='username']", "tourist_john")
        page.fill("input[name='password']", "TestPass123!")
        page.click("button[type='submit']")
        page.wait_for_url("http://127.0.0.1:8000/profile/")
        page.screenshot(path="/home/jules/verification/profile-page.png")
        browser.close()

if __name__ == "__main__":
    run()
