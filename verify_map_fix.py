
import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            # Login
            await page.goto("http://127.0.0.1:8000/login/")
            await page.fill('input[name="username"]', "tourist_john")
            await page.fill('input[name="password"]', "TestPass123!")
            await page.click('button[type="submit"]')
            await page.wait_for_url("http://127.0.0.1:8000/profile/")

            # Navigate to the first shop's detail page
            await page.goto("http://127.0.0.1:8000/shops/1/")
            await page.wait_for_selector("h1")

            # Find the map element and scroll to it
            map_element = await page.query_selector("div.h-\\[300px\\]")
            if map_element:
                await map_element.scroll_into_view_if_needed()
                await page.wait_for_timeout(1000) # Wait for map to load
            else:
                print("Map element not found.")


            # Ensure the verification directory exists
            os.makedirs("/home/jules/verification", exist_ok=True)

            # Take screenshot
            await page.screenshot(path="/home/jules/verification/map-fix.png")
            print("Screenshot saved to /home/jules/verification/map-fix.png")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
