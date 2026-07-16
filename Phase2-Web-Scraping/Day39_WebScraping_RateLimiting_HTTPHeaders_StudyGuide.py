"""
===============================================================================
Day39_WebScraping_RateLimiting_HTTPHeaders_StudyGuide.py
Phase 2 - Web Scraping
===============================================================================

DAY 38 (Completed Today)

1. HTTP Headers
---------------
Headers are extra information sent with an HTTP request.

Example:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

Purpose:
- Identify the client making the request.
- Some websites treat browser requests differently from the default
  python-requests client.

2. User-Agent
-------------
A User-Agent is one HTTP header.

Default requests client:
    python-requests/...

Browser example:
    Mozilla/5.0 ...

Usage:
    response = requests.get(url, headers=headers)

3. HTTP Status Codes
--------------------
200 -> Success
403 -> Forbidden (page exists, access denied)
404 -> Not Found (page/resource doesn't exist)
429 -> Too Many Requests (slow down)
500 -> Internal Server Error (website problem)

Professional pattern:

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Safe to parse HTML
else:
    # Handle the error

===============================================================================

DAY 39

4. Rate Limiting
----------------
Websites limit request frequency to:
- Protect CPU/RAM/Bandwidth
- Prevent abuse
- Keep the site responsive

Sending requests too quickly may cause:
- 403
- 429
- CAPTCHA
- Temporary IP blocking

5. time.sleep()
---------------
import time

time.sleep(2)

Pauses the program for 2 seconds.

6. Random Delays
----------------
import random

random.randint(1,3)
    -> 1, 2 or 3

random.uniform(1,3)
    -> Any decimal between 1.0 and 3.0

Preferred for scraping:
    time.sleep(random.uniform(1,3))

7. Correct Placement of Delay
-----------------------------
INSIDE:
    for page in range(...)

OUTSIDE:
    for card in cards:

Reason:
Delay should happen BETWEEN page requests,
not between individual products.

Structure:

for page:
    request page

    if success:
        scrape every product

    time.sleep(random.uniform(1,3))

print(all_products)

===============================================================================
Complete Example
===============================================================================
"""

import requests
from bs4 import BeautifulSoup
import random
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_products = []

for page in range(1, 4):

    url = f"https://example.com?page={page}"

    response = requests.get(url, headers=headers)

    print(f"\nScraping Page {page}")
    print("Status Code:", response.status_code)

    if response.status_code == 200:

        soup = BeautifulSoup(response.text, "html.parser")

        cards = soup.select(".product")

        for card in cards:

            title = card.select_one(".title")
            price = card.select_one(".price")

            if title:
                title = title.get_text(strip=True)
            else:
                title = "N/A"

            if price:
                price = price.get_text(strip=True)
            else:
                price = "N/A"

            product = {
                "title": title,
                "price": price
            }

            all_products.append(product)

            print(title, "-", price)

    elif response.status_code == 403:
        print("403 Forbidden")

    elif response.status_code == 404:
        print("404 Not Found")

    elif response.status_code == 429:
        print("429 Too Many Requests")

    elif response.status_code == 500:
        print("500 Internal Server Error")

    time.sleep(random.uniform(1,3))

print("\nAll Products")
print(all_products)
