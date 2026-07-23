"""
DAY 46: COMPREHENSIVE WEB SCRAPING, API, VALIDATION, AND STORAGE REVISION
========================================================================

PURPOSE
-------
This executable study guide combines the main Python and Phase 2 web-scraping
skills revised on Day 46 in one controlled project. It creates a local training
website, checks its automation policy, collects paginated HTML records, reads
API metadata, retains a session cookie, validates the extracted records,
analyses them, saves them in three formats, and verifies the complete workflow.

PROJECT: COMMUNITY SERVICE DIRECTORY ANALYZER
---------------------------------------------
The program revises:

1. Python fundamentals
   - Variables and data types
   - Lists and dictionaries
   - Functions and return values
   - for and while loops
   - if/elif/else conditions
   - list comprehensions
   - sum(), len(), max(), enumerate(), and lambda

2. HTML and BeautifulSoup
   - HTML tags, classes, and data attributes
   - BeautifulSoup(..., "html.parser")
   - CSS selectors with select() and select_one()
   - get_text(strip=True)
   - Extracting an attribute with element.get()
   - Converting extracted text with int() and float()

3. Controlled HTTP access
   - A local ThreadingHTTPServer used only for safe training
   - requests.Session() for shared headers, cookies, and connections
   - An identifiable User-Agent
   - A timeout on every HTTP request
   - Status-code verification

4. Ethical access and pagination
   - Terms of Service checked before scraping
   - robots.txt checked after the terms
   - RobotFileParser.can_fetch()
   - RobotFileParser.crawl_delay()
   - Safe stopping for 403, 404, 503, and unexpected statuses
   - urljoin() for a relative next-page link
   - time.sleep() for the crawl delay

5. REST API and session cookies
   - A controlled JSON API endpoint
   - Content-Type verification
   - response.json()
   - API metadata used by the program
   - A cookie received through Set-Cookie and retained by the session

6. Data analysis and quality checks
   - Missing-key, None, and empty-text detection
   - Duplicate-name detection with strip(), casefold(), and a set
   - Filtering available and recommended services
   - Totals, average rating, and highest-rated service

7. File and database storage
   - csv.DictWriter
   - json.dump()
   - SQLite table creation and parameterized SQL
   - executemany(), commit(), SELECT, SUM(), COUNT(), and fetchone()
   - Reading exports back for verification

8. Automated verification
   - Thirteen checks confirm the final end-to-end result.

EXPECTED FINAL RESULT
---------------------
Final result: 13/13 checks passed
DAY 46 PROGRAM VERIFICATION: PASS

INSTALLATION
------------
This program requires two third-party packages:

    pip install requests beautifulsoup4

The HTTP server, API, HTML pages, terms, and robots.txt are all local. The
program does not scrape a real external website.

ROADMAP BOUNDARY
----------------
Completed here: the Day 46 comprehensive revision.

Still unfinished after this file:
    - Final Phase 2 capstone/assessment
    - Exact allocation of Days 47-50

Deferred to the post-Day-50 recovery program:
    - Comprehensive request-error handling
    - Retry mechanisms
    - Logging and debugging
"""

import csv
import json
import sqlite3
import time

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup


# =============================================================================
# SECTION 1: CONTROLLED TRAINING WEBSITE DATA
# =============================================================================

# Page 1 contains three service cards and a relative link to page 2.
PAGE_ONE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Community Service Directory - Page 1</title>
</head>
<body>
    <section id="service-directory">

        <article class="service-card" data-free="true">
            <h2 class="service-name">Career Support Center</h2>
            <p class="category">Employment</p>
            <span class="rating">4.7</span>
            <span class="available-slots">12</span>
        </article>

        <article class="service-card" data-free="true">
            <h2 class="service-name">Digital Skills Lab</h2>
            <p class="category">Education</p>
            <span class="rating">4.5</span>
            <span class="available-slots">0</span>
        </article>

        <article class="service-card" data-free="false">
            <h2 class="service-name">Family Wellness Clinic</h2>
            <p class="category">Health</p>
            <span class="rating">4.8</span>
            <span class="available-slots">7</span>
        </article>

        <a class="next-page" href="/services?page=2">Next</a>

    </section>
</body>
</html>
"""


# Page 2 contains the final three service cards and no next-page link.
PAGE_TWO_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Community Service Directory - Page 2</title>
</head>
<body>
    <section id="service-directory">

        <article class="service-card" data-free="true">
            <h2 class="service-name">Language Learning Hub</h2>
            <p class="category">Education</p>
            <span class="rating">4.2</span>
            <span class="available-slots">5</span>
        </article>

        <article class="service-card" data-free="true">
            <h2 class="service-name">Housing Advice Center</h2>
            <p class="category">Housing</p>
            <span class="rating">4.6</span>
            <span class="available-slots">3</span>
        </article>

        <article class="service-card" data-free="true">
            <h2 class="service-name">Community Legal Aid</h2>
            <p class="category">Legal</p>
            <span class="rating">4.4</span>
            <span class="available-slots">2</span>
        </article>

    </section>
</body>
</html>
"""


# =============================================================================
# SECTION 2: LOCAL WEBSITE AND API HANDLER
# =============================================================================

class TrainingWebsiteHandler(BaseHTTPRequestHandler):
    """Serve the controlled terms, robots.txt, API, and HTML training pages."""

    def send_text_response(self, content, content_type="text/html"):
        """Encode text and send a successful HTTP response."""
        encoded_content = content.encode("utf-8")

        self.send_response(200)
        self.send_header(
            "Content-Type",
            f"{content_type}; charset=utf-8"
        )
        self.send_header("Content-Length", str(len(encoded_content)))
        self.end_headers()
        self.wfile.write(encoded_content)

    def send_json_response(self, data):
        """Serialize a dictionary and send it as JSON with a session cookie."""
        encoded_content = json.dumps(data).encode("utf-8")

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header("Content-Length", str(len(encoded_content)))
        self.send_header(
            "Set-Cookie",
            "directory_session=training-approved; Path=/"
        )
        self.end_headers()
        self.wfile.write(encoded_content)

    def do_GET(self):
        """Return a response based on the requested local path."""
        parsed_url = urlparse(self.path)

        if parsed_url.path == "/terms":
            self.send_text_response(
                "Automated training access: allowed.",
                "text/plain"
            )

        elif parsed_url.path == "/robots.txt":
            self.send_text_response(
                "User-agent: TrainingResearchBot/1.0\n"
                "Allow: /\n"
                "Crawl-delay: 1\n",
                "text/plain"
            )

        elif parsed_url.path == "/api/directory-status":
            self.send_json_response({
                "directory_name": "Community Service Directory",
                "api_version": "1.0",
                "active": True,
                "expected_records": 6,
                "minimum_recommended_rating": 4.3
            })

        elif self.path == "/services?page=1":
            self.send_text_response(PAGE_ONE_HTML)

        elif self.path == "/services?page=2":
            self.send_text_response(PAGE_TWO_HTML)

        else:
            self.send_error(404, "Page not found")

    def log_message(self, format, *args):
        """Prevent the local server from printing a line for every request."""
        return


# =============================================================================
# SECTION 3: REUSABLE FUNCTIONS
# =============================================================================

def extract_services(html):
    """
    Extract service dictionaries from one HTML page.

    select() returns every matching service card.
    select_one() returns the first matching child element.
    get_text(strip=True) removes surrounding whitespace from visible text.
    """
    soup = BeautifulSoup(html, "html.parser")
    service_cards = soup.select("article.service-card")
    extracted_services = []

    for card in service_cards:
        service = {
            "name": card.select_one(
                ".service-name"
            ).get_text(strip=True),

            "category": card.select_one(
                ".category"
            ).get_text(strip=True),

            "rating": float(
                card.select_one(
                    ".rating"
                ).get_text(strip=True)
            ),

            "available_slots": int(
                card.select_one(
                    ".available-slots"
                ).get_text(strip=True)
            ),

            # The comparison converts the HTML attribute text into a Boolean.
            "is_free": card.get("data-free") == "true"
        }

        extracted_services.append(service)

    return soup, extracted_services


def is_recommended(service, minimum_rating=4.3):
    """Return True only when one service satisfies all three conditions."""
    return (
        service["rating"] >= minimum_rating
        and service["available_slots"] > 0
        and service["is_free"]
    )


def validate_services(services):
    """
    Exclude records with missing data or duplicate normalized names.

    Numerical zero is valid, so only missing keys, None, and empty text are
    treated as missing. casefold() makes duplicate comparison
    case-insensitive.
    """
    required_fields = [
        "name",
        "category",
        "rating",
        "available_slots",
        "is_free"
    ]

    validated_services = []
    seen_service_names = set()
    missing_record_count = 0
    duplicate_record_count = 0

    for service in services:
        has_missing_data = False

        for field in required_fields:
            if field not in service:
                has_missing_data = True
                break

            field_value = service[field]

            if field_value is None:
                has_missing_data = True
                break

            if (
                isinstance(field_value, str)
                and not field_value.strip()
            ):
                has_missing_data = True
                break

        if has_missing_data:
            missing_record_count += 1
            continue

        normalized_name = service["name"].strip().casefold()

        if normalized_name in seen_service_names:
            duplicate_record_count += 1
            continue

        seen_service_names.add(normalized_name)
        validated_services.append(service)

    return (
        validated_services,
        missing_record_count,
        duplicate_record_count
    )


# =============================================================================
# SECTION 4: START THE CONTROLLED LOCAL WEBSITE
# =============================================================================

# Port 0 asks the operating system to choose an unused local port.
server = ThreadingHTTPServer(
    ("127.0.0.1", 0),
    TrainingWebsiteHandler
)

server_port = server.server_address[1]

# The daemon thread lets the program make requests to its own local server.
server_thread = Thread(
    target=server.serve_forever,
    daemon=True
)
server_thread.start()


base_url = f"http://127.0.0.1:{server_port}"
terms_url = f"{base_url}/terms"
robots_url = f"{base_url}/robots.txt"
api_url = f"{base_url}/api/directory-status"


# =============================================================================
# SECTION 5: SESSION, TERMS, ROBOTS.TXT, API, COOKIE, AND PAGINATION
# =============================================================================

session = requests.Session()
session.headers.update({
    "User-Agent": "TrainingResearchBot/1.0"
})

services = []
visited_pages = 0
next_url = f"{base_url}/services?page=1"


try:
    # Rule 1: Terms must clearly allow automated access before scraping.
    terms_response = session.get(terms_url, timeout=10)

    terms_allow_access = (
        terms_response.status_code == 200
        and "Automated training access: allowed" in terms_response.text
    )

    if not terms_allow_access:
        raise SystemExit(
            "STOPPED: Terms do not clearly permit automated access."
        )

    # Rule 2: robots.txt must be accessible and verified.
    robots_response = session.get(robots_url, timeout=10)

    if robots_response.status_code != 200:
        raise SystemExit(
            "STOPPED: robots.txt could not be verified."
        )

    robot_parser = RobotFileParser()
    robot_parser.parse(robots_response.text.splitlines())

    user_agent = session.headers["User-Agent"]
    crawl_delay = robot_parser.crawl_delay(user_agent)

    if crawl_delay is None:
        crawl_delay = 1

    # Request structured metadata from the controlled REST API.
    api_response = session.get(api_url, timeout=10)

    if api_response.status_code != 200:
        raise SystemExit(
            "STOPPED: Directory API could not be accessed."
        )

    content_type = api_response.headers.get("Content-Type", "")

    if "application/json" not in content_type:
        raise SystemExit(
            "STOPPED: API did not return JSON."
        )

    api_data = api_response.json()

    if not api_data.get("active", False):
        raise SystemExit(
            "STOPPED: Community directory is inactive."
        )

    expected_records = int(api_data["expected_records"])
    recommendation_rating = float(
        api_data["minimum_recommended_rating"]
    )

    # requests.Session retains the cookie received from the API response.
    session_cookie = session.cookies.get("directory_session")

    if session_cookie != "training-approved":
        raise SystemExit(
            "STOPPED: Expected session cookie was not received."
        )

    print(f"API directory: {api_data['directory_name']}")
    print(f"API version: {api_data['api_version']}")
    print(f"Session cookie: {session_cookie}")

    # while continues until the current page has no next-page link.
    while next_url:
        if not robot_parser.can_fetch(user_agent, next_url):
            print(f"STOPPED BY ROBOTS.TXT: {next_url}")
            break

        response = session.get(next_url, timeout=10)

        if response.status_code in {403, 404, 503}:
            print(
                f"SAFE STOP: Status {response.status_code} "
                f"received from {next_url}"
            )
            break

        if response.status_code != 200:
            print(
                "SAFE STOP: Unexpected status "
                f"{response.status_code}"
            )
            break

        visited_pages += 1

        soup, page_services = extract_services(response.text)
        services.extend(page_services)

        next_link = soup.select_one("a.next-page")

        if next_link:
            # urljoin converts the relative href into a complete URL.
            next_url = urljoin(
                response.url,
                next_link.get("href")
            )
            time.sleep(crawl_delay)
        else:
            next_url = None

    # This verification belongs outside while so both pages finish first.
    if len(services) != expected_records:
        raise SystemExit(
            "STOPPED: Extracted record count does not match "
            "the API metadata."
        )

    print(
        "API record-count verification: "
        f"{len(services)}/{expected_records} PASS"
    )

finally:
    # finally runs even when the workflow stops, preventing resource leaks.
    session.close()
    server.shutdown()
    server.server_close()
    server_thread.join()


print(f"Pages processed: {visited_pages}")


# =============================================================================
# SECTION 6: MISSING-DATA AND DUPLICATE VALIDATION
# =============================================================================

(
    services,
    missing_record_count,
    duplicate_record_count
) = validate_services(services)


if len(services) != expected_records:
    raise SystemExit(
        "STOPPED: Validated record count does not match "
        "the API metadata."
    )


print("\nDATA QUALITY VERIFICATION")
print("-" * 30)
print(f"Missing records excluded: {missing_record_count}")
print(f"Duplicate records excluded: {duplicate_record_count}")
print(f"Validated records retained: {len(services)}")
print(
    "Validated record-count verification: "
    f"{len(services)}/{expected_records} PASS"
)


# =============================================================================
# SECTION 7: PYTHON DATA ANALYSIS
# =============================================================================

recommended_services = []

for service in services:
    if is_recommended(service, recommendation_rating):
        recommended_services.append(service)


# This list comprehension retains services with one or more open slots.
available_services = [
    service
    for service in services
    if service["available_slots"] > 0
]


total_available_slots = sum(
    service["available_slots"]
    for service in available_services
)


if available_services:
    average_rating = sum(
        service["rating"]
        for service in available_services
    ) / len(available_services)

    highest_rated_service = max(
        available_services,
        key=lambda service: service["rating"]
    )
else:
    average_rating = 0
    highest_rated_service = None


print("COMMUNITY SERVICE ANALYSIS")
print("-" * 30)
print(f"Total records: {len(services)}")
print(f"Available services: {len(available_services)}")
print(f"Total available slots: {total_available_slots}")
print(f"Average rating: {average_rating:.2f}")
print(
    "Recommended free services: "
    f"{len(recommended_services)}"
)

if highest_rated_service:
    print(
        "Highest-rated available service: "
        f"{highest_rated_service['name']} "
        f"({highest_rated_service['rating']})"
    )
else:
    print("Highest-rated available service: None")


print("\nRECOMMENDED SERVICES")

if recommended_services:
    for number, service in enumerate(
        recommended_services,
        start=1
    ):
        print(
            f"{number}. {service['name']} | "
            f"{service['category']} | "
            f"Rating: {service['rating']} | "
            f"Slots: {service['available_slots']}"
        )
else:
    print("No services meet all recommendation conditions.")


# =============================================================================
# SECTION 8: CSV, JSON, AND SQLITE STORAGE
# =============================================================================

# All outputs are saved beside this Python file.
output_directory = Path(__file__).resolve().parent

csv_path = output_directory / "day46_community_services.csv"
json_path = output_directory / "day46_community_services.json"
database_path = output_directory / "day46_community_services.db"


# -----------------------------
# 8A. SAVE DICTIONARIES TO CSV
# -----------------------------

csv_fields = [
    "name",
    "category",
    "rating",
    "available_slots",
    "is_free"
]

with csv_path.open(
    "w",
    newline="",
    encoding="utf-8"
) as csv_file:
    writer = csv.DictWriter(
        csv_file,
        fieldnames=csv_fields
    )
    writer.writeheader()
    writer.writerows(services)


# -----------------------------
# 8B. SAVE STRUCTURED JSON
# -----------------------------

with json_path.open(
    "w",
    encoding="utf-8"
) as json_file:
    json.dump(
        services,
        json_file,
        indent=4,
        ensure_ascii=False
    )


# -----------------------------
# 8C. SAVE RECORDS TO SQLITE
# -----------------------------

connection = sqlite3.connect(database_path)

try:
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS community_services (
            service_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            rating REAL NOT NULL,
            available_slots INTEGER NOT NULL,
            is_free INTEGER NOT NULL
        )
    """)

    # Clearing training rows makes repeated runs produce consistent results.
    cursor.execute("DELETE FROM community_services")

    insert_query = """
        INSERT INTO community_services (
            name,
            category,
            rating,
            available_slots,
            is_free
        )
        VALUES (?, ?, ?, ?, ?)
    """

    records_to_insert = [
        (
            service["name"],
            service["category"],
            service["rating"],
            service["available_slots"],
            int(service["is_free"])
        )
        for service in services
    ]

    # SQL ? placeholders pass values without building unsafe SQL strings.
    cursor.executemany(insert_query, records_to_insert)
    connection.commit()

    cursor.execute("""
        SELECT COUNT(*)
        FROM community_services
    """)
    database_record_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(available_slots), 0)
        FROM community_services
        WHERE available_slots > 0
    """)
    database_available_slots = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM community_services
        WHERE rating >= ?
          AND available_slots > 0
          AND is_free = 1
    """, (recommendation_rating,))
    database_recommended_count = cursor.fetchone()[0]

finally:
    connection.close()


# -----------------------------
# 8D. READ EXPORTS BACK
# -----------------------------

with csv_path.open(
    "r",
    encoding="utf-8"
) as csv_file:
    csv_records = list(csv.DictReader(csv_file))


with json_path.open(
    "r",
    encoding="utf-8"
) as json_file:
    json_records = json.load(json_file)


print("\nSTORAGE VERIFICATION")
print("-" * 30)
print(f"CSV records saved: {len(csv_records)}")
print(f"JSON records saved: {len(json_records)}")
print(f"SQLite records saved: {database_record_count}")
print(f"SQLite available slots: {database_available_slots}")
print(
    "SQLite recommended services: "
    f"{database_recommended_count}"
)
print(f"CSV file: {csv_path.name}")
print(f"JSON file: {json_path.name}")
print(f"SQLite database: {database_path.name}")


# =============================================================================
# SECTION 9: FINAL AUTOMATED VERIFICATION
# =============================================================================

verification_checks = [
    (
        "API directory is active",
        api_data.get("active") is True
    ),
    (
        "Session cookie verified",
        session_cookie == "training-approved"
    ),
    (
        "Two pages processed",
        visited_pages == 2
    ),
    (
        "Expected records extracted",
        len(services) == expected_records
    ),
    (
        "No missing records",
        missing_record_count == 0
    ),
    (
        "No duplicate records",
        duplicate_record_count == 0
    ),
    (
        "Five services available",
        len(available_services) == 5
    ),
    (
        "Available slots total is 29",
        total_available_slots == 29
    ),
    (
        "Three services recommended",
        len(recommended_services) == 3
    ),
    (
        "CSV contains six records",
        len(csv_records) == 6
    ),
    (
        "JSON contains six records",
        len(json_records) == 6
    ),
    (
        "SQLite contains six records",
        database_record_count == 6
    ),
    (
        "All output files exist",
        (
            csv_path.exists()
            and json_path.exists()
            and database_path.exists()
        )
    )
]


passed_checks = 0

print("\nFINAL COMPREHENSIVE VERIFICATION")
print("-" * 35)

for check_number, (description, result) in enumerate(
    verification_checks,
    start=1
):
    status = "PASS" if result else "FAIL"
    print(f"{check_number}. {description}: {status}")

    if result:
        passed_checks += 1


total_checks = len(verification_checks)

print("-" * 35)
print(
    "Final result: "
    f"{passed_checks}/{total_checks} checks passed"
)


if passed_checks == total_checks:
    print("DAY 46 PROGRAM VERIFICATION: PASS")
else:
    print("DAY 46 PROGRAM VERIFICATION: FAIL")


# =============================================================================
# DAY 46 CLOSING NOTES
# =============================================================================
#
# Main result:
#   One controlled program successfully combined scraping, policy checks,
#   sessions, cookies, pagination, API JSON, validation, analysis, exports,
#   SQLite, and automated verification.
#
# Debugging lesson:
#   - Code beneath an if statement must be indented inside its block.
#   - Pagination's next-link logic must remain inside the while loop.
#   - Record-count verification must run after the while loop.
#   - finally must align with try.
#   - Cleanup commands stay inside finally.
#   - Analysis code runs outside the complete try/finally structure.
#
# Day 46 is complete, but the final Phase 2 capstone/assessment and the exact
# Days 47-50 allocation remain unfinished. Comprehensive request-error
# handling, retry mechanisms, logging, and debugging remain deferred until the
# post-Day-50 recovery program.
