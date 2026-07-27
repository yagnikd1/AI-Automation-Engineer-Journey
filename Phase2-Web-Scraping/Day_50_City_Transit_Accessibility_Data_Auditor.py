
"""
Day 50 - City Transit Accessibility Data Auditor

GitHub-ready final study program for the AI Automation Engineer Journey.

Purpose:
Revise Python fundamentals and the complete Phase 2 web-scraping
workflow through one final integrated project.

Required third-party packages:
    pip install requests beautifulsoup4

Generated output directory:
    day50_transit_output
"""

import csv
import json
import re
import sqlite3
import threading
import time

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

# ---------------------------------------------------------
# 1. PROJECT CONFIGURATION
# ---------------------------------------------------------

PROJECT_NAME = "City Transit Accessibility Data Auditor"
BUILD_LABEL = "FINAL-VERIFIED-BUILD-2026-07-27"

OUTPUT_DIRECTORY = Path("day50_transit_output")

EXPECTED_PAGE_COUNT = 3
RECORDS_PER_PAGE = 3
EXPECTED_TOTAL_RECORDS = 9

REQUEST_TIMEOUT = 10
REQUEST_DELAY_SECONDS = 1

USER_AGENT = (
    "TransitAccessibilityTrainingBot/1.0 "
    "(educational local-data audit)"
)


# ---------------------------------------------------------
# 2. PYTHON COLLECTION REVISION
# ---------------------------------------------------------

REQUIRED_FIELDS = {
    "station_id",
    "station_name",
    "district",
    "status",
    "daily_passengers",
    "wheelchair_accessible",
}

ALLOWED_STATUSES = {
    "operational",
    "maintenance",
    "closed",
}

INVALID_TEXT_VALUES = {
    "",
    "none",
    "null",
    "unknown",
    "n/a",
}


# ---------------------------------------------------------
# 3. OUTPUT DIRECTORY
# ---------------------------------------------------------

def create_output_directory(directory: Path) -> None:
    """Create the output directory when it does not already exist."""

    directory.mkdir(parents=True, exist_ok=True)

    print(f"Output directory ready: {directory}")


# ---------------------------------------------------------
# 4. BASIC CLEANING FUNCTIONS
# ---------------------------------------------------------

def clean_text(value: object) -> str | None:
    """
    Convert a value into cleaned text.

    Return None when the value is missing or contains an accepted
    missing-value marker.
    """

    if value is None:
        return None

    cleaned_value = str(value).strip()

    if cleaned_value.lower() in INVALID_TEXT_VALUES:
        return None

    return cleaned_value


def clean_integer(value: object) -> int | None:
    """
    Convert strings such as '12,500 passengers' into integers.
    """

    cleaned_value = clean_text(value)

    if cleaned_value is None:
        return None

    number_match = re.search(
        r"[+-]?\d[\d,]*",
        cleaned_value,
    )

    if number_match is None:
        return None

    return int(number_match.group().replace(",", ""))


def clean_boolean(value: object) -> bool | None:
    """
    Convert common yes/no values into Boolean values.
    """

    cleaned_value = clean_text(value)

    if cleaned_value is None:
        return None

    normalized_value = cleaned_value.lower()

    if normalized_value in {"yes", "true", "1", "available"}:
        return True

    if normalized_value in {"no", "false", "0", "unavailable"}:
        return False

    return None


# ---------------------------------------------------------
# 5. FUNCTION TESTS
# ---------------------------------------------------------

def run_cleaning_examples() -> None:
    """Demonstrate and verify the cleaning functions."""

    sample_passenger_values = [
        "12,500 passengers",
        " 8300 ",
        "unknown",
        None,
    ]

    cleaned_passenger_values = [
        clean_integer(value)
        for value in sample_passenger_values
    ]

    sample_accessibility_values = [
        "Yes",
        "no",
        "AVAILABLE",
        "unknown",
    ]

    cleaned_accessibility_values = [
        clean_boolean(value)
        for value in sample_accessibility_values
    ]

    print("\nCleaning revision:")

    print(
        "Passenger values:",
        cleaned_passenger_values,
    )

    print(
        "Accessibility values:",
        cleaned_accessibility_values,
    )

    assert cleaned_passenger_values == [
        12500,
        8300,
        None,
        None,
    ]

    assert cleaned_accessibility_values == [
        True,
        False,
        True,
        None,
    ]

    print("Cleaning function checks: PASS")

# ---------------------------------------------------------
# 6. LOCAL PAGINATED WEBSITE DATA
# ---------------------------------------------------------

TRANSIT_PAGES = {
    1: [
        {
            "station_id": "ST-101",
            "station_name": "Central Exchange",
            "district": "Downtown",
            "status": "Operational",
            "daily_passengers": "12,500 passengers",
            "wheelchair_accessible": "Yes",
        },
        {
            "station_id": "ST-102",
            "station_name": "Harbor Point",
            "district": "Waterfront",
            "status": "Maintenance",
            "daily_passengers": "8,300 passengers",
            "wheelchair_accessible": "No",
        },
        {
            "station_id": "ST-103",
            "station_name": "North Park",
            "district": "North District",
            "status": "Operational",
            "daily_passengers": "6,750 passengers",
            "wheelchair_accessible": "Yes",
        },
    ],
    2: [
        {
            "station_id": "ST-104",
            "station_name": "Museum Square",
            "district": "Cultural District",
            "status": "Operational",
            "daily_passengers": "9,100 passengers",
            "wheelchair_accessible": "Yes",
        },
        {
            "station_id": "ST-105",
            "station_name": "West Market",
            "district": "West District",
            "status": "Closed",
            "daily_passengers": "4,200 passengers",
            "wheelchair_accessible": "No",
        },
        {
            "station_id": "ST-106",
            "station_name": "Airport Junction",
            "district": "Airport District",
            "status": "Operational",
            "daily_passengers": "15,600 passengers",
            "wheelchair_accessible": "Yes",
        },
    ],
    3: [
        {
            "station_id": "ST-107",
            "station_name": "University Gate",
            "district": "Education District",
            "status": "Operational",
            "daily_passengers": "7,400 passengers",
            "wheelchair_accessible": "Yes",
        },
        {
            "station_id": "ST-102",
            "station_name": "Harbor Point Duplicate",
            "district": "Waterfront",
            "status": "Maintenance",
            "daily_passengers": "8,300 passengers",
            "wheelchair_accessible": "No",
        },
        {
            "station_id": "ST-108",
            "station_name": "Incomplete Station",
            "district": "",
            "status": "Operational",
            "daily_passengers": "unknown",
            "wheelchair_accessible": "unknown",
        },
    ],
}

# ---------------------------------------------------------
# 7. LOCAL REST API DATA
# ---------------------------------------------------------

TRANSIT_API_RECORDS = [
    {
        "station_id": "ST-101",
        "station_name": "Central Exchange",
        "district": "Downtown",
        "status": "operational",
        "daily_passengers": 12500,
        "wheelchair_accessible": True,
    },
    {
        "station_id": "ST-102",
        "station_name": "Harbor Point",
        "district": "Waterfront",
        "status": "maintenance",
        "daily_passengers": 8300,
        "wheelchair_accessible": False,
    },
    {
        "station_id": "ST-103",
        "station_name": "North Park",
        "district": "North District",
        "status": "operational",
        "daily_passengers": 6750,
        "wheelchair_accessible": True,
    },
    {
        "station_id": "ST-104",
        "station_name": "Museum Square",
        "district": "Cultural District",
        "status": "operational",
        "daily_passengers": 9100,
        "wheelchair_accessible": True,
    },
    {
        "station_id": "ST-105",
        "station_name": "West Market",
        "district": "West District",
        "status": "closed",
        "daily_passengers": 4200,
        "wheelchair_accessible": False,
    },
    {
        "station_id": "ST-106",
        "station_name": "Airport Junction",
        "district": "Airport District",
        "status": "operational",
        "daily_passengers": 15600,
        "wheelchair_accessible": True,
    },
    {
        "station_id": "ST-107",
        "station_name": "University Gate",
        "district": "Education District",
        "status": "operational",
        "daily_passengers": 7400,
        "wheelchair_accessible": True,
    },
]

EXPECTED_API_RECORD_COUNT = 7

# ---------------------------------------------------------
# 8. LOCAL HTML GENERATION
# ---------------------------------------------------------

def create_station_card(station: dict[str, str]) -> str:
    """Convert one station dictionary into an HTML article."""

    return f"""
    <article class="station-card"
             data-station-id="{station['station_id']}">

        <h2 class="station-name">
            {station['station_name']}
        </h2>

        <p class="district">
            {station['district']}
        </p>

        <span class="status">
            {station['status']}
        </span>

        <span class="daily-passengers">
            {station['daily_passengers']}
        </span>

        <span class="wheelchair-accessible">
            {station['wheelchair_accessible']}
        </span>
    </article>
    """


def create_transit_page(page_number: int) -> str:
    """Create one complete paginated HTML page."""

    station_cards = [
        create_station_card(station)
        for station in TRANSIT_PAGES[page_number]
    ]

    cards_html = "\n".join(station_cards)

    next_page_html = ""

    if page_number < EXPECTED_PAGE_COUNT:
        next_page_html = (
            f'<a class="next-page" '
            f'href="/transit?page={page_number + 1}">'
            f"Next page</a>"
        )

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>City Transit Directory</title>
    </head>
    <body>
        <main id="transit-directory">
            <h1>City Transit Stations</h1>

            <p class="page-number">
                Page {page_number}
            </p>

            <section class="station-list">
                {cards_html}
            </section>

            {next_page_html}
        </main>
    </body>
    </html>
    """


# ---------------------------------------------------------
# 9. LOCAL TRAINING SERVER
# ---------------------------------------------------------

class TransitTrainingHandler(BaseHTTPRequestHandler):
    """Serve the local transit website and robots.txt."""

    def log_message(self, format: str, *args: object) -> None:
        """Disable the default local-server request messages."""

    def send_text_response(
        self,
        status_code: int,
        content: str,
        content_type: str,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        """Send a text response with the required headers."""

        encoded_content = content.encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header(
            "Content-Length",
            str(len(encoded_content)),
        )

        if extra_headers:
            for header_name, header_value in extra_headers.items():
                self.send_header(header_name, header_value)

        self.end_headers()
        self.wfile.write(encoded_content)

    def do_GET(self) -> None:
        """Handle GET requests sent to the training server."""

        parsed_url = urlparse(self.path)

        if parsed_url.path == "/robots.txt":
            robots_content = (
                "User-agent: *\n"
                "Allow: /transit\n"
                "Allow: /api/transit\n"
                "Disallow: /private\n"
                f"Crawl-delay: {REQUEST_DELAY_SECONDS}\n"
            )

            self.send_text_response(
                200,
                robots_content,
                "text/plain; charset=utf-8",
            )
            return

        if parsed_url.path == "/":
            landing_page = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Transit Training Access</title>
            </head>
            <body>
                <h1>Training access approved</h1>
            </body>
            </html>
            """

            self.send_text_response(
                200,
                landing_page,
                "text/html; charset=utf-8",
                {
                    "Set-Cookie": (
                        "training_access=approved; "
                        "Path=/; SameSite=Lax"
                    )
                },
            )
            return

        if parsed_url.path == "/api/transit":
            cookie_header = self.headers.get("Cookie", "")

            if "training_access=approved" not in cookie_header:
                self.send_text_response(
                    403,
                    json.dumps(
                        {
                            "error": "Training cookie required."
                        }
                    ),
                    "application/json; charset=utf-8",
                )
                return

            query_values = parse_qs(parsed_url.query)
            limit_values = query_values.get(
                "limit",
                [str(EXPECTED_API_RECORD_COUNT)],
            )

            try:
                requested_limit = int(limit_values[0])
            except ValueError:
                self.send_text_response(
                    400,
                    json.dumps(
                        {
                            "error": "Invalid limit value."
                        }
                    ),
                    "application/json; charset=utf-8",
                )
                return

            if requested_limit < 1:
                self.send_text_response(
                    400,
                    json.dumps(
                        {
                            "error": (
                                "Limit must be greater than zero."
                            )
                        }
                    ),
                    "application/json; charset=utf-8",
                )
                return

            selected_records = TRANSIT_API_RECORDS[
                :requested_limit
            ]

            api_payload = {
                "api_name": (
                    "City Transit Accessibility API"
                ),
                "version": "1.0",
                "count": len(selected_records),
                "results": selected_records,
            }

            self.send_text_response(
                200,
                json.dumps(api_payload),
                "application/json; charset=utf-8",
            )
            return

        if parsed_url.path == "/transit":
            cookie_header = self.headers.get("Cookie", "")

            if "training_access=approved" not in cookie_header:
                self.send_text_response(
                    403,
                    "Training cookie required.",
                    "text/plain; charset=utf-8",
                )
                return

            query_values = parse_qs(parsed_url.query)
            page_values = query_values.get("page", ["1"])

            try:
                page_number = int(page_values[0])
            except ValueError:
                self.send_text_response(
                    400,
                    "Invalid page number.",
                    "text/plain; charset=utf-8",
                )
                return

            if page_number not in TRANSIT_PAGES:
                self.send_text_response(
                    404,
                    "Transit page not found.",
                    "text/plain; charset=utf-8",
                )
                return

            self.send_text_response(
                200,
                create_transit_page(page_number),
                "text/html; charset=utf-8",
            )
            return

        self.send_text_response(
            404,
            "Resource not found.",
            "text/plain; charset=utf-8",
        )


def start_training_server() -> tuple[
    ThreadingHTTPServer,
    threading.Thread,
    str,
]:
    """Start the local website on an automatically selected port."""

    server = ThreadingHTTPServer(
        ("127.0.0.1", 0),
        TransitTrainingHandler,
    )

    server_thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )

    server_thread.start()

    host = str(server.server_address[0])
    port = int(server.server_address[1])
    base_url = f"http://{host}:{port}"

    return server, server_thread, base_url

# ---------------------------------------------------------
# 10. POLICY, SESSION, COOKIE, AND PAGINATION REVISION
# ---------------------------------------------------------

def collect_paginated_html(base_url: str) -> list[str]:
    """
    Check robots.txt and collect every permitted transit page.

    Stop immediately when policy or request verification fails.
    """

    session = requests.Session()

    try:
        session.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml",
            }
        )

        landing_response = session.get(
            f"{base_url}/",
            timeout=REQUEST_TIMEOUT,
        )

        if landing_response.status_code != 200:
            raise RuntimeError(
                "STOP: Training access page was unavailable."
            )

        session_cookie = session.cookies.get("training_access")

        if session_cookie != "approved":
            raise RuntimeError(
                "STOP: Required session cookie was not received."
            )

        print("\nSession revision:")
        print("Training access status:", landing_response.status_code)
        print("Session cookie:", session_cookie)

        robots_parser = RobotFileParser()
        robots_parser.set_url(f"{base_url}/robots.txt")
        robots_parser.read()

        first_page_url = f"{base_url}/transit?page=1"

        robots_allowed = robots_parser.can_fetch(
            USER_AGENT,
            first_page_url,
        )

        crawl_delay = robots_parser.crawl_delay(USER_AGENT)

        if crawl_delay is None:
            crawl_delay = robots_parser.crawl_delay("*")

        effective_delay = float(
            crawl_delay
            if crawl_delay is not None
            else REQUEST_DELAY_SECONDS
        )

        print("\nPolicy revision:")
        print("robots.txt permission:", robots_allowed)
        print("Required crawl delay:", crawl_delay)

        if not robots_allowed:
            raise RuntimeError(
                "STOP: robots.txt does not permit collection."
            )

        collected_pages: list[str] = []
        current_page_url: str | None = first_page_url
        page_number = 1

        while current_page_url is not None:
            if page_number > 1:
                time.sleep(effective_delay)

            print(
                f"Requesting transit page "
                f"{page_number}/{EXPECTED_PAGE_COUNT}..."
            )

            response = session.get(
                current_page_url,
                timeout=REQUEST_TIMEOUT,
            )

            if response.status_code != 200:
                raise RuntimeError(
                    "STOP: Transit page request failed with "
                    f"status {response.status_code}."
                )

            collected_pages.append(response.text)

            soup = BeautifulSoup(response.text, "html.parser")
            next_page_link = soup.select_one("a.next-page")

            if next_page_link is None:
                current_page_url = None
            else:
                next_page_path = next_page_link.get("href")

                if not isinstance(next_page_path, str):
                    raise RuntimeError(
                        "STOP: Next-page URL is missing."
                    )

                current_page_url = f"{base_url}{next_page_path}"

                if not robots_parser.can_fetch(
                    USER_AGENT,
                    current_page_url,
                ):
                    raise RuntimeError(
                        "STOP: robots.txt denied the next page."
                    )

            print(
                "Page collected successfully. "
                f"Total pages: {len(collected_pages)}"
            )

            page_number += 1

        if len(collected_pages) != EXPECTED_PAGE_COUNT:
            raise RuntimeError(
                "STOP: Collected page count does not match "
                "the expected page count."
            )

        print("Paginated HTML collection check: PASS")

        return collected_pages

    finally:
        session.close()

# ---------------------------------------------------------
# 11. HTML PARSING REVISION
# ---------------------------------------------------------

def extract_element_text(element: Tag | None) -> str | None:
    """Safely extract cleaned text from a BeautifulSoup element."""

    if element is None:
        return None

    return clean_text(element.get_text(" ", strip=True))


def parse_station_card(station_card: Tag) -> dict[str, Any]:
    """
    Extract and clean one station card.

    This deliberately revises find(), select_one(), text extraction,
    attribute extraction, and missing-element handling.
    """

    station_name_element = station_card.select_one(
        "h2.station-name"
    )

    district_element = station_card.find(
        "p",
        class_="district",
    )

    status_element = station_card.select_one(
        "span.status"
    )

    passenger_element = station_card.find(
        "span",
        class_="daily-passengers",
    )

    accessibility_element = station_card.select_one(
        "span.wheelchair-accessible"
    )

    station_id = clean_text(
        station_card.get("data-station-id")
    )

    station_name = extract_element_text(
        station_name_element
    )

    district = extract_element_text(
        district_element
    )

    status = extract_element_text(
        status_element
    )

    if status is not None:
        status = status.lower()

    daily_passengers = clean_integer(
        extract_element_text(passenger_element)
    )

    wheelchair_accessible = clean_boolean(
        extract_element_text(accessibility_element)
    )

    return {
        "station_id": station_id,
        "station_name": station_name,
        "district": district,
        "status": status,
        "daily_passengers": daily_passengers,
        "wheelchair_accessible": wheelchair_accessible,
    }


def parse_html_pages(
    collected_pages: list[str],
) -> list[dict[str, Any]]:
    """Parse all station cards from the collected HTML pages."""

    parsed_records: list[dict[str, Any]] = []

    for page_position, html_page in enumerate(
        collected_pages,
        start=1,
    ):
        soup = BeautifulSoup(
            html_page,
            "html.parser",
        )

        directory = soup.find(
            "main",
            id="transit-directory",
        )

        if directory is None:
            raise RuntimeError(
                "STOP: Transit directory container is missing "
                f"from page {page_position}."
            )

        station_section = directory.find(
            "section",
            class_="station-list",
        )

        if station_section is None:
            raise RuntimeError(
                "STOP: Station-list section is missing "
                f"from page {page_position}."
            )

        station_cards = station_section.find_all(
            "article",
            class_="station-card",
        )

        print(
            f"Parsing page {page_position}: "
            f"{len(station_cards)} station cards found"
        )

        if len(station_cards) != RECORDS_PER_PAGE:
            raise RuntimeError(
                "STOP: Unexpected number of station cards "
                f"on page {page_position}."
            )

        page_records = [
            parse_station_card(station_card)
            for station_card in station_cards
        ]

        parsed_records.extend(page_records)

    print(
        "Total raw station records parsed:",
        len(parsed_records),
    )

    if len(parsed_records) != EXPECTED_TOTAL_RECORDS:
        raise RuntimeError(
            "STOP: Parsed record count does not match "
            "the expected total."
        )

    print("HTML parsing count check: PASS")

    return parsed_records

# ---------------------------------------------------------
# 12. VALIDATION AND AUDIT REVISION
# ---------------------------------------------------------

def validate_station_record(
    record: dict[str, Any],
) -> list[str]:
    """Return every validation problem found in one record."""

    validation_errors: list[str] = []

    missing_fields = [
        field_name
        for field_name in REQUIRED_FIELDS
        if record.get(field_name) is None
    ]

    if missing_fields:
        validation_errors.append(
            "Missing required fields: "
            + ", ".join(sorted(missing_fields))
        )

    status = record.get("status")

    if (
        status is not None
        and status not in ALLOWED_STATUSES
    ):
        validation_errors.append(
            f"Unsupported status: {status}"
        )

    passenger_count = record.get(
        "daily_passengers"
    )

    if (
        isinstance(passenger_count, int)
        and passenger_count < 0
    ):
        validation_errors.append(
            "Daily passenger count cannot be negative."
        )

    accessibility = record.get(
        "wheelchair_accessible"
    )

    if (
        accessibility is not None
        and not isinstance(accessibility, bool)
    ):
        validation_errors.append(
            "Accessibility value must be Boolean."
        )

    return validation_errors


def audit_station_records(
    parsed_records: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    """
    Separate records into valid, invalid, and duplicate groups.

    Station IDs are used as the unique identity.
    """

    valid_records: list[dict[str, Any]] = []
    invalid_records: list[dict[str, Any]] = []
    duplicate_records: list[dict[str, Any]] = []

    seen_station_ids: set[str] = set()

    for record in parsed_records:
        station_id = record.get("station_id")

        if (
            isinstance(station_id, str)
            and station_id in seen_station_ids
        ):
            duplicate_entry = {
                "record": record,
                "reason": (
                    "Duplicate station_id: "
                    f"{station_id}"
                ),
            }

            duplicate_records.append(
                duplicate_entry
            )

            continue

        validation_errors = validate_station_record(
            record
        )

        if validation_errors:
            invalid_entry = {
                "record": record,
                "errors": validation_errors,
            }

            invalid_records.append(invalid_entry)

            continue

        if not isinstance(station_id, str):
            raise RuntimeError(
                "STOP: Valid record has no usable station ID."
            )

        seen_station_ids.add(station_id)
        valid_records.append(record)

    return (
        valid_records,
        invalid_records,
        duplicate_records,
    )


def verify_audit_results(
    parsed_records: list[dict[str, Any]],
    valid_records: list[dict[str, Any]],
    invalid_records: list[dict[str, Any]],
    duplicate_records: list[dict[str, Any]],
) -> None:
    """Verify the expected record classifications."""

    classified_total = (
        len(valid_records)
        + len(invalid_records)
        + len(duplicate_records)
    )

    checks = {
        "raw_record_count": (
            len(parsed_records)
            == EXPECTED_TOTAL_RECORDS
        ),
        "classification_total": (
            classified_total
            == EXPECTED_TOTAL_RECORDS
        ),
        "valid_unique_count": (
            len(valid_records) == 7
        ),
        "invalid_count": (
            len(invalid_records) == 1
        ),
        "duplicate_count": (
            len(duplicate_records) == 1
        ),
        "unique_valid_ids": (
            len(
                {
                    record["station_id"]
                    for record in valid_records
                }
            )
            == len(valid_records)
        ),
    }

    failed_checks = [
        check_name
        for check_name, passed in checks.items()
        if not passed
    ]

    for check_name, passed in checks.items():
        result = "PASS" if passed else "FAIL"
        print(f"{check_name}: {result}")

    if failed_checks:
        raise RuntimeError(
            "STOP: Audit verification failed: "
            + ", ".join(failed_checks)
        )

    print("Station audit verification: PASS")


# ---------------------------------------------------------
# 13. REST API AND JSON REVISION
# ---------------------------------------------------------

def collect_transit_api(
    base_url: str,
) -> list[dict[str, Any]]:
    """Collect and verify the local REST API records."""

    session = requests.Session()

    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        }
    )

    try:
        access_response = session.get(
            f"{base_url}/",
            timeout=REQUEST_TIMEOUT,
        )

        if access_response.status_code != 200:
            raise RuntimeError(
                "STOP: API training access failed."
            )

        if (
            session.cookies.get("training_access")
            != "approved"
        ):
            raise RuntimeError(
                "STOP: API session cookie is missing."
            )

        api_url = (
            f"{base_url}/api/transit"
            f"?limit={EXPECTED_API_RECORD_COUNT}"
        )

        robots_parser = RobotFileParser()
        robots_parser.set_url(
            f"{base_url}/robots.txt"
        )
        robots_parser.read()

        if not robots_parser.can_fetch(
            USER_AGENT,
            api_url,
        ):
            raise RuntimeError(
                "STOP: robots.txt denied API access."
            )

        response = session.get(
            api_url,
            timeout=REQUEST_TIMEOUT,
        )

        print("\nREST API revision:")
        print("API response status:", response.status_code)
        print(
            "API content type:",
            response.headers.get("Content-Type"),
        )

        if response.status_code != 200:
            raise RuntimeError(
                "STOP: API request failed with status "
                f"{response.status_code}."
            )

        try:
            payload = response.json()
        except requests.exceptions.JSONDecodeError as error:
            raise RuntimeError(
                "STOP: API response was not valid JSON."
            ) from error

        if not isinstance(payload, dict):
            raise RuntimeError(
                "STOP: API payload must be a JSON object."
            )

        api_name = payload.get("api_name")
        api_version = payload.get("version")
        declared_count = payload.get("count")
        api_records = payload.get("results")

        if not isinstance(api_records, list):
            raise RuntimeError(
                "STOP: API results must be a list."
            )

        print("API name:", api_name)
        print("API version:", api_version)
        print("Declared record count:", declared_count)
        print("Received record count:", len(api_records))

        if declared_count != len(api_records):
            raise RuntimeError(
                "STOP: API declared count does not match "
                "the received result count."
            )

        if len(api_records) != EXPECTED_API_RECORD_COUNT:
            raise RuntimeError(
                "STOP: API record count does not match "
                "the expected count."
            )

        print("REST API count verification: PASS")

        return api_records

    finally:
        session.close()


# ---------------------------------------------------------
# 14. CROSS-SOURCE VERIFICATION
# ---------------------------------------------------------

def compare_html_and_api_records(
    html_records: list[dict[str, Any]],
    api_records: list[dict[str, Any]],
) -> None:
    """Verify that HTML and API records contain matching data."""

    html_by_id = {
        str(record["station_id"]): record
        for record in html_records
    }

    api_by_id = {
        str(record["station_id"]): record
        for record in api_records
    }

    print("\nCross-source verification:")

    checks = {
        "matching_station_ids": (
            set(html_by_id) == set(api_by_id)
        ),
        "matching_record_counts": (
            len(html_records) == len(api_records)
        ),
        "matching_names": all(
            html_by_id[station_id]["station_name"]
            == api_by_id[station_id]["station_name"]
            for station_id in html_by_id
            if station_id in api_by_id
        ),
        "matching_statuses": all(
            html_by_id[station_id]["status"]
            == api_by_id[station_id]["status"]
            for station_id in html_by_id
            if station_id in api_by_id
        ),
        "matching_passenger_counts": all(
            html_by_id[station_id]["daily_passengers"]
            == api_by_id[station_id]["daily_passengers"]
            for station_id in html_by_id
            if station_id in api_by_id
        ),
        "matching_accessibility": all(
            html_by_id[station_id][
                "wheelchair_accessible"
            ]
            == api_by_id[station_id][
                "wheelchair_accessible"
            ]
            for station_id in html_by_id
            if station_id in api_by_id
        ),
    }

    failed_checks = []

    for check_name, passed in checks.items():
        result = "PASS" if passed else "FAIL"
        print(f"{check_name}: {result}")

        if not passed:
            failed_checks.append(check_name)

    if failed_checks:
        raise RuntimeError(
            "STOP: Cross-source verification failed: "
            + ", ".join(failed_checks)
        )

    print("HTML and API consistency check: PASS")


# ---------------------------------------------------------
# 15. DATA ANALYSIS REVISION
# ---------------------------------------------------------

def analyze_transit_records(
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    """Calculate accessibility and passenger statistics."""

    if not records:
        raise ValueError(
            "Transit analysis requires at least one valid record."
        )

    operational_records = [
        record
        for record in records
        if record["status"] == "operational"
    ]

    accessible_records = [
        record
        for record in records
        if record["wheelchair_accessible"] is True
    ]

    total_passengers = sum(
        int(record["daily_passengers"])
        for record in records
    )

    average_passengers = (
        total_passengers / len(records)
        if records
        else 0
    )

    accessibility_rate = (
        len(accessible_records) / len(records) * 100
        if records
        else 0
    )

    busiest_station = max(
        records,
        key=lambda record: int(
            record["daily_passengers"]
        ),
    )

    stations_by_passengers = sorted(
        records,
        key=lambda record: int(
            record["daily_passengers"]
        ),
        reverse=True,
    )

    analysis = {
        "total_stations": len(records),
        "operational_stations": len(
            operational_records
        ),
        "accessible_stations": len(
            accessible_records
        ),
        "accessibility_rate": round(
            accessibility_rate,
            2,
        ),
        "total_daily_passengers": total_passengers,
        "average_daily_passengers": round(
            average_passengers,
            2,
        ),
        "busiest_station": (
            busiest_station["station_name"]
        ),
        "busiest_station_passengers": (
            busiest_station["daily_passengers"]
        ),
        "station_ranking": [
            {
                "position": position,
                "station_id": record["station_id"],
                "station_name": record["station_name"],
                "daily_passengers": (
                    record["daily_passengers"]
                ),
            }
            for position, record in enumerate(
                stations_by_passengers,
                start=1,
            )
        ],
    }

    return analysis


def verify_analysis(
    analysis: dict[str, Any],
) -> None:
    """Verify the known analysis results."""

    checks = {
        "total_stations": (
            analysis["total_stations"] == 7
        ),
        "operational_stations": (
            analysis["operational_stations"] == 5
        ),
        "accessible_stations": (
            analysis["accessible_stations"] == 5
        ),
        "accessibility_rate": (
            analysis["accessibility_rate"] == 71.43
        ),
        "total_daily_passengers": (
            analysis["total_daily_passengers"]
            == 63850
        ),
        "average_daily_passengers": (
            analysis["average_daily_passengers"]
            == 9121.43
        ),
        "busiest_station": (
            analysis["busiest_station"]
            == "Airport Junction"
        ),
        "busiest_station_passengers": (
            analysis["busiest_station_passengers"]
            == 15600
        ),
    }

    failed_checks = []

    print("\nAnalysis verification:")

    for check_name, passed in checks.items():
        result = "PASS" if passed else "FAIL"
        print(f"{check_name}: {result}")

        if not passed:
            failed_checks.append(check_name)

    if failed_checks:
        raise RuntimeError(
            "STOP: Analysis verification failed: "
            + ", ".join(failed_checks)
        )

    print("Transit analysis verification: PASS")


# ---------------------------------------------------------
# 16. CSV, JSON, AND SQLITE STORAGE
# ---------------------------------------------------------

def save_valid_records_to_csv(
    records: list[dict[str, Any]],
    output_directory: Path,
) -> Path:
    """Save valid station records to a CSV file."""

    csv_path = output_directory / "valid_transit_stations.csv"
    fieldnames = [
        "station_id",
        "station_name",
        "district",
        "status",
        "daily_passengers",
        "wheelchair_accessible",
    ]

    with csv_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(records)

    return csv_path


def save_audit_to_json(
    valid_records: list[dict[str, Any]],
    invalid_records: list[dict[str, Any]],
    duplicate_records: list[dict[str, Any]],
    analysis: dict[str, Any],
    output_directory: Path,
) -> Path:
    """Save the complete audit evidence to a JSON file."""

    json_path = output_directory / "transit_audit.json"
    audit_payload = {
        "project_name": PROJECT_NAME,
        "summary": {
            "valid_unique_records": len(valid_records),
            "invalid_records": len(invalid_records),
            "duplicate_records": len(duplicate_records),
        },
        "analysis": analysis,
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "duplicate_records": duplicate_records,
    }

    with json_path.open(
        "w",
        encoding="utf-8",
    ) as json_file:
        json.dump(
            audit_payload,
            json_file,
            indent=4,
            ensure_ascii=False,
        )

    return json_path


def save_valid_records_to_sqlite(
    records: list[dict[str, Any]],
    output_directory: Path,
) -> Path:
    """Replace the SQLite station table with verified records."""

    database_path = output_directory / "transit_audit.db"

    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transit_stations (
                station_id TEXT PRIMARY KEY,
                station_name TEXT NOT NULL,
                district TEXT NOT NULL,
                status TEXT NOT NULL,
                daily_passengers INTEGER NOT NULL
                    CHECK (daily_passengers >= 0),
                wheelchair_accessible INTEGER NOT NULL
                    CHECK (wheelchair_accessible IN (0, 1))
            )
            """
        )

        cursor.execute("DELETE FROM transit_stations")

        cursor.executemany(
            """
            INSERT INTO transit_stations (
                station_id,
                station_name,
                district,
                status,
                daily_passengers,
                wheelchair_accessible
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    record["station_id"],
                    record["station_name"],
                    record["district"],
                    record["status"],
                    record["daily_passengers"],
                    int(record["wheelchair_accessible"]),
                )
                for record in records
            ],
        )

        connection.commit()

    return database_path


def verify_saved_outputs(
    csv_path: Path,
    json_path: Path,
    database_path: Path,
    expected_record_count: int,
) -> None:
    """Read all saved formats back and verify their record counts."""

    with csv_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as csv_file:
        csv_count = sum(
            1
            for _ in csv.DictReader(csv_file)
        )

    with json_path.open(
        "r",
        encoding="utf-8",
    ) as json_file:
        saved_audit = json.load(json_file)

    json_count = len(saved_audit["valid_records"])

    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM transit_stations"
        )
        sqlite_result = cursor.fetchone()

    sqlite_count = (
        int(sqlite_result[0])
        if sqlite_result is not None
        else 0
    )

    checks = {
        "csv_record_count": (
            csv_count == expected_record_count
        ),
        "json_record_count": (
            json_count == expected_record_count
        ),
        "sqlite_record_count": (
            sqlite_count == expected_record_count
        ),
        "cross_format_counts": (
            csv_count == json_count == sqlite_count
        ),
    }

    print("\nSaved-output verification:")

    failed_checks = []

    for check_name, passed in checks.items():
        result = "PASS" if passed else "FAIL"
        print(f"{check_name}: {result}")

        if not passed:
            failed_checks.append(check_name)

    if failed_checks:
        raise RuntimeError(
            "STOP: Saved-output verification failed: "
            + ", ".join(failed_checks)
        )

    print("Cross-format storage verification: PASS")


# ---------------------------------------------------------
# 17. TEXT REPORT GENERATION
# ---------------------------------------------------------

def create_text_report(
    valid_records: list[dict[str, Any]],
    invalid_records: list[dict[str, Any]],
    duplicate_records: list[dict[str, Any]],
    analysis: dict[str, Any],
    output_directory: Path,
) -> Path:
    """Create a readable summary of the completed transit audit."""

    report_path = output_directory / "transit_audit_report.txt"

    report_lines = [
        PROJECT_NAME,
        "=" * len(PROJECT_NAME),
        "",
        "AUDIT SUMMARY",
        f"Valid unique stations: {len(valid_records)}",
        f"Invalid records: {len(invalid_records)}",
        f"Duplicate records: {len(duplicate_records)}",
        "",
        "ACCESSIBILITY AND PASSENGER ANALYSIS",
        f"Total stations: {analysis['total_stations']}",
        (
            "Operational stations: "
            f"{analysis['operational_stations']}"
        ),
        (
            "Wheelchair-accessible stations: "
            f"{analysis['accessible_stations']}"
        ),
        (
            "Accessibility rate: "
            f"{analysis['accessibility_rate']:.2f}%"
        ),
        (
            "Total daily passengers: "
            f"{analysis['total_daily_passengers']}"
        ),
        (
            "Average daily passengers: "
            f"{analysis['average_daily_passengers']:.2f}"
        ),
        (
            "Busiest station: "
            f"{analysis['busiest_station']} "
            f"({analysis['busiest_station_passengers']} passengers)"
        ),
        "",
        "PASSENGER RANKING",
    ]

    for ranked_station in analysis["station_ranking"]:
        report_lines.append(
            f"{ranked_station['position']}. "
            f"{ranked_station['station_name']} — "
            f"{ranked_station['daily_passengers']}"
        )

    report_lines.extend(
        [
            "",
            "DATA-QUALITY FINDINGS",
        ]
    )

    for invalid_entry in invalid_records:
        invalid_record = invalid_entry["record"]
        report_lines.append(
            "Invalid record: "
            f"{invalid_record.get('station_name')} — "
            + "; ".join(invalid_entry["errors"])
        )

    for duplicate_entry in duplicate_records:
        duplicate_record = duplicate_entry["record"]
        report_lines.append(
            "Duplicate record: "
            f"{duplicate_record.get('station_id')} — "
            f"{duplicate_record.get('station_name')}"
        )

    report_lines.extend(
        [
            "",
            "FINAL STATUS",
            "HTML and REST API consistency: PASS",
            "CSV, JSON, and SQLite storage consistency: PASS",
            "City transit accessibility audit: PASS",
        ]
    )

    report_path.write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    return report_path


# ---------------------------------------------------------
# 18. FINAL END-TO-END VERIFICATION
# ---------------------------------------------------------

def verify_final_project(
    collected_pages: list[str],
    parsed_records: list[dict[str, Any]],
    valid_records: list[dict[str, Any]],
    invalid_records: list[dict[str, Any]],
    duplicate_records: list[dict[str, Any]],
    api_records: list[dict[str, Any]],
    analysis: dict[str, Any],
    csv_path: Path,
    json_path: Path,
    database_path: Path,
    report_path: Path,
) -> None:
    """Independently verify the completed integrated project."""

    report_text = report_path.read_text(encoding="utf-8")

    output_paths = [
        csv_path,
        json_path,
        database_path,
        report_path,
    ]

    checks = {
        "html_page_count": (
            len(collected_pages) == EXPECTED_PAGE_COUNT
        ),
        "raw_record_count": (
            len(parsed_records) == EXPECTED_TOTAL_RECORDS
        ),
        "valid_unique_count": (
            len(valid_records) == 7
        ),
        "invalid_count": (
            len(invalid_records) == 1
        ),
        "duplicate_count": (
            len(duplicate_records) == 1
        ),
        "api_record_count": (
            len(api_records) == EXPECTED_API_RECORD_COUNT
        ),
        "analysis_total_stations": (
            analysis["total_stations"] == len(valid_records)
        ),
        "all_output_files_exist": all(
            path.is_file()
            for path in output_paths
        ),
        "all_output_files_nonempty": all(
            path.stat().st_size > 0
            for path in output_paths
            if path.is_file()
        ) and len(output_paths) == sum(
            path.is_file()
            for path in output_paths
        ),
        "report_project_name": (
            PROJECT_NAME in report_text
        ),
        "report_busiest_station": (
            "Busiest station: Airport Junction "
            "(15600 passengers)"
            in report_text
        ),
        "report_final_status": (
            "City transit accessibility audit: PASS"
            in report_text
        ),
    }

    print("\nFinal end-to-end verification:")

    failed_checks = []

    for check_name, passed in checks.items():
        result = "PASS" if passed else "FAIL"
        print(f"{check_name}: {result}")

        if not passed:
            failed_checks.append(check_name)

    if failed_checks:
        raise RuntimeError(
            "STOP: Final project verification failed: "
            + ", ".join(failed_checks)
        )

    print("Final end-to-end verification: PASS")


# ---------------------------------------------------------
# 19. MAIN PROGRAM
# ---------------------------------------------------------

def main() -> None:
    """Run the Day 50 transit accessibility auditor."""

    print(f"Starting {PROJECT_NAME}...")
    print("Program build:", BUILD_LABEL)

    create_output_directory(OUTPUT_DIRECTORY)
    run_cleaning_examples()

    server, server_thread, base_url = start_training_server()

    print("\nLocal training website started.")
    print("Local base URL:", base_url)

    try:
        collected_pages = collect_paginated_html(base_url)

        print("\nHTML parsing revision:")
        parsed_records = parse_html_pages(collected_pages)

        (
            valid_records,
            invalid_records,
            duplicate_records,
        ) = audit_station_records(parsed_records)

        print("\nStation audit results:")
        print("Raw records:", len(parsed_records))
        print("Valid unique records:", len(valid_records))
        print("Invalid records:", len(invalid_records))
        print("Duplicate records:", len(duplicate_records))

        if invalid_records:
            print(
                "Invalid station:",
                invalid_records[0]["record"]["station_name"],
            )
            print(
                "Invalid reasons:",
                invalid_records[0]["errors"],
            )

        if duplicate_records:
            print(
                "Duplicate station ID:",
                duplicate_records[0]["record"]["station_id"],
            )

        print("\nStation audit verification:")
        verify_audit_results(
            parsed_records,
            valid_records,
            invalid_records,
            duplicate_records,
        )

        api_records = collect_transit_api(base_url)

        compare_html_and_api_records(
            valid_records,
            api_records,
        )

        analysis = analyze_transit_records(valid_records)

        print("\nTransit analysis results:")
        print("Total stations:", analysis["total_stations"])
        print(
            "Operational stations:",
            analysis["operational_stations"],
        )
        print(
            "Wheelchair-accessible stations:",
            analysis["accessible_stations"],
        )
        print(
            "Accessibility rate:",
            f"{analysis['accessibility_rate']:.2f}%",
        )
        print(
            "Total daily passengers:",
            analysis["total_daily_passengers"],
        )
        print(
            "Average daily passengers:",
            f"{analysis['average_daily_passengers']:.2f}",
        )
        print(
            "Busiest station:",
            analysis["busiest_station"],
        )
        print(
            "Busiest station passengers:",
            analysis["busiest_station_passengers"],
        )

        print("\nPassenger ranking:")

        for ranked_station in analysis["station_ranking"]:
            print(
                f"{ranked_station['position']}. "
                f"{ranked_station['station_name']} — "
                f"{ranked_station['daily_passengers']}"
            )

        verify_analysis(analysis)

        csv_path = save_valid_records_to_csv(
            valid_records,
            OUTPUT_DIRECTORY,
        )
        json_path = save_audit_to_json(
            valid_records,
            invalid_records,
            duplicate_records,
            analysis,
            OUTPUT_DIRECTORY,
        )
        database_path = save_valid_records_to_sqlite(
            valid_records,
            OUTPUT_DIRECTORY,
        )

        print("\nSaved output files:")
        print("CSV:", csv_path)
        print("JSON:", json_path)
        print("SQLite:", database_path)

        verify_saved_outputs(
            csv_path,
            json_path,
            database_path,
            len(valid_records),
        )

        report_path = create_text_report(
            valid_records,
            invalid_records,
            duplicate_records,
            analysis,
            OUTPUT_DIRECTORY,
        )

        print("\nText report generated:")
        print("Report:", report_path)

        verify_final_project(
            collected_pages,
            parsed_records,
            valid_records,
            invalid_records,
            duplicate_records,
            api_records,
            analysis,
            csv_path,
            json_path,
            database_path,
            report_path,
        )

        print(
            "\nDay 50 integrated project "
            "completed successfully."
        )

    finally:
        server.shutdown()
        server.server_close()
        server_thread.join()

        print("Local training server closed.")


if __name__ == "__main__":
    main()
