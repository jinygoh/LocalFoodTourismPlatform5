"""
This is a standalone Playwright script for frontend verification.

Its purpose is to automate the process of logging in, navigating to a specific
shop detail page, and taking a screenshot of the map element. This is useful for
manually or automatically verifying that a fix related to the map's display has
been successfully implemented.

The script uses Playwright's async API.
"""
import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    """
    Main asynchronous function to run the Playwright automation.
    """
    # Launch a new browser session.
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            # --- 1. Login ---
            # Navigate to the login page and fill in the credentials for a test user.
            await page.goto("http://1227.0.0.1:8000/login/")
            await page.fill('input[name="username"]', "tourist_john")
            await page.fill('input[name="password"]', "TestPass123!")
            await page.click('button[type="submit"]')
            # Wait for the successful login redirect to the profile page.
            await page.wait_for_url("http://127.0.0.1:8000/profile/")

            # --- 2. Navigate to Shop Detail Page ---
            # Go to the detail page for the shop with primary key 1.
            await page.goto("http://127.0.0.1:8000/shops/1/")
            # Wait for a key element (the main heading) to ensure the page has loaded.
            await page.wait_for_selector("h1")

            # --- 3. Find and Prepare Map for Screenshot ---
            # The selector `div.h-\[300px\]` targets the map container based on its Tailwind CSS class.
            map_element = await page.query_selector("div.h-\\[300px\\]")
            if map_element:
                # Scroll the map into view to ensure it's not off-screen.
                await map_element.scroll_into_view_if_needed()
                # Wait for a brief moment to allow map tiles to load.
                await page.wait_for_timeout(1000)
            else:
                print("Map element not found.")


            # --- 4. Take Screenshot ---
            # Ensure the directory for saving the screenshot exists.
            os.makedirs("verification", exist_ok=True)
            # Capture the screenshot.
            screenshot_path = "verification/map-fix.png"
            await page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

        except Exception as e:
            # Print any error that occurs during the automation.
            print(f"An error occurred: {e}")
        finally:
            # Ensure the browser is always closed, even if errors occur.
            await browser.close()

# --- Script Execution ---
if __name__ == "__main__":
    asyncio.run(main())
