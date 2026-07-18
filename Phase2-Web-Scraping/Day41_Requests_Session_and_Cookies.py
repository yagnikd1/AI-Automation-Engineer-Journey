"""
===============================================================================
PHASE 2 - WEB SCRAPING
DAY 41 - REQUESTS.SESSION(), COOKIES, AND PRODUCT PRICE ANALYSIS
===============================================================================

TODAY'S MAJOR TOPIC
-------------------
requests.Session() and Cookies

MINOR TOPICS COMPLETED
----------------------
1. Why a session is useful when making several requests to one website.
2. Difference between requests.get() and session.get().
3. Creating a reusable session with requests.Session().
4. Automatically closing a session with a context manager.
5. Closing a session with finally when a context manager is not used.
6. Applying shared headers with session.headers.update().
7. Reusing connections across multiple requests.
8. Understanding cookies and the cookie request-response lifecycle.
9. Creating, reading, updating, and deleting cookies.
10. Automatically sending session cookies with later requests.
11. Difference between response.cookies and session.cookies.
12. Session-cookie and persistent-cookie concepts.
13. Cookie lifetime in a Python Requests session.
14. Inspecting the Cookie header actually sent with a request.
15. Combining sessions and cookies with pagination, timeout, error handling,
    status-code validation, missing-element handling, and random delays.
16. Analysing scraped prices using lists, dictionaries, loops, conditions,
    numeric conversion, totals, averages, minimums, maximums, and budgets.

===============================================================================
1. THE PROBLEM SOLVED BY REQUESTS.SESSION()
===============================================================================

Without an explicitly created session:

    response_1 = requests.get(url_1, headers=headers)
    response_2 = requests.get(url_2, headers=headers)
    response_3 = requests.get(url_3, headers=headers)

Each call uses the module-level request interface. Shared settings such as
headers have to be supplied repeatedly, and application state is not managed
through one session object.

With a session:

    session = requests.Session()
    session.headers.update(headers)

    response_1 = session.get(url_1)
    response_2 = session.get(url_2)
    response_3 = session.get(url_3)

The same reusable request manager handles all three requests. It can maintain:

    - shared headers
    - cookies
    - authentication information
    - common parameters
    - connection pooling and reusable connections

Sessions are especially useful for pagination because multiple pages normally
belong to the same website and should share the same request configuration.

PLAIN-ENGLISH SESSION ALGORITHM
-------------------------------
1. Create one session.
2. Configure shared headers and other settings once.
3. Send every related request through session.get().
4. Allow the session to maintain cookies and reusable connection resources.
5. Close the session when all network work finishes.

===============================================================================
2. CREATING, CONFIGURING, AND CLOSING A SESSION
===============================================================================

Manual creation and closing:

    session = requests.Session()

    try:
        response = session.get(url, timeout=10)
    finally:
        session.close()

The finally block executes whether the request succeeds or fails, ensuring
that the session releases its connection resources.

Recommended context-manager form:

    with requests.Session() as session:
        response = session.get(url, timeout=10)

The session is open inside the with block and closes automatically when the
block finishes.

Only network work needs to remain inside the session block. Data analysis can
run after the block because it uses the collected Python data, not the network.

===============================================================================
3. SHARED SESSION HEADERS
===============================================================================

Correct syntax:

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    session.headers.update(headers)

Every later session.get() request automatically uses these stored headers.

IMPORTANT DEBUGGING NOTE
------------------------
The correct HTTP header name is "User-Agent" with a hyphen.

Incorrect:

    "User Agent": "Mozilla/5.0"

That creates an unrelated custom header instead of setting User-Agent.

Requests may also provide default headers such as Accept, Accept-Encoding,
and Connection. A displayed value such as "Connection: keep-alive" indicates
that connection reuse is supported.

===============================================================================
4. COOKIE FUNDAMENTALS
===============================================================================

A cookie is a small name-value pair used by a website to remember information
about a visitor or session.

Examples:

    currency=USD
    language=en
    session_id=abc123

COOKIE LIFECYCLE
----------------
1. The client sends a request.
2. The server may return a Set-Cookie header in its response.
3. A requests.Session stores the applicable cookie in its cookie jar.
4. The session automatically sends the cookie back on applicable later
   requests.
5. The website can associate those later requests with the same visitor or
   session.

COMMON COOKIE TYPES
-------------------
Session cookie:
    Normally exists only for the current browsing or application session.

Persistent cookie:
    Contains expiry information and is intended to survive longer. However,
    requests.Session() does not automatically write cookies to a disk file.

REQUESTS COOKIE-LIFETIME LIMIT
------------------------------
A Requests session preserves its cookie jar only while that Python session
exists. Closing the program loses those cookies unless the programmer
deliberately saves and reloads them using a separate storage method.

===============================================================================
5. COOKIE MANAGEMENT SYNTAX
===============================================================================

Create cookies:

    session.cookies.set("currency", "USD")
    session.cookies.set("language", "en")

Read one cookie:

    language = session.cookies.get("language")

Read all stored cookies as a dictionary:

    all_cookies = session.cookies.get_dict()

Update a cookie:

    session.cookies.set("language", "fr")

Delete one cookie:

    del session.cookies["currency"]

Delete every cookie:

    session.cookies.clear()

response.cookies versus session.cookies:

    response.cookies
        Cookies received from that individual response.

    session.cookies
        Cookies currently stored across the reusable session.

Inspect the Cookie header actually sent by the request:

    sent_cookie_header = response.request.headers.get("Cookie")

Example result:

    currency=USD; language=en

This proves that session.get() automatically attached the stored cookies to
the outgoing request.

===============================================================================
6. ERRORS OBSERVED AND DEBUGGED TODAY
===============================================================================

ReadTimeout:
    A cookie-testing server did not answer within timeout=10. The session code
    was correct; the external server took too long to respond.

NameResolutionError:
    The computer could not translate a hostname into an IP address. This is a
    DNS/network-resolution failure, not evidence that cookie syntax is wrong.

Indentation issue:
    Analysis code placed inside a with requests.Session() block still runs,
    but unnecessarily keeps the session open during offline calculations.
    Scraping belongs inside the with block; analysis belongs outside it.

===============================================================================
7. COMPLETE DAY 41 PROJECT
===============================================================================

The executable program below:

    - creates one reusable session
    - stores shared headers
    - demonstrates cookie operations
    - paginates through three product pages
    - uses session.get() for every request
    - catches request exceptions
    - validates HTTP status codes
    - parses HTML with BeautifulSoup
    - handles missing HTML elements
    - converts price strings into floats
    - stores products as dictionaries inside a list
    - waits randomly between requests
    - closes the session before analysis begins
    - calculates total and average prices
    - finds the cheapest and most expensive products
    - filters products using a maximum budget
"""

import random
import time

import requests
from bs4 import BeautifulSoup


BASE_URL = (
    "https://webscraper.io/test-sites/e-commerce/"
    "static/computers/laptops?page={}"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

PAGE_START = 1
PAGE_STOP = 4  # range() stops before 4, so pages 1, 2, and 3 are scraped.
REQUEST_TIMEOUT = 10
MINIMUM_DELAY = 1
MAXIMUM_DELAY = 3
DEFAULT_BUDGET = 1000


def demonstrate_cookie_management(session):
    """Demonstrate creating, reading, updating, and deleting cookies."""
    print("\n--- Cookie Management Demonstration ---")

    session.cookies.set("currency", "USD")
    session.cookies.set("language", "en")

    print("Cookie jar:", session.cookies)
    print("Cookies dictionary:", session.cookies.get_dict())

    language = session.cookies.get("language")
    print("Language cookie:", language)

    session.cookies.set("language", "fr")
    print("After updating language:", session.cookies.get_dict())

    del session.cookies["language"]
    print("After deleting language:", session.cookies.get_dict())

    # The currency cookie remains stored and will be automatically added to
    # each applicable request sent through this session.


def extract_products_from_response(response):
    """Extract valid product dictionaries from one successful response."""
    products = []
    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select(".thumbnail")

    print("Products found:", len(cards))

    for card in cards:
        name_element = card.select_one(".title")
        price_element = card.select_one(".price")

        # Either missing element would otherwise cause an AttributeError when
        # get_text() is called. Skipping the incomplete card keeps the scraper
        # running safely.
        if not name_element or not price_element:
            print("Skipped one product with missing information.")
            continue

        name = name_element.get_text(strip=True)
        price_text = price_element.get_text(strip=True)

        # Scraped price: "$416.99" (string)
        # After replace: "416.99" (string)
        # After float:    416.99 (number)
        # Numeric conversion is required for calculations and comparisons.
        price = float(price_text.replace("$", ""))

        product = {
            "name": name,
            "price": price,
        }

        products.append(product)

    return products


def scrape_products():
    """Scrape three pages through one session and return all products."""
    all_products = []

    # The session is automatically closed after this block, even if an error
    # occurs while working inside it.
    with requests.Session() as session:
        session.headers.update(HEADERS)
        demonstrate_cookie_management(session)

        for page in range(PAGE_START, PAGE_STOP):
            url = BASE_URL.format(page)

            print(f"\nScraping page {page}...")
            print("URL:", url)

            try:
                response = session.get(url, timeout=REQUEST_TIMEOUT)
            except requests.exceptions.RequestException as error:
                print("Request failed:", error)
                # Skip only the failed page and continue pagination.
                continue

            print("Status code:", response.status_code)

            if response.status_code != 200:
                print("Skipped page because its status code was not 200.")
                continue

            # Cookies returned by only this particular response.
            print("Response cookies:", response.cookies.get_dict())

            # All cookies currently stored by the session.
            print("Session cookies:", session.cookies.get_dict())

            # Cookies automatically attached to this actual outgoing request.
            sent_cookie_header = response.request.headers.get("Cookie", "None")
            print("Cookie header automatically sent:", sent_cookie_header)

            page_products = extract_products_from_response(response)
            all_products.extend(page_products)

            delay = random.uniform(MINIMUM_DELAY, MAXIMUM_DELAY)
            print(f"Waiting {delay:.2f} seconds...")
            time.sleep(delay)

    # Network work is complete and the session is closed before returning.
    return all_products


def calculate_total_price(products):
    """Return the combined price of every product using a revision loop."""
    total_price = 0

    for product in products:
        total_price += product["price"]

    return total_price


def find_price_extremes(products):
    """Return the cheapest and most expensive product dictionaries."""
    cheapest_product = products[0]
    most_expensive_product = products[0]

    for product in products:
        if product["price"] < cheapest_product["price"]:
            cheapest_product = product

        if product["price"] > most_expensive_product["price"]:
            most_expensive_product = product

    return cheapest_product, most_expensive_product


def filter_products_by_budget(products, budget):
    """Return products whose price is less than or equal to the budget."""
    products_within_budget = []

    for product in products:
        # <= includes prices below the budget and prices exactly equal to it.
        if product["price"] <= budget:
            products_within_budget.append(product)

    return products_within_budget


def analyze_products(products, budget=DEFAULT_BUDGET):
    """Calculate and print all required product-price statistics."""
    print("\n--- Product Price Analysis ---")
    print("Total products collected:", len(products))

    # This guard prevents division by zero and prevents products[0] from
    # raising IndexError when scraping returns no products.
    if not products:
        print("No products available for analysis.")
        return

    total_price = calculate_total_price(products)
    average_price = total_price / len(products)

    cheapest_product, most_expensive_product = find_price_extremes(products)
    products_within_budget = filter_products_by_budget(products, budget)

    print(f"Total price: ${total_price:.2f}")
    print(f"Average price: ${average_price:.2f}")
    print(
        f"Cheapest product: {cheapest_product['name']} "
        f"- ${cheapest_product['price']:.2f}"
    )
    print(
        f"Most expensive product: {most_expensive_product['name']} "
        f"- ${most_expensive_product['price']:.2f}"
    )

    print(f"\nProducts within ${budget}: {len(products_within_budget)}")

    for product in products_within_budget:
        print(f"- {product['name']}: ${product['price']:.2f}")


def main():
    """Run the complete Day 41 session, cookie, and analysis project."""
    products = scrape_products()

    # Analysis happens after scrape_products() returns, so its internal
    # requests.Session has already been closed.
    analyze_products(products)


if __name__ == "__main__":
    main()
