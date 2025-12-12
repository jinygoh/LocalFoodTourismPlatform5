"""
This is a standalone Playwright script for frontend verification.

Its purpose is to automate the process of logging in as a tourist and taking a
screenshot of the main profile page. This is a simple but effective way to
visually verify that the profile page is rendering correctly after changes
have been made.

The script uses Playwright's sync API.
"""
from playwright.sync_api import sync_playwright
import os

def run():
    """
    Main function to launch the browser, perform the actions, and take a screenshot.
    """
    # The `with` statement ensures that the Playwright resources are properly cleaned up.
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # --- 1. Login ---
        # Navigate to the login page and fill in the credentials for a test tourist user.
        page.goto("http://127.0.0.1:8000/login/")
        page.fill("input[name='username']", "tourist_john")
        page.fill("input[name='password']", "TestPass123!")

        # --- 2. Submit and Wait for Navigation ---
        page.click("button[type='submit']")
        # Wait for the page to redirect and fully load the profile page.
        page.wait_for_url("http://127.0.0.1:8000/profile/")

        # --- 3. Take Screenshot ---
        # Ensure the directory for saving the screenshot exists.
        os.makedirs("verification", exist_ok=True)
        screenshot_path = "verification/profile-page.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot of profile page saved to: {screenshot_path}")

        # Close the browser session.
        browser.close()

# --- Script Execution ---
if __name__ == "__main__":
    run()
