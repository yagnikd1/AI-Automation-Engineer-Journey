"""Day 60: Selective Retries and Backoff.

This guided study project collects public research records from Open Library.
It demonstrates a retry-enabled requests.Session, selective HTTP status
retries, exponential backoff, Retry-After handling, timeout/error handling,
JSON validation, record cleaning, duplicate detection, and CSV/JSON export.
"""

import csv
import json
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


API_URL = "https://openlibrary.org/search.json"
OUTPUT_DIRECTORY = Path("day60_archive_output")

SEARCH_TERMS = [
    "artificial intelligence",
    "web scraping",
    "automation",
]

RETRYABLE_STATUS_CODES = {
    408,
    429,
    500,
    502,
    503,
    504,
}


def create_retry_session():
    """Return a Session configured for safe automatic GET retries."""
    retry_strategy = Retry(
        total=3,
        connect=3,
        read=3,
        status=3,
        backoff_factor=1,
        status_forcelist=RETRYABLE_STATUS_CODES,
        allowed_methods={"GET"},
        respect_retry_after_header=True,
        raise_on_status=False,
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update(
        {
            "User-Agent": (
                "PublicResearchArchiveCollector/1.0 "
                "(educational project)"
            )
        }
    )

    return session


def fetch_archive_data(session, search_term):
    """Fetch and validate one Open Library search response."""
    parameters = {
        "q": search_term,
        "limit": 5,
        "fields": "key,title,author_name,first_publish_year",
    }

    print(f"\nSearching for: {search_term}")

    try:
        response = session.get(
            API_URL,
            params=parameters,
            timeout=(5, 15),
        )

        print(f"Requested URL: {response.url}")
        print(f"Final status code: {response.status_code}")

        if response.status_code in RETRYABLE_STATUS_CODES:
            print(
                "The request still returned a retryable status "
                "after automatic retries."
            )

        response.raise_for_status()
        response_data = response.json()

    except requests.Timeout as error:
        print(f"Request timed out: {error}")
        return []

    except requests.ConnectionError as error:
        print(f"Connection failed: {error}")
        return []

    except requests.HTTPError as error:
        print(f"HTTP request failed: {error}")
        return []

    except requests.RequestException as error:
        print(f"Other request failure: {error}")
        return []

    except ValueError as error:
        print(f"Response did not contain valid JSON: {error}")
        return []

    if not isinstance(response_data, dict):
        print("Invalid response: the top-level JSON value is not a dictionary.")
        return []

    documents = response_data.get("docs")

    if not isinstance(documents, list):
        print("Invalid response: 'docs' is missing or is not a list.")
        return []

    print(f"Records received: {len(documents)}")
    return documents


def clean_archive_record(document, search_term):
    """Return one normalized archive record, or None if it is invalid."""
    if not isinstance(document, dict):
        return None

    archive_key = document.get("key")
    title = document.get("title")

    if not archive_key or not title:
        return None

    authors = document.get("author_name", [])

    if not isinstance(authors, list):
        authors = []

    clean_authors = [
        str(author).strip()
        for author in authors
        if str(author).strip()
    ]

    first_publish_year = document.get("first_publish_year")

    if not isinstance(first_publish_year, int):
        first_publish_year = None

    return {
        "archive_key": str(archive_key).strip(),
        "title": str(title).strip(),
        "authors": ", ".join(clean_authors) or "Unknown",
        "first_publish_year": first_publish_year,
        "search_term": search_term,
    }


def save_as_csv(records, file_path):
    """Save normalized records as CSV."""
    fieldnames = [
        "archive_key",
        "title",
        "authors",
        "first_publish_year",
        "search_term",
    ]

    with file_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def save_as_json(records, file_path):
    """Save normalized records as readable UTF-8 JSON."""
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)


def main():
    """Run the complete retry-enabled archive collection pipeline."""
    print("Starting Public Research Archive Collector...")

    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)

    csv_path = OUTPUT_DIRECTORY / "archive_records.csv"
    json_path = OUTPUT_DIRECTORY / "archive_records.json"

    collected_records = []
    seen_archive_keys = set()
    duplicate_count = 0
    invalid_count = 0

    session = create_retry_session()

    try:
        for search_term in SEARCH_TERMS:
            documents = fetch_archive_data(session, search_term)

            for document in documents:
                clean_record = clean_archive_record(document, search_term)

                if clean_record is None:
                    invalid_count += 1
                    continue

                archive_key = clean_record["archive_key"]

                if archive_key in seen_archive_keys:
                    duplicate_count += 1
                    continue

                seen_archive_keys.add(archive_key)
                collected_records.append(clean_record)

    finally:
        session.close()

    save_as_csv(collected_records, csv_path)
    save_as_json(collected_records, json_path)

    print("\n--- COLLECTION SUMMARY ---")
    print(f"Unique valid records: {len(collected_records)}")
    print(f"Duplicate records skipped: {duplicate_count}")
    print(f"Invalid records skipped: {invalid_count}")
    print(f"CSV file: {csv_path}")
    print(f"JSON file: {json_path}")
    print("Archive collection completed.")


if __name__ == "__main__":
    main()
