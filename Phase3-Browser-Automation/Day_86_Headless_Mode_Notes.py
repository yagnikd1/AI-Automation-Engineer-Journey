"""
DAY 86 — PLAYWRIGHT HEADLESS MODE
Phase 3 — Browser Automation
STATUS: COMPLETED AND PRACTICALLY VERIFIED

Covered:
- Headed vs headless execution
- headless=True
- Why headless execution is useful on servers
- Viewport configuration

Verified:
Headless browser: True
Viewport: 1280 x 720
Page title: Example Domain
Heading: Example Domain
Browser closed: True
"""

import asyncio
from playwright.async_api import async_playwright


async def verify_headless_mode():
    print("=== DAY 86 FINAL VERIFICATION ===")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        print("Headless browser:", True)

        page = await browser.new_page(
            viewport={"width": 1280, "height": 720}
        )

        viewport = await page.evaluate(
            "() => ({ width: window.innerWidth, height: window.innerHeight })"
        )

        print("Viewport width:", viewport["width"])
        print("Viewport height:", viewport["height"])

        await page.goto("https://example.com")

        print("Page title:", await page.title())
        print("Heading:", await page.locator("h1").text_content())

        await browser.close()
        print("Browser closed:", True)


asyncio.run(verify_headless_mode())
