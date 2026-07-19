"""
DAY 42 — WEB SCRAPING REVISION + REST API COMPLETE STUDY GUIDE
================================================================

This file is both:
1. A detailed revision document containing everything studied on Day 42.
2. A runnable collection of the realistic programs built during the lesson.

TODAY'S COMPLETED WORK
----------------------
A. Web-scraping revision project
   Competitor Price Monitor for ASUS Ryzen 9 gaming laptops.
   Final stable retailers: Vijay Sales and Poorvika.

B. REST API lesson
   1. API purpose and request-response flow
   2. Endpoints and resources
   3. GET requests and an overview of other HTTP methods
   4. Query parameters and URL encoding
   5. Request and response headers
   6. HTTP status codes
   7. JSON conversion with response.json()
   8. Nested dictionaries and parallel lists
   9. Filtering, extraction, analysis, and clean output
   10. Pagination
   11. Public APIs, authentication, and safe tokens
   12. API rate limits
   13. JSON, text, CSV, and binary response formats
   14. Connecting two APIs in one workflow
   15. Final GitHub API Monitor project

C. Programs used
   1. Open-Meteo Weather API and Geocoding API
   2. Open Library Search API with pagination
   3. GitHub REST API Monitor

IMPORTANT SCOPE DECISION
------------------------
Detailed request exception handling, automatic retries, and logging were
deliberately postponed until the planned post-Day-50 recovery section.
They are not silently missing from this guide.

INSTALLATION
------------
Run this once if the packages are not already installed:

    pip install requests beautifulsoup4

The websites and APIs are live services. Their HTML, selectors, data, rate
limits, and availability can change after this study file is created.
Always respect a website's terms, robots rules, and reasonable request rates.
"""

import csv
import json
import os
import random
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


# ============================================================================
# SECTION 1 — CORE WEB AND API THEORY
# ============================================================================

DAY_42_THEORY = r"""
1. WHAT IS AN API?
------------------
API means Application Programming Interface.

An API is a defined way for one program to communicate with another program.
Instead of parsing the visible layout of a webpage, a program sends a request
to an API and receives structured data, commonly JSON.

Examples of API uses:
- Read current weather information.
- Convert a city name into latitude and longitude.
- Search a book catalogue.
- Read a public GitHub profile and repository statistics.
- Create or update data when an API and authorization permit it.

Basic request-response flow:
    Python program -> HTTP request -> API endpoint
    API endpoint   -> HTTP response -> Python program

2. ENDPOINT AND RESOURCE
------------------------
An endpoint is a specific API URL that accepts a request for a resource or
operation.

Examples:
- https://api.open-meteo.com/v1/forecast
  Forecast resource.
- https://geocoding-api.open-meteo.com/v1/search
  Location-search resource.
- https://openlibrary.org/search.json
  Book-search resource.
- https://api.github.com/users/yagnikd1
  Public GitHub user resource.
- https://api.github.com/users/yagnikd1/repos
  Public repositories belonging to that user.
- https://api.github.com/rate_limit
  Current GitHub API allowance.

The base URL identifies the API service. The remaining path identifies the
resource. Query parameters add choices or filters to the request.

3. HTTP METHODS
---------------
GET:
    Read or retrieve data. All live API programs used today mainly use GET.

POST:
    Submit data or create a new resource.

PUT:
    Replace a complete resource.

PATCH:
    Update part of an existing resource.

DELETE:
    Delete a resource.

The endpoint documentation decides which methods are supported. A client
cannot safely choose any method it wants.

4. QUERY PARAMETERS
-------------------
Query parameters are key-value settings added after '?' in a URL. Multiple
parameters are separated by '&'.

Example:
    endpoint?latitude=51.5074&longitude=-0.1278&current=temperature_2m

With requests, pass parameters as a dictionary. Requests builds and encodes
the final URL:

    parameters = {
        "latitude": 51.5074,
        "longitude": -0.1278,
        "current": "temperature_2m,relative_humidity_2m"
    }
    response = requests.get(endpoint, params=parameters)

There are not only three possible query parameters. Each API defines its own
available parameters. Open-Meteo supports many current, daily, hourly, unit,
timezone, and forecast-range options.

The string '%2C' in a requested URL is the URL-encoded representation of a
comma. For example, requests may display:
    temperature_2m%2Crelative_humidity_2m
That is normal and means:
    temperature_2m,relative_humidity_2m

5. HEADERS
----------
Request headers provide metadata about the request.

Headers used today:
- Accept: tells the server the response type preferred by the client.
- User-Agent: identifies the client application.
- Authorization: carries a token when authentication is used.
- X-GitHub-Api-Version: chooses a GitHub REST API version.
- Accept-Language: gives a preferred human language/region to a website.

Response headers describe the returned response. Content-Type is important:
    application/json; charset=utf-8
means the server returned JSON encoded as UTF-8 text.

6. HTTP STATUS CODES
--------------------
Status-code families:
- 2xx: request succeeded.
- 3xx: redirection.
- 4xx: client-side request/authentication/limit problem.
- 5xx: server-side problem.

Important individual codes studied:
- 200 OK: request succeeded and data was returned.
- 201 Created: a resource was successfully created.
- 204 No Content: request succeeded without a response body.
- 400 Bad Request: parameters or request data are invalid.
- 401 Unauthorized: valid authentication is missing.
- 403 Forbidden: access is refused, or a policy/rate limit blocks access.
- 404 Not Found: resource or endpoint was not found.
- 429 Too Many Requests: rate limit was exceeded.
- 500 Internal Server Error: server failed unexpectedly.
- 503 Service Unavailable: service is temporarily unavailable.

Actual Day 42 example:
    current=temprature_2m
returned status 400 because 'temperature' was misspelled.

Correct spelling:
    current=temperature_2m
returned status 200.

This showed that a 400 response is useful diagnostic information rather than
just an unexplained program failure.

7. RESPONSE FORMATS AND PYTHON ACCESS
-------------------------------------
JSON response:
    data = response.json()
JSON objects become Python dictionaries. JSON arrays become Python lists.

Plain text or CSV response:
    text_data = response.text

Binary data such as an image or PDF:
    binary_data = response.content

Headers:
    content_type = response.headers.get("Content-Type")

An API can only return formats that its documentation supports. Open-Meteo
uses JSON by default and supports other formats for suitable endpoints. Merely
changing an Accept header does not force every API to support every format.

8. NESTED JSON
--------------
The Open-Meteo response is a top-level dictionary. Its 'current' value is
another dictionary:

    current = weather_data["current"]
    temperature = current["temperature_2m"]

Use .get() when a missing key should have a safe default:

    temperature = current.get("temperature_2m", "Not available")

Daily forecast values arrive as parallel lists:
    daily["time"][0]
    daily["temperature_2m_max"][0]
    daily["temperature_2m_min"][0]

Index 0 in every list describes the same day. Index 1 describes the next day.

9. PAGINATION
-------------
Large APIs split results into pages instead of returning everything at once.

Common parameters:
- page: page number.
- limit or per_page: records requested on each page.

Open Library example used three pages with five books on every page, producing
15 collected records.

GitHub permits up to 100 repositories per page. The program continues until a
page contains fewer than 100 results. If a result count is exactly divisible
by 100, one final empty-page request can occur; it safely ends the loop.

GitHub may also provide a Link response header with next/last page links. The
length-based loop used today is easier to understand and still collects every
public repository.

10. AUTHENTICATION AND TOKEN SAFETY
-----------------------------------
Some endpoints are public and unauthenticated. The public GitHub profile,
public repositories, repository languages, and rate-limit endpoint used today
work without a token.

Authenticated requests can receive a larger rate allowance and can access
authorized resources. Authentication does not automatically grant permission;
the token's permissions still control access.

Never hard-code a secret token into source code or commit it to GitHub.
Read it from an environment variable:

    token = os.getenv("GITHUB_API_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

Temporary PowerShell environment variable example:
    $env:GITHUB_API_TOKEN="your_token_here"

Remove it from the current PowerShell session:
    Remove-Item Env:GITHUB_API_TOKEN

No token was necessary for today's public-data project.

11. RATE LIMITS
---------------
Rate limits restrict how many API requests a client can make in a time window.
GitHub's unauthenticated core allowance observed today was:
    limit: 60

The response reported:
- limit: total allowance in the window.
- used: requests already counted.
- remaining: requests still available.
- reset: Unix timestamp for the reset time.

Repeated program runs increase 'used'. The reset timestamp is converted to a
readable UTC time with time.gmtime() and time.strftime(). GitHub documents that
requesting /rate_limit does not consume the primary rate limit, although it can
still be relevant to secondary limits.

12. WEB SCRAPING VERSUS AN API
------------------------------
Web scraping parses HTML intended mainly for browsers and people. An API
returns data through a documented program interface.

Scraping challenges observed today:
- Flipkart returned 403 to the detailed scraper even though an earlier simple
  diagnostic request could return 200.
- A 200 response and a large HTML body do not guarantee that expected product
  cards exist in the server-returned HTML.
- 'Contains Ryzen 9: True' proves only that the phrase exists somewhere in the
  response; it does not prove selectors can extract complete product records.
- Retailers may use anti-bot protection or client-side JavaScript rendering.
- CSS class names and page structures can change without notice.
- Amazon, Flipkart, and Croma were considered, but stable extraction was not
  available in the learning environment. Vijay Sales and Poorvika produced a
  reliable final learning program.

API advantages:
- Usually documented fields and parameters.
- Structured JSON is easier to parse.
- Pagination and rate-limit rules are explicit.

API limitations:
- Authentication may be required.
- Rate limits apply.
- Not every service exposes the exact desired data.
- Endpoints and versions can change.

13. CLEAN OUTPUT VERSUS DEBUG OUTPUT
------------------------------------
During learning, diagnostics such as requested URL, status, Python type,
top-level keys, and Content-Type helped explain an API response.

For the finished weather program those repeated diagnostics were removed,
leaving a clean user report. Diagnostic prints are useful while learning or
debugging; user-facing output should show only information the user needs.

14. IMPORTANT BUGS FIXED TODAY
------------------------------
- Typo: 'temprature_2m' changed to 'temperature_2m'.
- Retailer key typo: 'basu_url' must be 'base_url'.
- JSON-LD MIME type, when needed, is 'application/ld+json', not
  'application/id+json'.
- Duplicate function definitions and unreachable code after return were
  removed from the early competitor scraper.
- Model extraction originally selected '16GB-1TB'. The extractor was changed
  to exclude hardware-capacity details such as GB, TB, RAM, and SSD, allowing
  model numbers such as G614PH-RV073WS to be selected.
- Products are compared only when their exact normalized model number matches.
  Similar product families are not automatically identical configurations.
- all_products was once referenced outside the scope where it existed. The
  collection and report workflow was moved into main().
- repositories was once printed outside main(), where it was undefined.
- Profile and repository calls were incorrectly combined into one assignment;
  they were separated into two statements.
- The final repository print block was initially outside its for loop. Correct
  indentation now prints every repository and also works when the list is empty.
- The 'Files saved successfully' block was moved to the end of main() so the
  output follows the actual workflow.

15. DATA ACCURACY DETAILS
-------------------------
- clean_price() keeps digits and converts the result to int. This is suitable
  for the displayed whole-rupee prices in today's target pages.
- urljoin() safely combines a retailer base URL and a relative product link.
- Duplicate Poorvika products are prevented by tracking their full URLs.
- Products with MODEL_NOT_FOUND are retained in raw collection/report data but
  excluded from model-to-model price comparisons.
- A comparison requires at least two valid offers for the same exact model.
- Savings = highest valid price - lowest valid price.
- GitHub's open_issues_count includes open pull requests as well as issues.
  Therefore the program's 'open issues' figure follows GitHub's combined field.
- GitHub's languages endpoint returns language names mapped to detected byte
  counts. Today's report keeps the language names; it does not claim percentage
  accuracy.
- Open Library may return records that look duplicated because editions or
  catalogue records can represent the same/similar work. Pagination did not
  create those source-data records.
- Entering 'total available' as the book topic searches those literal words;
  it does not ask the API to print the overall total.
"""


ACTUAL_DAY_42_SESSION_RESULTS = r"""
ACTUAL RESULTS OBSERVED DURING DAY 42
=====================================

These values record today's learning session. Live values can change later.

1. COMPETITOR PRICE MONITOR
---------------------------
The diagnostic stage showed:
- Flipkart: status 200, HTML size 577579, contained 'Ryzen 9': True.
- Vijay Sales: status 200, HTML size 1414278, contained 'Ryzen 9': True.
- Poorvika: status 200, HTML size 476223, contained 'Ryzen 9': True.

The detailed Flipkart product scraper later received status 403 and collected
zero products. This proved that one successful diagnostic request does not
guarantee stable access for every subsequent request or extraction strategy.

The stable final scan produced:
- Poorvika pages scanned: 1 and 2.
- Vijay Sales matching products: 2.
- Poorvika matching products: 3.
- Total products collected: 5.
- Products excluded from comparison: 0.

Exact model comparison:
- G614PH-RV073WS
  Vijay Sales: ₹173,990
  Poorvika: ₹159,990
  Cheapest: Poorvika
  Potential saving: ₹14,000
- G614PM-S5046WS
  Vijay Sales: ₹199,990; only one retailer.
- GA403UM-QS007WS
  Poorvika: ₹201,490; only one retailer.
- G614PR-RV032WS
  Poorvika: ₹229,990; only one retailer.

Files created:
- competitor_prices.csv
- competitor_prices.json
- competitor_report.txt

2. FIRST WEATHER API REQUEST
----------------------------
Endpoint:
    https://api.open-meteo.com/v1/forecast

Initial parameters:
- latitude: 51.5074
- longitude: -0.1278
- current: temprature_2m (incorrect spelling)

Result:
- Status: 400
- JSON error said the string value 'temprature_2m' was invalid.

After changing it to temperature_2m:
- Status: 200
- response.json() returned a Python dict.
- Top-level keys included latitude, longitude, generationtime_ms,
  utc_offset_seconds, timezone, timezone_abbreviation, elevation,
  current_units, and current.
- Nested current data contained time, interval, and temperature_2m.
- London temperature observed during the first successful request: 17.0 °C.

The expanded current request added:
- relative_humidity_2m
- apparent_temperature
- wind_speed_10m
- is_day
- timezone=auto
- temperature_unit=celsius
- wind_speed_unit=kmh

The response Content-Type was:
    application/json; charset=utf-8

3. FIVE-DAY WEATHER AND CONNECTED APIS
--------------------------------------
The daily request added:
- temperature_2m_max
- temperature_2m_min
- precipitation_probability_max
- forecast_days=5

The London example demonstrated indexing through five parallel daily lists.
The later program connected a city-name request to the forecast request:
    Tokyo -> geocoding -> latitude/longitude -> weather forecast

Tokyo location selected:
- Latitude: 35.6895
- Longitude: 139.69171

Tokyo current result observed:
- Temperature: 28.1 °C
- Feels like: 33.2 °C
- Humidity: 77%
- Wind speed: 5.8 km/h
- Day status: Day
- Observation time: 2026-07-19T18:30

Tokyo five-day forecast observed:
- 2026-07-19: max 31.2 °C, min 24.5 °C, rain 16%
- 2026-07-20: max 33.9 °C, min 24.8 °C, rain 8%
- 2026-07-21: max 34.7 °C, min 25.5 °C, rain 84%
- 2026-07-22: max 35.8 °C, min 26.0 °C, rain 80%
- 2026-07-23: max 38.1 °C, min 28.8 °C, rain 96%

The final weather display intentionally removed requested URL, status, Python
type, top-level keys, and other repeated diagnostics to produce cleaner output.

4. OPEN LIBRARY PAGINATION
--------------------------
The entered topic was 'total available'. The API correctly treated it as a
literal search topic.

Observed collection:
- Total available from the API: 146.
- Page 1: 5 books.
- Page 2: 5 books.
- Page 3: 5 books.
- Total collected: 15 books.

The result set included similar catalogue records. This demonstrated that
source data can contain editions or near-duplicates independently of the page
loop.

5. GITHUB AUTHENTICATION AND RATE LIMIT
---------------------------------------
The token experiment printed:
- Token not found.
- Authentication mode: Public and unauthenticated.
- Status code: 200.

This proved that a token was optional for the public endpoints used today.
The initial observed unauthenticated allowance was 60 requests. Repeated runs
increased the used count. The last completed final-program output showed:
- Request limit: 60.
- Requests used: 20.
- Requests remaining: 40.
- Reset time: 2026-07-19 11:18:50 UTC.

6. FINAL GITHUB API MONITOR
---------------------------
Username monitored: yagnikd1

Public profile observed:
- Name: Yagnik
- Bio: Not provided
- Location: Not provided
- Public repositories: 1
- Followers: 0
- Following: 0
- Account created: 2026-05-18T18:37:37Z
- Profile URL: https://github.com/yagnikd1

Repository observed:
- Name: AI-Automation-Engineer-Journey
- Languages: Python
- Stars: 0
- Forks: 0
- Open issues field: 0
- URL: https://github.com/yagnikd1/AI-Automation-Engineer-Journey

Files created:
- github_repositories.csv
- github_monitor.json
- github_report.txt

DAY 42 COMPLETION STATUS
------------------------
The web-scraping revision, all planned API concepts, and the final GitHub API
Monitor were completed and verified. Day 42 was officially marked complete.
"""


def print_study_notes():
    """Print the complete theory notes stored above."""
    print(DAY_42_THEORY)
    print(ACTUAL_DAY_42_SESSION_RESULTS)


# ============================================================================
# SECTION 2 — COMPETITOR PRICE MONITOR (WEB-SCRAPING REVISION)
# ============================================================================

SEARCH_TARGET = {
    "brand": "asus",
    "processor": "ryzen 9",
    "product_type": "gaming laptop"
}

RETAILERS = [
    {
        "name": "Vijay Sales",
        "base_url": "https://www.vijaysales.com",
        "search_url": (
            "https://www.vijaysales.com/c/laptops"
            "?brand=ASUS&categories=Laptops"
        )
    },
    {
        "name": "Poorvika",
        "base_url": "https://www.poorvika.com",
        "search_url": (
            "https://www.poorvika.com/ASUS/s"
            "?brand_name=brand_name%3A%3D%5B%60ASUS%60%5D"
        )
    }
]

SCRAPING_SESSION = requests.Session()
SCRAPING_SESSION.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/150.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9"
})
SCRAPING_SESSION.cookies.set("market_region", "IN")


def matches_search_target(title):
    """Require ASUS + Ryzen 9 + a gaming-laptop indicator in the title."""
    clean_title = title.lower()
    has_brand = SEARCH_TARGET["brand"] in clean_title
    has_processor = SEARCH_TARGET["processor"] in clean_title
    has_product_type = (
        "gaming laptop" in clean_title
        or "rog" in clean_title
        or "tuf gaming" in clean_title
    )
    return has_brand and has_processor and has_product_type


def clean_price(price_text):
    """Convert text such as '₹1,59,990' into integer 159990."""
    digits = ""
    for character in price_text:
        if character.isdigit():
            digits += character

    try:
        return int(digits)
    except ValueError:
        return None


def extract_model_number(title):
    """Find a likely hyphenated model code while rejecting capacity text."""
    cleaned_title = (
        title.replace("(", " ")
        .replace(")", " ")
        .replace(",", " ")
        .replace("/", " ")
    )
    words = cleaned_title.split()
    excluded_details = ["GB", "TB", "RAM", "SSD"]

    for word in reversed(words):
        clean_word = word.strip(".*:;").upper()
        has_hyphen = "-" in clean_word
        has_number = any(character.isdigit() for character in clean_word)
        long_enough = len(clean_word) >= 8
        is_hardware_detail = any(
            detail in clean_word for detail in excluded_details
        )

        if (
            has_hyphen
            and has_number
            and long_enough
            and not is_hardware_detail
        ):
            return clean_word

    return "MODEL_NOT_FOUND"


def create_product(retailer, title, price_text, relative_link):
    """Normalize different retailer fields into one product dictionary."""
    return {
        "retailer": retailer["name"],
        "title": title.strip(),
        "model": extract_model_number(title),
        "price": clean_price(price_text),
        "url": urljoin(retailer["base_url"], relative_link)
    }


def scrape_vijay_sales(retailer):
    """Collect matching Vijay Sales product cards from its laptop page."""
    products = []
    response = SCRAPING_SESSION.get(retailer["search_url"], timeout=20)

    if response.status_code != 200:
        print(retailer["name"], "returned status:", response.status_code)
        return products

    soup = BeautifulSoup(response.text, "html.parser")
    product_cards = soup.select("div.product-card")

    for card in product_cards:
        title_tag = card.select_one(".product-name")
        price_tag = card.select_one(".discountedPrice")
        link_tag = card.select_one("a.product-card__link")

        if title_tag is None or price_tag is None or link_tag is None:
            continue

        title = title_tag.get_text(" ", strip=True)
        price_text = price_tag.get("data-price", "")
        relative_link = link_tag.get("href", "")

        if matches_search_target(title):
            products.append(
                create_product(retailer, title, price_text, relative_link)
            )

    return products


def scrape_poorvika(retailer):
    """Scan every discovered Poorvika page and prevent duplicate URLs."""
    products = []
    collected_links = set()
    page_number = 1
    total_pages = 1

    while page_number <= total_pages:
        if page_number == 1:
            page_url = retailer["search_url"]
        else:
            page_url = retailer["search_url"] + f"&page={page_number}"

        print("Scanning Poorvika page:", page_number)
        response = SCRAPING_SESSION.get(page_url, timeout=20)

        if response.status_code != 200:
            print(
                retailer["name"], "page", page_number,
                "returned status:", response.status_code
            )
            return products

        soup = BeautifulSoup(response.text, "html.parser")

        if page_number == 1:
            pagination_items = soup.select(
                "li[class*='pagination_pagination_item__']"
            )
            for item in pagination_items:
                page_text = item.get_text(strip=True)
                if page_text.isdigit():
                    total_pages = max(total_pages, int(page_text))

        product_cards = soup.select(
            "div[class*='product-cardlist_card--border']"
        )

        for card in product_cards:
            description = card.select_one(
                "div[class*='product-cardlist_card__description']"
            )
            if description is None:
                continue

            link_tag = description.select_one("a[href]")
            title_tag = description.select_one("a[href] > b")
            price_tags = description.select(
                "div[class*='product-cardlist_price__'] span"
            )

            if link_tag is None or title_tag is None:
                continue

            price_text = ""
            for price_tag in price_tags:
                current_text = price_tag.get_text(" ", strip=True)
                if "₹" in current_text:
                    price_text = current_text
                    break

            if price_text == "":
                continue

            title = title_tag.get_text(" ", strip=True)
            relative_link = link_tag.get("href", "")

            if matches_search_target(title):
                product = create_product(
                    retailer, title, price_text, relative_link
                )
                if product["url"] not in collected_links:
                    products.append(product)
                    collected_links.add(product["url"])

        if page_number < total_pages:
            time.sleep(random.uniform(1, 2))
        page_number += 1

    return products


def group_products_by_model(products):
    """Separate unknown models and group valid products by exact model code."""
    model_groups = {}
    unmatched_products = []

    for product in products:
        model = product["model"]
        if model == "MODEL_NOT_FOUND":
            unmatched_products.append(product)
            continue
        if model not in model_groups:
            model_groups[model] = []
        model_groups[model].append(product)

    return model_groups, unmatched_products


def find_price_comparison(offers):
    """Return valid offers, cheapest offer, most expensive offer, and saving."""
    valid_offers = [offer for offer in offers if offer["price"] is not None]
    if len(valid_offers) < 2:
        return valid_offers, None, None, None

    cheapest = min(valid_offers, key=lambda offer: offer["price"])
    most_expensive = max(valid_offers, key=lambda offer: offer["price"])
    savings = most_expensive["price"] - cheapest["price"]
    return valid_offers, cheapest, most_expensive, savings


def save_competitor_reports(products, groups):
    """Save normalized rows, structured scan data, and a readable report."""
    scan_time = time.strftime("%Y-%m-%d %H:%M:%S")
    csv_fields = ["retailer", "model", "price", "title", "url"]

    with open(
        "competitor_prices.csv", "w", newline="", encoding="utf-8-sig"
    ) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows(products)

    json_report = {
        "scan_time": scan_time,
        "search_target": SEARCH_TARGET,
        "total_products": len(products),
        "model_groups": groups
    }
    with open("competitor_prices.json", "w", encoding="utf-8") as json_file:
        json.dump(json_report, json_file, indent=4, ensure_ascii=False)

    lines = [
        "ASUS RYZEN 9 COMPETITOR PRICE REPORT",
        "=" * 45,
        f"Scan time: {scan_time}",
        f"Products collected: {len(products)}"
    ]

    for model, offers in groups.items():
        valid, cheapest, _most_expensive, savings = find_price_comparison(
            offers
        )
        lines.extend(["", f"Model: {model}"])
        for offer in valid:
            lines.append(f"{offer['retailer']}: ₹{offer['price']:,}")

        if cheapest is not None:
            lines.append(f"Cheapest retailer: {cheapest['retailer']}")
            lines.append(f"Potential savings: ₹{savings:,}")
        elif len(valid) == 1:
            lines.append("Comparison unavailable: only one retailer found")
        else:
            lines.append("No valid price found")

    with open("competitor_report.txt", "w", encoding="utf-8") as text_file:
        text_file.write("\n".join(lines))


def run_competitor_price_monitor():
    """Run the completed Day 42 web-scraping revision project."""
    vijay_products = scrape_vijay_sales(RETAILERS[0])
    time.sleep(random.uniform(1, 2))
    poorvika_products = scrape_poorvika(RETAILERS[1])
    all_products = vijay_products + poorvika_products
    model_groups, unmatched = group_products_by_model(all_products)

    print("Vijay Sales matching products:", len(vijay_products))
    print("Poorvika matching products:", len(poorvika_products))
    print("Total products collected:", len(all_products))
    print("Products excluded from comparison:", len(unmatched))
    print("\nCOMPETITOR PRICE REPORT")

    for model, offers in model_groups.items():
        valid, cheapest, _most_expensive, savings = find_price_comparison(
            offers
        )
        print("\nModel:", model)
        for offer in valid:
            print(offer["retailer"], "-", f"₹{offer['price']:,}")

        if cheapest is not None:
            print("Cheapest retailer:", cheapest["retailer"])
            print("Potential savings:", f"₹{savings:,}")
        elif len(valid) == 1:
            print("Comparison unavailable: found at only one retailer")
        else:
            print("No valid price was found")

    save_competitor_reports(all_products, model_groups)
    print("\nFiles saved successfully:")
    print("- competitor_prices.csv")
    print("- competitor_prices.json")
    print("- competitor_report.txt")


# ============================================================================
# SECTION 3 — OPEN-METEO WEATHER + GEOCODING API
# ============================================================================

GEOCODING_ENDPOINT = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_ENDPOINT = "https://api.open-meteo.com/v1/forecast"


def find_city(city_name):
    """Turn a city name into the first matching latitude/longitude result."""
    parameters = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    response = requests.get(
        GEOCODING_ENDPOINT, params=parameters, timeout=20
    )
    data = response.json()
    results = data.get("results", [])
    if not results:
        return None

    location = results[0]
    return {
        "name": location.get("name", city_name),
        "country": location.get("country", "Not available"),
        "latitude": location.get("latitude"),
        "longitude": location.get("longitude")
    }


def get_weather(latitude, longitude):
    """Request current weather and five parallel daily forecast lists."""
    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,relative_humidity_2m,apparent_temperature,"
            "wind_speed_10m,is_day"
        ),
        "daily": (
            "temperature_2m_max,temperature_2m_min,"
            "precipitation_probability_max"
        ),
        "forecast_days": 5,
        "timezone": "auto",
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh"
    }
    response = requests.get(
        FORECAST_ENDPOINT, params=parameters, timeout=20
    )
    return response.json()


def display_weather_report(location, weather_data):
    """Present nested current data and indexed daily lists cleanly."""
    current = weather_data.get("current", {})
    daily = weather_data.get("daily", {})
    day_status = "Day" if current.get("is_day") == 1 else "Night"

    print(f"\nWEATHER REPORT: {location['name']}, {location['country']}")
    print("\nCURRENT WEATHER REPORT")
    print("Temperature:", current.get("temperature_2m"), "°C")
    print("Feels like:", current.get("apparent_temperature"), "°C")
    print("Humidity:", current.get("relative_humidity_2m"), "%")
    print("Wind speed:", current.get("wind_speed_10m"), "km/h")
    print("Day status:", day_status)
    print("Observation time:", current.get("time"))
    print("\nFIVE-DAY FORECAST")

    dates = daily.get("time", [])
    maximums = daily.get("temperature_2m_max", [])
    minimums = daily.get("temperature_2m_min", [])
    rain_probabilities = daily.get("precipitation_probability_max", [])

    for index in range(len(dates)):
        print("-" * 35)
        print("Date:", dates[index])
        print("Maximum:", maximums[index], "°C")
        print("Minimum:", minimums[index], "°C")
        print("Rain probability:", rain_probabilities[index], "%")


def run_weather_api_program():
    """Connect geocoding output to the forecast endpoint input."""
    city_name = input("Enter a city name: ").strip()
    location = find_city(city_name)
    if location is None:
        print("City not found.")
        return
    weather_data = get_weather(location["latitude"], location["longitude"])
    display_weather_report(location, weather_data)


# ============================================================================
# SECTION 4 — OPEN LIBRARY SEARCH API PAGINATION
# ============================================================================

OPEN_LIBRARY_ENDPOINT = "https://openlibrary.org/search.json"


def search_books(topic, pages=3, books_per_page=5):
    """Collect selected book fields from multiple Open Library pages."""
    collected_books = []
    total_available = 0

    for page_number in range(1, pages + 1):
        parameters = {
            "q": topic,
            "page": page_number,
            "limit": books_per_page,
            "fields": "title,author_name,first_publish_year"
        }
        response = requests.get(
            OPEN_LIBRARY_ENDPOINT, params=parameters, timeout=20
        )
        data = response.json()
        total_available = data.get("numFound", 0)
        documents = data.get("docs", [])

        for document in documents:
            authors = document.get("author_name", [])
            collected_books.append({
                "title": document.get("title", "Not available"),
                "author": ", ".join(authors) if authors else "Not available",
                "first_published": document.get(
                    "first_publish_year", "Not available"
                )
            })

        print(
            "Collected page:", page_number,
            "| Books:", len(documents)
        )

        if len(documents) < books_per_page:
            break

    return collected_books, total_available


def run_open_library_program():
    """Run the three-page book-search demonstration."""
    topic = input("Enter a book topic: ").strip()
    books, total_available = search_books(topic)

    print("\nBOOK SEARCH REPORT")
    print("Topic:", topic)
    print("Total available:", total_available)
    print("Books collected:", len(books))

    for result_number, book in enumerate(books, start=1):
        print("-" * 45)
        print("Result:", result_number)
        print("Title:", book["title"])
        print("Author:", book["author"])
        print("First published:", book["first_published"])


# ============================================================================
# SECTION 5 — FINAL GITHUB REST API MONITOR
# ============================================================================

GITHUB_USERNAME = "yagnikd1"
GITHUB_BASE_URL = "https://api.github.com"


def create_github_headers():
    """Create public headers and add a token only when the environment has it."""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
        "User-Agent": "Day42-GitHub-API-Monitor/1.0"
    }
    api_token = os.getenv("GITHUB_API_TOKEN")
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}"
    return headers


def get_github_public_profile(username, headers):
    """Read and normalize selected public profile fields."""
    profile_url = f"{GITHUB_BASE_URL}/users/{username}"
    response = requests.get(profile_url, headers=headers, timeout=20)
    profile_data = response.json()

    profile = {
        "username": profile_data.get("login", "Not available"),
        "name": profile_data.get("name") or "Not provided",
        "bio": profile_data.get("bio") or "Not provided",
        "location": profile_data.get("location") or "Not provided",
        "profile_url": profile_data.get("html_url", "Not available"),
        "public_repositories": profile_data.get("public_repos", 0),
        "followers": profile_data.get("followers", 0),
        "following": profile_data.get("following", 0),
        "created_at": profile_data.get("created_at", "Not available")
    }
    return profile, response.status_code


def get_all_github_public_repositories(username, headers):
    """Collect every public repository by requesting up to 100 per page."""
    repositories = []
    page = 1
    per_page = 100

    while True:
        repositories_url = f"{GITHUB_BASE_URL}/users/{username}/repos"
        parameters = {
            "page": page,
            "per_page": per_page,
            "sort": "full_name",
            "direction": "asc"
        }
        response = requests.get(
            repositories_url,
            headers=headers,
            params=parameters,
            timeout=20
        )
        repositories_page = response.json()
        if not repositories_page:
            break

        repositories.extend(repositories_page)
        if len(repositories_page) < per_page:
            break
        page += 1

    return repositories


def collect_github_repository_details(repositories, headers):
    """Add all detected language names and requested repository statistics."""
    repository_details = []

    for repository in repositories:
        languages_response = requests.get(
            repository.get("languages_url"),
            headers=headers,
            timeout=20
        )
        languages_data = languages_response.json()

        repository_details.append({
            "name": repository.get("name", "Not available"),
            "url": repository.get("html_url", "Not available"),
            "languages": list(languages_data.keys()),
            "stars": repository.get("stargazers_count", 0),
            "forks": repository.get("forks_count", 0),
            "open_issues": repository.get("open_issues_count", 0)
        })

    return repository_details


def get_github_rate_limit(headers):
    """Read the core API allowance and convert the Unix reset timestamp."""
    response = requests.get(
        f"{GITHUB_BASE_URL}/rate_limit", headers=headers, timeout=20
    )
    data = response.json()
    core_limit = data.get("resources", {}).get("core", {})
    reset_timestamp = core_limit.get("reset", 0)

    if reset_timestamp:
        reset_time = time.strftime(
            "%Y-%m-%d %H:%M:%S UTC", time.gmtime(reset_timestamp)
        )
    else:
        reset_time = "Not available"

    return {
        "limit": core_limit.get("limit", 0),
        "used": core_limit.get("used", 0),
        "remaining": core_limit.get("remaining", 0),
        "reset_timestamp": reset_timestamp,
        "reset_time": reset_time
    }


def save_github_reports(profile, repository_details, rate_limit):
    """Save repositories to CSV and the complete monitor to JSON and text."""
    csv_fields = ["name", "languages", "stars", "forks", "open_issues", "url"]

    with open(
        "github_repositories.csv", "w", newline="", encoding="utf-8"
    ) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_fields)
        writer.writeheader()
        for repository in repository_details:
            csv_row = repository.copy()
            csv_row["languages"] = ", ".join(repository["languages"])
            writer.writerow(csv_row)

    complete_report = {
        "profile": profile,
        "repositories": repository_details,
        "rate_limit": rate_limit
    }
    with open("github_monitor.json", "w", encoding="utf-8") as json_file:
        json.dump(complete_report, json_file, indent=4, ensure_ascii=False)

    lines = [
        "GITHUB API MONITOR REPORT",
        "=" * 50,
        "",
        "PUBLIC PROFILE",
        "-" * 50,
        f"Username: {profile['username']}",
        f"Name: {profile['name']}",
        f"Bio: {profile['bio']}",
        f"Location: {profile['location']}",
        f"Public repositories: {profile['public_repositories']}",
        f"Followers: {profile['followers']}",
        f"Following: {profile['following']}",
        f"Account created: {profile['created_at']}",
        f"Profile URL: {profile['profile_url']}",
        "",
        "PUBLIC REPOSITORIES",
        "-" * 50
    ]

    for repository in repository_details:
        language_text = (
            ", ".join(repository["languages"])
            if repository["languages"]
            else "Not detected"
        )
        lines.extend([
            f"Repository: {repository['name']}",
            f"Languages: {language_text}",
            f"Stars: {repository['stars']}",
            f"Forks: {repository['forks']}",
            f"Open issues: {repository['open_issues']}",
            f"URL: {repository['url']}",
            ""
        ])

    lines.extend([
        "API RATE-LIMIT STATUS",
        "-" * 50,
        f"Request limit: {rate_limit['limit']}",
        f"Requests used: {rate_limit['used']}",
        f"Requests remaining: {rate_limit['remaining']}",
        f"Reset time: {rate_limit['reset_time']}"
    ])

    with open("github_report.txt", "w", encoding="utf-8") as text_file:
        text_file.write("\n".join(lines))


def run_github_api_monitor():
    """Run the completed final Day 42 API project."""
    headers = create_github_headers()
    profile, status_code = get_github_public_profile(
        GITHUB_USERNAME, headers
    )
    repositories = get_all_github_public_repositories(
        GITHUB_USERNAME, headers
    )
    repository_details = collect_github_repository_details(
        repositories, headers
    )
    rate_limit = get_github_rate_limit(headers)

    print("GITHUB PUBLIC PROFILE")
    print("-" * 40)
    print("Status code:", status_code)
    print("Username:", profile["username"])
    print("Name:", profile["name"])
    print("Bio:", profile["bio"])
    print("Location:", profile["location"])
    print("Public repositories:", profile["public_repositories"])
    print("Followers:", profile["followers"])
    print("Following:", profile["following"])
    print("Account created:", profile["created_at"])
    print("Profile URL:", profile["profile_url"])

    print("\nPUBLIC REPOSITORIES")
    print("-" * 40)
    print("Repositories collected:", len(repositories))

    for repository in repository_details:
        language_text = (
            ", ".join(repository["languages"])
            if repository["languages"]
            else "Not detected"
        )
        print("\nRepository:", repository["name"])
        print("Languages:", language_text)
        print("Stars:", repository["stars"])
        print("Forks:", repository["forks"])
        print("Open issues:", repository["open_issues"])
        print("URL:", repository["url"])

    print("\nAPI RATE-LIMIT STATUS")
    print("-" * 40)
    print("Request limit:", rate_limit["limit"])
    print("Requests used:", rate_limit["used"])
    print("Requests remaining:", rate_limit["remaining"])
    print("Reset time:", rate_limit["reset_time"])

    save_github_reports(profile, repository_details, rate_limit)
    print("\nFiles saved successfully:")
    print("- github_repositories.csv")
    print("- github_monitor.json")
    print("- github_report.txt")


# ============================================================================
# SECTION 6 — QUICK REFERENCE AND RUN MENU
# ============================================================================

QUICK_REFERENCE = """
DAY 42 QUICK REFERENCE
======================
requests.get(url, params=params, headers=headers, timeout=20)
response.status_code          -> HTTP status integer
response.url                  -> final encoded URL
response.headers              -> response metadata dictionary
response.headers.get(...)     -> one response header
response.json()               -> JSON converted to Python dict/list
response.text                 -> decoded text response
response.content              -> raw bytes

BeautifulSoup(response.text, "html.parser")
soup.select("selector")       -> all matching tags
soup.select_one("selector")   -> first matching tag or None
tag.get_text(" ", strip=True) -> clean visible text
tag.get("href", "")          -> attribute with a safe default
urljoin(base_url, link)       -> absolute URL

JSON -> dict/list -> extract -> normalize -> analyze -> report
HTML -> soup -> cards -> tags -> normalize -> analyze -> report

CSV is best for rows and spreadsheet analysis.
JSON preserves nested structure and Python-like data types.
Text is best for a readable human report.
"""


def show_menu():
    """Let this single study file run any completed Day 42 program."""
    print("DAY 42 — WEB SCRAPING AND REST API STUDY GUIDE")
    print("1. Print complete theory notes")
    print("2. Run competitor price monitor")
    print("3. Run weather API program")
    print("4. Run Open Library pagination program")
    print("5. Run GitHub API monitor")
    print("6. Print quick reference")
    choice = input("Choose 1-6: ").strip()

    if choice == "1":
        print_study_notes()
    elif choice == "2":
        run_competitor_price_monitor()
    elif choice == "3":
        run_weather_api_program()
    elif choice == "4":
        run_open_library_program()
    elif choice == "5":
        run_github_api_monitor()
    elif choice == "6":
        print(QUICK_REFERENCE)
    else:
        print("Invalid choice. Run the file again and choose 1 to 6.")


if __name__ == "__main__":
    show_menu()
