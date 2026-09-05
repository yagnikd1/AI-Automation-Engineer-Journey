"""
DAY 87 — PLAYWRIGHT SESSIONS & LOGIN STATE
Phase 3 — Browser Automation | Week 12 — Advanced Playwright

Complete notes + runnable reference.

Verified practical revision:
Login: PASS
Cookies: 1
Auth state saved: auth_state.json
Authentication reuse: PASS
Products found: 6
Final verification: PASS

Covered:
1. Browser contexts
2. Cookies
3. Local storage
4. Session storage
5. storage_state
6. Saving authenticated state
7. Restoring authenticated state
8. Protecting credentials/session files
"""

import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright

BASE_URL = "https://www.saucedemo.com/"
PRODUCTS_URL = "https://www.saucedemo.com/inventory.html"

# SauceDemo practice credentials. For real systems, use environment variables.
USERNAME = os.getenv("SWAG_USERNAME", "standard_user")
PASSWORD = os.getenv("SWAG_PASSWORD", "secret_sauce")

AUTH_STATE_FILE = Path("auth_state.json")
REPORT_FILE = Path("day_87_product_report.json")


async def login(page):
    """Perform an authorized login and verify the authenticated URL."""
    await page.goto(BASE_URL)
    await page.locator("#user-name").fill(USERNAME)
    await page.locator("#password").fill(PASSWORD)
    await page.locator("#login-button").click()
    await page.wait_for_url("**/inventory.html")
    return page


async def extract_products(page):
    """Extract product cards using Playwright locators."""
    products = []
    cards = page.locator(".inventory_item")
    count = await cards.count()

    for index in range(count):
        card = cards.nth(index)

        name = await card.locator(".inventory_item_name").text_content()
        description = await card.locator(".inventory_item_desc").text_content()
        price = await card.locator(".inventory_item_price").text_content()
        button = card.locator("button")
        button_text = await button.text_content()
        button_id = await button.get_attribute("id")

        products.append({
            "name": name.strip() if name else "",
            "description": description.strip() if description else "",
            "price": price.strip() if price else "",
            "button_text": button_text.strip() if button_text else "",
            "button_id": button_id or "",
        })

    return products


def analyze_products(products):
    """Apply Python fundamentals to extracted browser data."""
    prices = []
    available = []

    for product in products:
        if product["button_text"].lower() == "add to cart":
            available.append(product["name"])

        try:
            prices.append(float(product["price"].replace("$", "")))
        except ValueError:
            pass

    if prices:
        lowest = min(prices)
        highest = max(prices)
        average = round(sum(prices) / len(prices), 2)
    else:
        lowest = highest = average = 0

    return {
        "total_products": len(products),
        "available_products": len(available),
        "available_product_names": available,
        "lowest_price": lowest,
        "highest_price": highest,
        "average_price": average,
    }


async def inspect_cookies(context):
    """Read non-secret cookie metadata from the context."""
    cookies = await context.cookies()

    return [
        {
            "name": cookie["name"],
            "domain": cookie["domain"],
            "path": cookie["path"],
        }
        for cookie in cookies
    ]


async def inspect_storage(page):
    """Inspect localStorage and sessionStorage through page.evaluate()."""
    local_storage = await page.evaluate(
        "() => Object.fromEntries(Object.entries(localStorage))"
    )

    session_storage = await page.evaluate(
        "() => Object.fromEntries(Object.entries(sessionStorage))"
    )

    return {
        "local_storage": local_storage,
        "session_storage": session_storage,
    }


async def main():
    async with async_playwright() as p:
        # Day 86 concept reused: headless Chromium.
        browser = await p.chromium.launch(headless=True)

        # First isolated browser session.
        login_context = await browser.new_context(
            viewport={"width": 1280, "height": 720}
        )
        login_page = await login_context.new_page()

        try:
            # 1. Login
            await login(login_page)
            assert await login_page.locator(".title").text_content() == "Products"
            print("Login: PASS")

            # 2. Extract and process browser-rendered data
            products = await extract_products(login_page)
            print("Products found:", len(products))
            analysis = analyze_products(products)

            # 3. Inspect cookies
            cookies = await inspect_cookies(login_context)
            print("Cookies:", len(cookies))

            # 4. Inspect browser storage
            storage = await inspect_storage(login_page)

            # 5. Save authenticated context state
            await login_context.storage_state(path=AUTH_STATE_FILE)
            print("Auth state saved:", AUTH_STATE_FILE)

            # 6. Destroy original session
            await login_context.close()

            # 7. Create a completely new context from saved state
            restored_context = await browser.new_context(
                storage_state=AUTH_STATE_FILE,
                viewport={"width": 1280, "height": 720},
            )
            restored_page = await restored_context.new_page()

            # 8. Verify that authentication was reused
            await restored_page.goto(PRODUCTS_URL)
            await restored_page.wait_for_load_state("domcontentloaded")

            heading = await restored_page.locator(".title").text_content()
            authentication_reused = heading.strip() == "Products"

            print(
                "Authentication reuse:",
                "PASS" if authentication_reused else "FAIL",
            )
            assert authentication_reused

            # 9. Save a learning report
            report = {
                "day": 87,
                "program": "Authenticated Product Monitor",
                "headless": True,
                "login_successful": True,
                "products": products,
                "analysis": analysis,
                "cookies": cookies,
                "storage": storage,
                "auth_state_saved": AUTH_STATE_FILE.exists(),
                "authentication_reused": authentication_reused,
            }

            with REPORT_FILE.open("w", encoding="utf-8") as file:
                json.dump(report, file, indent=4)

            print("Final verification: PASS")

            await restored_context.close()

        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())


# ============================================================
# DAY 87 SYNTAX REFERENCE
# ============================================================
#
# Browser context:
#     context = await browser.new_context()
#
# New page:
#     page = await context.new_page()
#
# Cookies:
#     cookies = await context.cookies()
#     await context.add_cookies([...])
#     await context.clear_cookies()
#
# localStorage:
#     await page.evaluate(
#         "() => localStorage.getItem('key')"
#     )
#
# sessionStorage:
#     await page.evaluate(
#         "() => sessionStorage.getItem('key')"
#     )
#
# Save state:
#     await context.storage_state(
#         path="auth_state.json"
#     )
#
# Restore state:
#     context = await browser.new_context(
#         storage_state="auth_state.json"
#     )
#
# SECURITY:
#     Never commit real auth_state.json files.
#
# Recommended .gitignore:
#     auth_state.json
#     *.auth.json
#     playwright/.auth/
#
# For real credentials:
#     USERNAME = os.getenv("APP_USERNAME")
#     PASSWORD = os.getenv("APP_PASSWORD")
#
# ============================================================
# MENTAL MODEL
# ============================================================
#
# Browser
#   ↓
# Context
#   ↓
# Cookies / localStorage / sessionStorage
#   ↓
# Authentication
#   ↓
# storage_state()
#   ↓
# auth_state.json
#   ↓
# new_context(storage_state="auth_state.json")
#   ↓
# Reused authenticated session
#
# ============================================================
