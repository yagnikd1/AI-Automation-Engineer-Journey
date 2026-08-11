"""Day 65: final guided recovery project — resilient Open Library collector."""

import csv
import json
import logging
import sqlite3
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


BASE_URL = "https://openlibrary.org/search.json"
SEARCH_QUERY = "python automation"
RESULT_LIMIT = 10

OUTPUT_DIRECTORY = Path("day_65_output")
DATABASE_PATH = OUTPUT_DIRECTORY / "book_search_records.db"
JSON_PATH = OUTPUT_DIRECTORY / "book_search_records.json"
CSV_PATH = OUTPUT_DIRECTORY / "book_search_records.csv"

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


def build_retry_session():
    """Create an HTTPS session that retries temporary failures."""
    retry_policy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry_policy))
    return session


def prepare_output_directory():
    OUTPUT_DIRECTORY.mkdir(exist_ok=True)
    logger.info("Output directory is ready: %s", OUTPUT_DIRECTORY)


def fetch_book_data(session):
    parameters = {
        "q": SEARCH_QUERY,
        "limit": RESULT_LIMIT,
        "fields": "key,title,author_name,first_publish_year",
    }

    try:
        logger.info("Requesting book-search data...")
        response = session.get(BASE_URL, params=parameters, timeout=15)
        response.raise_for_status()
        logger.info("Request succeeded with status %s", response.status_code)
        return response.json()
    except requests.Timeout:
        logger.error("The request timed out after 15 seconds.")
    except requests.HTTPError as error:
        logger.error("The server returned an HTTP error: %s", error)
    except requests.RequestException as error:
        logger.error("A request-related error occurred: %s", error)
    except ValueError as error:
        logger.error("The response was not valid JSON: %s", error)
    return None


def parse_and_validate_books(response_data):
    if response_data is None:
        logger.error("No response data is available for parsing.")
        return []

    raw_books = response_data.get("docs", [])
    valid_books = []
    seen_book_keys = set()
    logger.info("Received %s raw book records.", len(raw_books))

    for position, book in enumerate(raw_books, start=1):
        book_key = book.get("key")
        title = book.get("title")
        authors = book.get("author_name", [])
        first_publish_year = book.get("first_publish_year")

        if not book_key or not title:
            logger.warning("Record %s rejected: missing required key or title.", position)
            continue
        if book_key in seen_book_keys:
            logger.warning("Record %s skipped: duplicate key %s.", position, book_key)
            continue

        seen_book_keys.add(book_key)
        valid_books.append(
            {
                "book_key": book_key,
                "title": title.strip(),
                "authors": ", ".join(authors) if authors else "Author Unavailable",
                "first_publish_year": (
                    first_publish_year
                    if first_publish_year is not None
                    else "Year Unavailable"
                ),
            }
        )

    logger.info("Accepted %s valid unique records.", len(valid_books))
    return valid_books


def store_books_in_database(books):
    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS books (
                    book_key TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    authors TEXT NOT NULL,
                    first_publish_year TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_books_title ON books(title)"
            )

            for book in books:
                cursor.execute(
                    """
                    INSERT INTO books (book_key, title, authors, first_publish_year)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(book_key) DO UPDATE SET
                        title = excluded.title,
                        authors = excluded.authors,
                        first_publish_year = excluded.first_publish_year
                    """,
                    (
                        book["book_key"],
                        book["title"],
                        book["authors"],
                        str(book["first_publish_year"]),
                    ),
                )
            connection.commit()
        logger.info("Stored %s book records in SQLite.", len(books))
    except sqlite3.Error as error:
        logger.error("Database operation failed: %s", error)


def export_books(books):
    try:
        with JSON_PATH.open("w", encoding="utf-8") as json_file:
            json.dump(books, json_file, indent=4, ensure_ascii=False)

        with CSV_PATH.open("w", newline="", encoding="utf-8") as csv_file:
            field_names = ["book_key", "title", "authors", "first_publish_year"]
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(books)
        logger.info("Exported %s records to JSON and CSV.", len(books))
    except OSError as error:
        logger.error("File export failed: %s", error)


def display_summary(books):
    print("\n--- FINAL BOOK SEARCH SUMMARY ---")
    print(f"Search query: {SEARCH_QUERY}")
    print(f"Valid unique records: {len(books)}")
    print(f"SQLite database: {DATABASE_PATH}")
    print(f"JSON export: {JSON_PATH}")
    print(f"CSV export: {CSV_PATH}")
    logger.info("Final summary displayed.")


def main():
    prepare_output_directory()
    session = build_retry_session()
    try:
        response_data = fetch_book_data(session)
        books = parse_and_validate_books(response_data)
        store_books_in_database(books)
        export_books(books)
        display_summary(books)
    finally:
        session.close()
        logger.info("HTTP session closed.")


if __name__ == "__main__":
    main()
