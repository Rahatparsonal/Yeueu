# requirements: playwright
# install: pip install playwright && playwright install

import asyncio
from playwright.async_api import async_playwright
import json

# === CONFIGURATION ===
TARGET_URL = "http://94.23.120.156/ints/client/dashboard.php"  # Replace with your dashboard or landing page
SESSION_COOKIE_NAME = "PHPSESSID"
SESSION_COOKIE_VALUE = "your_session_id_here"  # Replace with your real session cookie
OUTPUT_FILE = "captured_apis.json"

# === SCRIPT START ===
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        # Set session cookie
        await context.add_cookies([{
            'name': SESSION_COOKIE_NAME,
            'value': SESSION_COOKIE_VALUE,
            'url': 'http://94.23.120.156',
            'path': '/',
            'httpOnly': True
        }])

        page = await context.new_page()
        captured_requests = []

        async def log_request(request):
            if request.resource_type in ["xhr", "fetch"]:
                captured_requests.append({
                    "method": request.method,
                    "url": request.url,
                    "headers": dict(request.headers),
                    "post_data": request.post_data or ""
                })
                print(f"[API] {request.method} {request.url}")

        page.on("request", log_request)

        print("🔄 Loading target page...")
        await page.goto(TARGET_URL)
        await page.wait_for_timeout(15000)  # wait 15 seconds for all API calls

        print(f"✅ Captured {len(captured_requests)} API request(s). Saving to {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "w") as f:
            json.dump(captured_requests, f, indent=2)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
