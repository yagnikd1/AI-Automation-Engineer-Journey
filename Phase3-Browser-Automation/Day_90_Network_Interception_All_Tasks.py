"""
DAY 90 — NETWORK INTERCEPTION
Phase 3 — Browser Automation

Program:
Authorised Product Network Monitor

This file contains:
1. Combined Python + Web Scraping guided revision program
2. Task 1 — Python fundamentals
3. Task 2 — Function and price cleaning
4. Task 3 — Requests and HTTP
5. Task 4 — BeautifulSoup
6. Task 5 — Error handling
7. Task 6 — Playwright browser + locators
8. Task 7 — Day 89 network inspection bridge
9. Day 90 — JSON response capture
10. Day 90 — Request routing
11. Day 90 — Blocking resources
12. Day 90 — Authorised request modification
13. Day 90 — API data vs rendered HTML
14. Day 90 — Network-error handling
15. Final integrated Day 90 program

NOTE:
The revision URL intentionally uses example.com/products, which returns
404. That is expected and was used to verify HTTP/network-error handling.
Only modify/intercept traffic on systems you are authorised to test.
"""

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


# ============================================================
# GUIDED REVISION — TASK 1
# Python fundamentals
# ============================================================

products = []

product_items = [
    {"name": "Wireless Headphones", "price": "$79.99"},
    {"name": "Mechanical Keyboard", "price": "$129.50"},
    {"name": "USB Microphone", "price": "$59.00"},
]

for item in product_items:
    name = item["name"]
    price = item["price"]

    if float(price.replace("$", "")) < 100:
        products.append({
            "name": name,
            "price": price
        })

print("Filtered products:")
print(products)


# ============================================================
# GUIDED REVISION — TASK 2
# Function + string cleaning + type conversion
# ============================================================

def clean_price(price_text):
    cleaned_price = price_text.replace("$", "")
    price = float(cleaned_price)
    return price


price = clean_price("$1,299.50".replace(",", ""))
print("Cleaned price:", price)


# ============================================================
# GUIDED REVISION — TASK 3
# Requests + HTTP
# ============================================================

url = "https://example.com/products"

try:
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        print("Request successful")
        print("Status:", response.status_code)
        html = response.text
    else:
        print("Request failed:", response.status_code)

except requests.RequestException as e:
    print("Network error:", e)


# ============================================================
# GUIDED REVISION — TASK 4
# BeautifulSoup
# ============================================================

if "html" in locals():
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select(".product")

    scraped_products = []

    for card in cards:
        name_element = card.select_one("h2")
        price_element = card.select_one(".price")

        if name_element and price_element:
            name = name_element.get_text(strip=True)
            price = price_element.get_text(strip=True)

            scraped_products.append({
                "name": name,
                "price": price
            })

    print("Scraped products:")
    print(scraped_products)


# ============================================================
# GUIDED REVISION — TASK 5
# Error handling
# ============================================================

try:
    response = requests.get(url, timeout=10)
    print("Status:", response.status_code)
except requests.RequestException as e:
    print("Request failed safely:", e)


# ============================================================
# GUIDED REVISION — TASK 6
# Playwright browser + navigation + locator
# ============================================================

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    response = page.goto(
        url,
        wait_until="domcontentloaded"
    )

    print("Page URL:", page.url)

    if response:
        print("HTTP status:", response.status)

    heading = page.locator("h1")

    if heading.count() > 0:
        print("Page heading:", heading.first.text_content())

    product_cards = page.locator(".product")
    print("Products found:", product_cards.count())

    browser.close()


# ============================================================
# GUIDED REVISION — TASK 7
# Day 89 → Day 90 bridge
# Observe responses
# ============================================================

def handle_response(response):
    print("Response:", response.status, response.url)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.on("response", handle_response)

    page.goto(
        url,
        wait_until="domcontentloaded"
    )

    browser.close()


# ============================================================
# DAY 90 — TASK 1
# Capturing JSON responses
# ============================================================

json_responses = []


def capture_json_response(response):
    content_type = response.headers.get("content-type", "")

    if "application/json" in content_type:
        try:
            data = response.json()

            json_responses.append({
                "url": response.url,
                "data": data
            })

            print("JSON URL:", response.url)
            print("JSON data:", data)

        except Exception as e:
            print("JSON parsing failed:", e)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.on("response", capture_json_response)

    try:
        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=10000
        )
    except Exception as e:
        print("Navigation error:", e)

    browser.close()


# ============================================================
# DAY 90 — TASK 2
# Request routing
# ============================================================

def handle_route(route):
    request = route.request

    print(
        "Intercepted:",
        request.method,
        request.url
    )

    route.continue_()


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.route("**/*", handle_route)

    try:
        page.goto(url, wait_until="domcontentloaded")
    except Exception as e:
        print("Navigation error:", e)

    browser.close()


# ============================================================
# DAY 90 — TASK 3
# Blocking unnecessary resources
# ============================================================

def block_resources(route):
    resource_type = route.request.resource_type

    if resource_type in ["image", "font", "media"]:
        print(
            "Blocked:",
            resource_type,
            route.request.url
        )
        route.abort()
    else:
        route.continue_()


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.route("**/*", block_resources)

    try:
        page.goto(url, wait_until="domcontentloaded")
    except Exception as e:
        print("Navigation error:", e)

    browser.close()


# ============================================================
# DAY 90 — TASK 4
# Modifying requests in authorised testing
# ============================================================

def modify_request(route):
    headers = route.request.all_headers()

    headers["X-Test-Mode"] = "true"

    print(
        "Modified authorised test request:",
        route.request.url
    )

    route.continue_(headers=headers)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.route("**/*", modify_request)

    try:
        page.goto(url, wait_until="domcontentloaded")
    except Exception as e:
        print("Navigation error:", e)

    browser.close()


# ============================================================
# DAY 90 — TASK 5
# API data vs rendered HTML
# ============================================================

print()
print("API vs rendered HTML decision:")
print("Prefer structured API/network JSON when it provides the required data.")
print("Use rendered HTML/DOM when the information is only available there,")
print("when API data is insufficient, or when validating the visible UI.")


# ============================================================
# DAY 90 — TASK 6
# Network-error handling
# ============================================================

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    try:
        response = page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=10000
        )

        if response:
            print("Status:", response.status)

            if response.status >= 400:
                print(
                    "HTTP error detected:",
                    response.status
                )

    except Exception as e:
        print("Navigation/network error:", e)

    finally:
        browser.close()


# ============================================================
# FINAL INTEGRATED DAY 90 PROGRAM
# Authorised Product Network Monitor
# ============================================================

URL = "https://example.com"

json_responses = []
blocked_resources = []
intercepted_requests = []
html = ""


def capture_json(response):
    content_type = response.headers.get("content-type", "")

    if "application/json" in content_type:
        try:
            data = response.json()

            json_responses.append({
                "url": response.url,
                "data": data
            })

        except Exception as e:
            print("JSON error:", e)


def intercept_request(route):
    request = route.request

    intercepted_requests.append({
        "method": request.method,
        "url": request.url
    })

    resource_type = request.resource_type

    if resource_type in ["image", "font", "media"]:
        blocked_resources.append(request.url)
        route.abort()
        return

    # Authorised testing header only.
    headers = request.all_headers()
    headers["X-Test-Mode"] = "true"

    route.continue_(headers=headers)


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.on("response", capture_json)

    page.route("**/*", intercept_request)

    try:
        response = page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=10000
        )

        if response:
            print("Navigation status:", response.status)

            if response.status >= 400:
                print(
                    "HTTP error detected:",
                    response.status
                )

        html = page.content()

        print(
            "Rendered HTML characters:",
            len(html)
        )

    except Exception as e:
        print("Navigation failed:", e)

    finally:
        browser.close()


print()
print("=" * 60)
print("DAY 90 — NETWORK INTERCEPTION REPORT")
print("=" * 60)

print(
    "Intercepted requests:",
    len(intercepted_requests)
)

print(
    "Blocked resources:",
    len(blocked_resources)
)

print(
    "JSON responses:",
    len(json_responses)
)

print(
    "Rendered HTML captured:",
    len(html)
)

print("=" * 60)
print("DAY 90 COMPLETE — 6/6 SUBTOPICS")
print("=" * 60)
