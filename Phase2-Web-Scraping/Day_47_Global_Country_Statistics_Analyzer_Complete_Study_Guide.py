"""
DAY 47 — GLOBAL COUNTRY STATISTICS ANALYZER
COMPLETE PYTHON STUDY GUIDE
==========================================

Roadmap position
----------------
Day 47 combined the major Phase 2 skills into one verified data pipeline:

    policy checks
    -> API collection
    -> multi-page website scraping
    -> HTML parsing
    -> source merging
    -> cleaning and validation
    -> analysis
    -> CSV + JSON + SQLite storage
    -> text report
    -> automated verification

Verified Day 47 result
----------------------
- Countries processed: 3/3
- Missing required values: 0
- Duplicate records retained: 0
- Numeric validation: PASS
- CSV records: 3
- JSON records: 3
- SQLite records: 3
- Text-report records: 3
- Automated verification: PASS (15/15)

Important:
This file is a GitHub-ready study guide. It explains the Day 47 architecture
and provides executable offline examples. The real project used live World
Bank API data and permitted Wikipedia article pages. Before scraping any
website, review its current Terms of Use and robots.txt. Stop if access is
prohibited or cannot be verified.

Still pending after Day 47
--------------------------
- Final Phase 2 practical assessment
- Phase 2 closing review and continuity verification
- Deferred recovery: request errors, selective retries, production logging,
  systematic debugging and partial-failure recovery
"""

from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path
from statistics import mean
from typing import Any


# ============================================================================
# 1. IMPORTS, CONSTANTS AND CONFIGURATION
# ============================================================================

# The live project also used:
#
# import time
# import requests
# from bs4 import BeautifulSoup
# from urllib.robotparser import RobotFileParser

BASE_URL = "https://api.worldbank.org/v2"
WIKIPEDIA_ROBOTS_URL = "https://en.wikipedia.org/robots.txt"
WIKIMEDIA_TERMS_URL = "https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use"

COUNTRIES = {
    "IND": {
        "country_name": "India",
        "wikipedia_url": "https://en.wikipedia.org/wiki/India",
    },
    "USA": {
        "country_name": "United States",
        "wikipedia_url": "https://en.wikipedia.org/wiki/United_States",
    },
    "DEU": {
        "country_name": "Germany",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Germany",
    },
}

INDICATORS = {
    "population": "SP.POP.TOTL",
    "land_area_km2": "AG.LND.TOTL.K2",
    "gdp_usd": "NY.GDP.MKTP.CD",
    "gdp_per_capita_usd": "NY.GDP.PCAP.CD",
    "unemployment_rate": "SL.UEM.TOTL.ZS",
    "inflation_rate": "FP.CPI.TOTL.ZG",
}

OUTPUT_DIRECTORY = Path("day47_study_guide_demo_output")
CSV_FILE = OUTPUT_DIRECTORY / "country_statistics.csv"
JSON_FILE = OUTPUT_DIRECTORY / "country_statistics.json"
DATABASE_FILE = OUTPUT_DIRECTORY / "country_statistics.db"
REPORT_FILE = OUTPUT_DIRECTORY / "country_statistics_report.txt"

POLICY_REVIEW = {
    "reviewed_on": "2026-07-24",
    "terms_accessible": True,
    "terms_prohibit_project": False,
    "robots_allowed_for_all_pages": True,
}

STORAGE_FIELDS = (
    "country_code",
    "country_name",
    "capital",
    "official_languages",
    "currency",
    "population",
    "population_year",
    "land_area_km2",
    "land_area_km2_year",
    "gdp_usd",
    "gdp_usd_year",
    "gdp_per_capita_usd",
    "gdp_per_capita_usd_year",
    "unemployment_rate",
    "unemployment_rate_year",
    "inflation_rate",
    "inflation_rate_year",
    "supplementary_source",
)


# ============================================================================
# 2. PURPOSE BEFORE COMMAND: WHY EACH TOOL WAS USED
# ============================================================================

"""
requests.Session()
    Reuses headers and connection settings across requests.

response.raise_for_status()
    Raises an HTTP error when the response status is unsuccessful.

response.json()
    Converts a JSON response into Python lists and dictionaries.

BeautifulSoup(response.text, "html.parser")
    Converts HTML text into a searchable document tree.

soup.select(...)
    Returns every HTML element matching a CSS selector.

soup.select_one(...)
    Returns the first matching element, or None when no match exists.

RobotFileParser
    Reads robots.txt rules. robots.txt is an access instruction, not a
    replacement for Terms-of-Use review.

csv.DictWriter
    Writes dictionaries as rows with a controlled column order.

json.dump
    Writes nested Python data to a structured JSON file.

sqlite3
    Stores typed, queryable records with uniqueness constraints and upserts.

Path
    Builds cross-platform file and directory paths.
"""


# ============================================================================
# 3. ETHICAL ACCESS GATE
# ============================================================================

def verify_stored_policy_review(policy_review: dict[str, Any]) -> None:
    """
    Demonstrate the decision gate used before website scraping.

    A real program should retrieve and inspect the current policies. This
    offline study example verifies the recorded Day 47 decision.
    """

    if not policy_review["terms_accessible"]:
        raise PermissionError("Stop: Terms of Use could not be accessed.")

    if policy_review["terms_prohibit_project"]:
        raise PermissionError("Stop: Terms of Use prohibit this project.")

    if not policy_review["robots_allowed_for_all_pages"]:
        raise PermissionError("Stop: robots.txt does not permit every page.")

    print("Policy gate: PASS")


LIVE_POLICY_PATTERN = r'''
from urllib.robotparser import RobotFileParser
import requests

session = requests.Session()
session.headers.update({"User-Agent": "TrainingResearchBot/1.0"})

def robots_allows(url):
    parser = RobotFileParser()
    parser.set_url("https://example.com/robots.txt")
    parser.read()
    return parser.can_fetch(session.headers["User-Agent"], url)

# Review Terms of Use separately.
# Stop on prohibition, inaccessible policy, 403, 404 or 503.
'''


# ============================================================================
# 4. API COLLECTION: LATEST AVAILABLE INDICATOR RECORD
# ============================================================================

def select_latest_indicator_record(
    api_records: list[dict[str, Any]],
) -> tuple[float, int]:
    """
    Select the first usable value from a newest-to-oldest API response.

    World Bank indicator results are normally returned with recent years
    first. Values can be None, so the program must not simply use index 0.
    """

    for record in api_records:
        if record.get("value") is not None and record.get("date") is not None:
            return float(record["value"]), int(record["date"])

    raise ValueError("No usable indicator value was returned.")


LIVE_WORLD_BANK_PATTERN = r'''
def fetch_latest_indicator(session, country_code, indicator_code):
    url = (
        f"https://api.worldbank.org/v2/country/{country_code}"
        f"/indicator/{indicator_code}"
    )
    response = session.get(
        url,
        params={"format": "json", "per_page": 70},
        timeout=15
    )
    response.raise_for_status()
    payload = response.json()

    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError("Unexpected World Bank response structure.")

    records = payload[1]
    return select_latest_indicator_record(records)
'''


# ============================================================================
# 5. HTML PARSING AND MULTI-PAGE SCRAPING
# ============================================================================

def normalize_label(label: str) -> str:
    """Normalize a label before comparing it with expected field names."""

    return " ".join(label.replace("\xa0", " ").split()).rstrip(":").lower()


def clean_text(text: str) -> str:
    """Remove repeated whitespace and reference-marker spacing."""

    return " ".join(text.replace("\xa0", " ").split())


HTML_PARSING_PATTERN = r'''
from bs4 import BeautifulSoup

def parse_country_page(html):
    soup = BeautifulSoup(html, "html.parser")
    details = {}

    for row in soup.select("table.infobox tr"):
        label_cell = row.select_one("th")
        value_cell = row.select_one("td")

        if label_cell is None or value_cell is None:
            continue

        label = normalize_label(label_cell.get_text(" ", strip=True))
        value = clean_text(value_cell.get_text(" ", strip=True))

        if label == "capital":
            details["capital"] = value
        elif label in {"official language", "official languages"}:
            details["official_languages"] = value
        elif label == "currency":
            details["currency"] = value

    return details
'''

MULTI_PAGE_PATTERN = r'''
import time

def scrape_country_pages(session):
    scraped = {}

    for page_number, (country_code, config) in enumerate(
        COUNTRIES.items(),
        start=1
    ):
        page_url = config["wikipedia_url"]

        # Only continue after Terms and robots.txt permit this exact page.
        response = session.get(page_url, timeout=15)
        response.raise_for_status()

        scraped[country_code] = parse_country_page(response.text)

        if page_number < len(COUNTRIES):
            time.sleep(2)

    return scraped
'''


# ============================================================================
# 6. SOURCE MERGING
# ============================================================================

def merge_country_sources(
    api_countries: list[dict[str, Any]],
    scraped_details: dict[str, dict[str, str]],
) -> list[dict[str, Any]]:
    """
    Merge API and website records with stable country codes.

    Country names can vary between sources. IND, USA and DEU are more reliable
    merge keys than display names.
    """

    merged: list[dict[str, Any]] = []

    for country in api_countries:
        country_code = country["country_code"]

        if country_code not in scraped_details:
            raise ValueError(
                f"Missing supplementary details for {country_code}."
            )

        combined = {
            **country,
            **scraped_details[country_code],
            "supplementary_source": COUNTRIES[country_code]["wikipedia_url"],
        }
        merged.append(combined)

    return merged


# ============================================================================
# 7. CLEANING, DUPLICATE PREVENTION AND VALIDATION
# ============================================================================

def require_non_empty(record: dict[str, Any], field_name: str) -> None:
    """Reject None, empty strings and whitespace-only strings."""

    value = record.get(field_name)

    if value is None:
        raise ValueError(f"{field_name} is missing.")

    if isinstance(value, str) and not value.strip():
        raise ValueError(f"{field_name} is empty.")


def validate_numeric_ranges(country: dict[str, Any]) -> None:
    """Validate every numeric category described by the PASS message."""

    positive_fields = (
        "population",
        "land_area_km2",
        "gdp_usd",
        "gdp_per_capita_usd",
    )

    for field_name in positive_fields:
        if float(country[field_name]) <= 0:
            raise ValueError(
                f"{country['country_code']}: {field_name} must be positive."
            )

    unemployment = float(country["unemployment_rate"])
    if not 0 <= unemployment <= 100:
        raise ValueError("Unemployment rate must be between 0 and 100.")

    # Deflation can produce a negative inflation rate, so do not require >= 0.
    if float(country["inflation_rate"]) < -100:
        raise ValueError("Inflation rate cannot be below -100%.")

    year_fields = (
        "population_year",
        "land_area_km2_year",
        "gdp_usd_year",
        "gdp_per_capita_usd_year",
        "unemployment_rate_year",
        "inflation_rate_year",
    )

    for field_name in year_fields:
        year = int(country[field_name])
        if not 1900 <= year <= 2100:
            raise ValueError(
                f"{country['country_code']}: invalid {field_name}: {year}."
            )


def clean_and_validate_countries(
    countries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Clean fields, reject duplicates and validate before analysis or storage.
    """

    cleaned: list[dict[str, Any]] = []
    seen_codes: set[str] = set()

    for original in countries:
        country = original.copy()
        country_code = clean_text(str(country["country_code"])).upper()

        if country_code in seen_codes:
            continue

        country["country_code"] = country_code

        for field_name in (
            "country_name",
            "capital",
            "official_languages",
            "currency",
            "supplementary_source",
        ):
            country[field_name] = clean_text(str(country[field_name]))

        for field_name in STORAGE_FIELDS:
            require_non_empty(country, field_name)

        validate_numeric_ranges(country)
        seen_codes.add(country_code)
        cleaned.append(country)

    if len(cleaned) != len(COUNTRIES):
        raise ValueError(
            f"Expected {len(COUNTRIES)} unique records; found {len(cleaned)}."
        )

    return cleaned


# ============================================================================
# 8. ANALYSIS
# ============================================================================

def analyse_statistics(countries: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculate the three Day 47 analysis results."""

    if not countries:
        raise ValueError("Cannot analyse an empty country list.")

    largest_economy = max(countries, key=lambda item: item["gdp_usd"])
    lowest_unemployment = min(
        countries,
        key=lambda item: item["unemployment_rate"],
    )
    average_inflation = mean(
        country["inflation_rate"] for country in countries
    )

    return {
        "largest_economy": largest_economy,
        "lowest_unemployment": lowest_unemployment,
        "average_inflation": average_inflation,
    }


def format_integer(value: float | int) -> str:
    return f"{value:,.0f}"


def format_currency(value: float | int) -> str:
    return f"${value:,.2f}"


def format_percentage(value: float | int) -> str:
    return f"{value:.2f}%"


# ============================================================================
# 9. CSV, JSON AND SQLITE STORAGE
# ============================================================================

def create_output_directory() -> None:
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)


def save_to_csv(countries: list[dict[str, Any]]) -> None:
    with CSV_FILE.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=STORAGE_FIELDS)
        writer.writeheader()

        for country in countries:
            writer.writerow(
                {
                    field_name: country[field_name]
                    for field_name in STORAGE_FIELDS
                }
            )


def save_to_json(countries: list[dict[str, Any]]) -> None:
    output = {
        "project": "Global Country Statistics Analyzer",
        "record_count": len(countries),
        "economic_source": {
            "name": "World Bank Indicators API",
            "url": BASE_URL,
        },
        "supplementary_source": {
            "name": "Wikipedia",
            "robots_url": WIKIPEDIA_ROBOTS_URL,
            "terms_url": WIKIMEDIA_TERMS_URL,
        },
        "countries": [
            {
                field_name: country[field_name]
                for field_name in STORAGE_FIELDS
            }
            for country in countries
        ],
    }

    with JSON_FILE.open("w", encoding="utf-8") as json_file:
        json.dump(output, json_file, indent=4, ensure_ascii=False)


def create_database_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS country_statistics (
            country_code TEXT PRIMARY KEY,
            country_name TEXT NOT NULL,
            capital TEXT NOT NULL,
            official_languages TEXT NOT NULL,
            currency TEXT NOT NULL,
            population INTEGER NOT NULL,
            population_year INTEGER NOT NULL,
            land_area_km2 REAL NOT NULL,
            land_area_km2_year INTEGER NOT NULL,
            gdp_usd REAL NOT NULL,
            gdp_usd_year INTEGER NOT NULL,
            gdp_per_capita_usd REAL NOT NULL,
            gdp_per_capita_usd_year INTEGER NOT NULL,
            unemployment_rate REAL NOT NULL,
            unemployment_rate_year INTEGER NOT NULL,
            inflation_rate REAL NOT NULL,
            inflation_rate_year INTEGER NOT NULL,
            supplementary_source TEXT NOT NULL
        )
        """
    )


def save_to_sqlite(countries: list[dict[str, Any]]) -> None:
    """
    Use an upsert so rerunning the program updates, rather than duplicates,
    each record.
    """

    placeholders = ", ".join("?" for _ in STORAGE_FIELDS)
    columns = ", ".join(STORAGE_FIELDS)
    update_columns = ", ".join(
        f"{field}=excluded.{field}"
        for field in STORAGE_FIELDS
        if field != "country_code"
    )

    query = f"""
        INSERT INTO country_statistics ({columns})
        VALUES ({placeholders})
        ON CONFLICT(country_code) DO UPDATE SET
            {update_columns}
    """

    with sqlite3.connect(DATABASE_FILE) as connection:
        create_database_table(connection)

        for country in countries:
            connection.execute(
                query,
                tuple(country[field] for field in STORAGE_FIELDS),
            )


def store_country_statistics(countries: list[dict[str, Any]]) -> None:
    create_output_directory()
    save_to_csv(countries)
    save_to_json(countries)
    save_to_sqlite(countries)


# ============================================================================
# 10. HUMAN-READABLE TEXT REPORT
# ============================================================================

def save_text_report(countries: list[dict[str, Any]]) -> None:
    analysis = analyse_statistics(countries)
    largest = analysis["largest_economy"]
    lowest = analysis["lowest_unemployment"]

    lines = [
        "GLOBAL COUNTRY STATISTICS ANALYZER",
        "=" * 72,
        "",
        "DATA SOURCES",
        f"Economic statistics: World Bank Indicators API ({BASE_URL})",
        "Supplementary details: Wikipedia article pages",
        f"Terms reviewed on: {POLICY_REVIEW['reviewed_on']}",
        "",
        "COUNTRY STATISTICS",
        "=" * 72,
    ]

    for country in countries:
        lines.extend(
            [
                "",
                f"Country: {country['country_name']}",
                f"Country code: {country['country_code']}",
                f"Capital: {country['capital']}",
                f"Official language(s): {country['official_languages']}",
                f"Currency: {country['currency']}",
                (
                    f"Population: {format_integer(country['population'])} "
                    f"({country['population_year']})"
                ),
                (
                    f"GDP: {format_currency(country['gdp_usd'])} "
                    f"({country['gdp_usd_year']})"
                ),
                (
                    "Unemployment rate: "
                    f"{format_percentage(country['unemployment_rate'])} "
                    f"({country['unemployment_rate_year']})"
                ),
                "-" * 72,
            ]
        )

    lines.extend(
        [
            "",
            "LATEST-AVAILABLE DATA ANALYSIS",
            "=" * 72,
            (
                f"Largest economy: {largest['country_name']} — "
                f"{format_currency(largest['gdp_usd'])} "
                f"({largest['gdp_usd_year']})"
            ),
            (
                f"Lowest unemployment rate: {lowest['country_name']} — "
                f"{format_percentage(lowest['unemployment_rate'])} "
                f"({lowest['unemployment_rate_year']})"
            ),
            (
                "Average of the latest available inflation rates: "
                f"{analysis['average_inflation']:.2f}%"
            ),
            (
                "Note: indicator years may differ because each result uses "
                "its latest available official record."
            ),
        ]
    )

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")


# ============================================================================
# 11. AUTOMATED OUTPUT VERIFICATION — 15 CHECKS
# ============================================================================

def verify_output_files() -> None:
    """
    Reopen every output. A successful write message is not final proof that
    the saved content has the required records and structure.
    """

    expected_codes = set(COUNTRIES)

    with CSV_FILE.open("r", newline="", encoding="utf-8-sig") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        csv_rows = list(csv_reader)
        csv_fieldnames = csv_reader.fieldnames

    with JSON_FILE.open("r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    with sqlite3.connect(DATABASE_FILE) as connection:
        sqlite_record_count = connection.execute(
            "SELECT COUNT(*) FROM country_statistics"
        ).fetchone()[0]
        sqlite_unique_count = connection.execute(
            "SELECT COUNT(DISTINCT country_code) FROM country_statistics"
        ).fetchone()[0]
        sqlite_codes = {
            row[0]
            for row in connection.execute(
                "SELECT country_code FROM country_statistics"
            ).fetchall()
        }

    report_text = REPORT_FILE.read_text(encoding="utf-8")
    required_report_text = (
        "GLOBAL COUNTRY STATISTICS ANALYZER",
        "World Bank Indicators API",
        "Wikipedia article pages",
        "Terms reviewed on:",
        "Country: India",
        "Country: United States",
        "Country: Germany",
        "Largest economy:",
        "Lowest unemployment rate:",
        "Average of the latest available inflation rates:",
    )

    checks = [
        ("CSV file exists and is not empty", CSV_FILE.exists() and CSV_FILE.stat().st_size > 0),
        ("JSON file exists and is not empty", JSON_FILE.exists() and JSON_FILE.stat().st_size > 0),
        ("SQLite file exists and is not empty", DATABASE_FILE.exists() and DATABASE_FILE.stat().st_size > 0),
        ("Text report exists and is not empty", REPORT_FILE.exists() and REPORT_FILE.stat().st_size > 0),
        ("CSV record count is 3", len(csv_rows) == len(COUNTRIES)),
        ("CSV field order is correct", csv_fieldnames == list(STORAGE_FIELDS)),
        ("CSV country codes are correct", {row["country_code"] for row in csv_rows} == expected_codes),
        ("JSON metadata count is 3", json_data.get("record_count") == len(COUNTRIES)),
        ("JSON country count is 3", len(json_data.get("countries", [])) == len(COUNTRIES)),
        ("JSON field structure is correct", all(set(item) == set(STORAGE_FIELDS) for item in json_data.get("countries", []))),
        ("JSON country codes are correct", {item["country_code"] for item in json_data.get("countries", [])} == expected_codes),
        ("SQLite record count is 3", sqlite_record_count == len(COUNTRIES)),
        ("SQLite records are unique", sqlite_unique_count == len(COUNTRIES)),
        ("SQLite country codes are correct", sqlite_codes == expected_codes),
        ("Text report contains all required sections", all(text in report_text for text in required_report_text)),
    ]

    failed = [description for description, passed in checks if not passed]

    for number, (description, passed) in enumerate(checks, start=1):
        print(
            f"Check {number:02d}: {description}: "
            f"{'PASS' if passed else 'FAIL'}"
        )

    if failed:
        raise AssertionError("Verification failed: " + "; ".join(failed))

    print(f"Automated verification: PASS ({len(checks)}/{len(checks)})")


# ============================================================================
# 12. DAY 47 CORRECTIONS AND LESSONS
# ============================================================================

"""
Correction 1 — validation must match the PASS message
------------------------------------------------------
The first version printed "Numeric range validation: PASS" without checking
every numeric category. The final version added unemployment, inflation and
all six year-field validations.

Lesson:
A PASS statement is trustworthy only when the program tests everything that
the statement claims.

Correction 2 — syntax error in verification
-------------------------------------------
Incorrect:
    sqlite_unique_count sqlite == len(COUNTRIES)

Correct:
    sqlite_unique_count == len(COUNTRIES)

The extra word caused SyntaxError, so Python could not start the program.

SyntaxError versus failed verification:
- SyntaxError: Python cannot understand the program structure.
- Failed verification: Python runs, but a tested result is wrong.

Correction 3 — write messages are not independent proof
--------------------------------------------------------
"CSV records saved: 3" shows that the writer finished. Reopening the file and
checking its count, fields and country codes provides stronger evidence.
"""


# ============================================================================
# 13. POSSIBLE ISSUES AND RESPONSES
# ============================================================================

POSSIBLE_ISSUES = {
    "Terms unavailable or prohibit access":
        "Stop. Do not scrape without confirmed permission.",
    "robots.txt disallows a page":
        "Stop that page request even if another page is allowed.",
    "HTTP 403, 404 or 503":
        "Stop under the Day 47 safety rule; do not bypass the response.",
    "Timeout or connection failure":
        "Report the failure. Selective retries are a deferred recovery topic.",
    "Unexpected JSON structure":
        "Validate payload type and length before using payload[1].",
    "API value is None":
        "Search newest-to-oldest for the latest usable record.",
    "Different indicator years":
        "Store and display a separate source year for every indicator.",
    "HTML selector returns None":
        "Check before get_text(); the page structure may have changed.",
    "Capital, language or currency missing":
        "Reject the incomplete merged record before storage.",
    "Country-name mismatch":
        "Merge with stable country codes instead of display names.",
    "Duplicate records":
        "Track seen codes and enforce a SQLite primary key.",
    "Invalid numeric range":
        "Raise ValueError before analysis or storage.",
    "Empty analysis list":
        "Reject it before min(), max(), mean() or division.",
    "CSV opens incorrectly in spreadsheet software":
        "Use utf-8-sig and newline=''.",
    "JSON serialization error":
        "Convert unsupported objects such as Path before json.dump().",
    "SQLite column/value mismatch":
        "Keep STORAGE_FIELDS, SQL columns and parameter order identical.",
    "Database rerun creates duplicates":
        "Use PRIMARY KEY plus ON CONFLICT ... DO UPDATE.",
    "Database is locked":
        "Close other connections and use with sqlite3.connect(...).",
    "Output directory missing":
        "Call mkdir(parents=True, exist_ok=True) before writing.",
    "Verification reports FAIL":
        "Read the exact failed check; do not mark the project complete.",
}


def display_possible_issues() -> None:
    print("\nPOSSIBLE ISSUES")
    print("=" * 72)

    for number, (issue, response) in enumerate(POSSIBLE_ISSUES.items(), start=1):
        print(f"{number}. {issue}")
        print(f"   Response: {response}")


# ============================================================================
# 14. OFFLINE DEMONSTRATION DATA
# ============================================================================

def build_offline_demo_records() -> list[dict[str, Any]]:
    """
    Provide stable records so this study guide can be executed without making
    network requests. The values mirror the verified Day 47 execution.
    """

    api_records = [
        {
            "country_code": "IND",
            "country_name": "India",
            "population": 1_463_865_525,
            "population_year": 2025,
            "land_area_km2": 2_973_190,
            "land_area_km2_year": 2023,
            "gdp_usd": 3_956_067_115_771.63,
            "gdp_usd_year": 2025,
            "gdp_per_capita_usd": 2_702.48,
            "gdp_per_capita_usd_year": 2025,
            "unemployment_rate": 4.22,
            "unemployment_rate_year": 2025,
            "inflation_rate": 2.40,
            "inflation_rate_year": 2025,
        },
        {
            "country_code": "USA",
            "country_name": "United States",
            "population": 341_784_857,
            "population_year": 2025,
            "land_area_km2": 9_147_420,
            "land_area_km2_year": 2023,
            "gdp_usd": 30_769_700_000_000.00,
            "gdp_usd_year": 2025,
            "gdp_per_capita_usd": 90_026.52,
            "gdp_per_capita_usd_year": 2025,
            "unemployment_rate": 4.20,
            "unemployment_rate_year": 2025,
            "inflation_rate": 2.95,
            "inflation_rate_year": 2024,
        },
        {
            "country_code": "DEU",
            "country_name": "Germany",
            "population": 83_491_249,
            "population_year": 2025,
            "land_area_km2": 349_430,
            "land_area_km2_year": 2023,
            "gdp_usd": 5_050_922_925_047.05,
            "gdp_usd_year": 2025,
            "gdp_per_capita_usd": 60_496.44,
            "gdp_per_capita_usd_year": 2025,
            "unemployment_rate": 3.71,
            "unemployment_rate_year": 2025,
            "inflation_rate": 2.17,
            "inflation_rate_year": 2025,
        },
    ]

    scraped_details = {
        "IND": {
            "capital": "New Delhi",
            "official_languages": "Hindi, English",
            "currency": "Indian rupee",
        },
        "USA": {
            "capital": "Washington, D.C.",
            "official_languages": "English",
            "currency": "U.S. dollar",
        },
        "DEU": {
            "capital": "Berlin",
            "official_languages": "German",
            "currency": "Euro",
        },
    }

    return merge_country_sources(api_records, scraped_details)


# ============================================================================
# 15. PIPELINE CONTROLLER
# ============================================================================

def main() -> None:
    """
    Run the study-guide demonstration in the same logical order as Day 47.

    The real live program collected API and website data before merging.
    This offline version begins with recorded demo data so it is safe and
    repeatable.
    """

    print("DAY 47 — GLOBAL COUNTRY STATISTICS ANALYZER STUDY GUIDE")
    print("=" * 72)

    verify_stored_policy_review(POLICY_REVIEW)
    countries = build_offline_demo_records()
    countries = clean_and_validate_countries(countries)

    analysis = analyse_statistics(countries)
    print(
        "Largest economy:",
        analysis["largest_economy"]["country_name"],
    )
    print(
        "Lowest unemployment:",
        analysis["lowest_unemployment"]["country_name"],
    )
    print(
        "Average inflation:",
        f"{analysis['average_inflation']:.2f}%",
    )

    store_country_statistics(countries)
    save_text_report(countries)
    verify_output_files()
    display_possible_issues()


if __name__ == "__main__":
    main()

