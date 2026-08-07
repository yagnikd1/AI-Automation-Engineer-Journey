"""
Day 61 - Logged Requests, Parsing, Validation, and Error Tracing
Complete Python Study Guide

This program combines today's Python fundamentals and web-scraping revision:

1. A named logger with DEBUG, INFO, WARNING, ERROR, and CRITICAL examples.
2. A clean INFO-level console handler and detailed DEBUG-level file handler.
3. Duplicate-handler prevention and disabled propagation.
4. A Crossref API request with contextual request logging.
5. Defensive parsing and validation of article records.
6. JSON and CSV exports with useful file-path logging.
7. logger.exception() and logger.error(..., exc_info=True).
8. Bare raise for exception propagation.
9. finally-based handler flushing, removal, and closing.
10. Controlled examples showing what can raise common errors.

Normal live run:
    python Day_61_Logged_Requests_Parsing_Validation_and_Error_Tracing_Complete_Study_Guide.py

Offline sample-data run:
    python Day_61_Logged_Requests_Parsing_Validation_and_Error_Tracing_Complete_Study_Guide.py --sample

Controlled error examples (all exceptions are caught):
    python Day_61_Logged_Requests_Parsing_Validation_and_Error_Tracing_Complete_Study_Guide.py --error-examples
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path
from typing import Any

import requests


# ---------------------------------------------------------------------------
# SECTION 1 - CONSTANTS AND OUTPUT PATHS
# ---------------------------------------------------------------------------

API_URL = "https://api.crossref.org/v1/works"
SEARCH_QUERY = "international space research"
RECORD_LIMIT = 5
REQUEST_TIMEOUT = 15

OUTPUT_DIRECTORY = Path("day61_space_article_output")
LOG_FILE = OUTPUT_DIRECTORY / "space_article_monitor.log"
JSON_FILE = OUTPUT_DIRECTORY / "space_articles.json"
CSV_FILE = OUTPUT_DIRECTORY / "space_articles.csv"

LOGGER_NAME = "space_article_monitor"


# ---------------------------------------------------------------------------
# SECTION 2 - SAMPLE DATA FOR OFFLINE REVISION
# ---------------------------------------------------------------------------

SAMPLE_ITEMS: list[dict[str, Any]] = [
    {
        "title": ["International Space Weather Initiative"],
        "DOI": "10.1016/j.srt.2010.07.018",
        "publisher": "Elsevier BV",
        "published-print": {"date-parts": [[2010]]},
    },
    {
        "title": ["International Space Weather Initiative (ISWI)"],
        "DOI": "10.1016/j.srt.2009.07.002",
        "publisher": "Elsevier BV",
        "published-print": {"date-parts": [[2009]]},
    },
    {
        "title": ["Space research - An international endeavor"],
        "DOI": "10.1016/0273-1177(87)90180-3",
        "author": [{"given": "E.R.", "family": "Schmerling"}],
        "publisher": "Elsevier BV",
        "published-print": {"date-parts": [[1987]]},
    },
    {
        "title": ["International Year of Astronomy"],
        "DOI": "10.1016/s1752-9298(07)80075-2",
        "publisher": "Elsevier BV",
        "published-print": {"date-parts": [[2007]]},
    },
    {
        "title": ["International geophysical calendar 2007"],
        "DOI": "10.1016/s0045-8732(07)80056-8",
        "publisher": "Elsevier BV",
        "published-print": {"date-parts": [[2007]]},
    },
]


# ---------------------------------------------------------------------------
# SECTION 3 - LOGGER CONFIGURATION
# ---------------------------------------------------------------------------

def create_logger() -> logging.Logger:
    """Create the Day 61 logger without attaching duplicate handlers.

    Why the check comes before handler construction:
    - logging.getLogger(name) returns the same named logger in one process.
    - If handlers already exist, adding more would duplicate every message.
    - Returning early also avoids unnecessarily reopening the log file.
    """

    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)

    # Prevent records from also travelling to the root logger, where another
    # handler could display the same message again.
    logger.propagate = False

    if logger.handlers:
        return logger

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler(
        LOG_FILE,
        mode="w",
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def close_logger(logger: logging.Logger) -> None:
    """Flush, remove, and close every handler safely.

    Calling this from finally ensures cleanup after success and failure.
    Removing handlers also allows create_logger() to work correctly if main()
    is called again in the same Python process.
    """

    logger.info("Closing logging handlers")

    for handler in logger.handlers[:]:
        handler.flush()
        logger.removeHandler(handler)
        handler.close()


# ---------------------------------------------------------------------------
# SECTION 4 - REQUEST AND COLLECTION
# ---------------------------------------------------------------------------

def collect_articles(logger: logging.Logger) -> list[dict[str, Any]]:
    """Request article records from Crossref and return raw items.

    Possible errors:
    - requests.Timeout: the server does not respond within REQUEST_TIMEOUT.
    - requests.ConnectionError: DNS, internet, TLS, or connection failure.
    - requests.HTTPError: raise_for_status() sees a 4xx or 5xx response.
    - requests.RequestException: fallback for other request failures.
    - requests.exceptions.JSONDecodeError: response body is not valid JSON.
    - KeyError/TypeError: the API payload has an unexpected structure.
    """

    params = {
        "query": SEARCH_QUERY,
        "rows": RECORD_LIMIT,
        "select": "title,DOI,author,publisher,published,published-print,published-online",
    }
    headers = {
        "User-Agent": (
            "Day61LearningMonitor/1.0 "
            "(educational Python logging practice)"
        )
    }

    logger.info(
        "Article request started | endpoint=%s | query=%s",
        API_URL,
        SEARCH_QUERY,
    )
    logger.debug(
        "Request configuration | params=%s | timeout=%s",
        params,
        REQUEST_TIMEOUT,
    )

    try:
        response = requests.get(
            API_URL,
            params=params,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
        logger.debug("Response received | final_url=%s", response.url)

        response.raise_for_status()
        logger.info(
            "Article request succeeded | status_code=%s",
            response.status_code,
        )

        payload = response.json()
        items = payload["message"]["items"]

        if not isinstance(items, list):
            raise TypeError("Crossref message.items must be a list")

    except requests.Timeout:
        logger.exception(
            "Article request timed out | endpoint=%s | timeout=%s",
            API_URL,
            REQUEST_TIMEOUT,
        )
        raise
    except requests.ConnectionError:
        logger.exception("Article connection failed | endpoint=%s", API_URL)
        raise
    except requests.HTTPError:
        logger.exception("Article HTTP request failed | endpoint=%s", API_URL)
        raise
    except requests.exceptions.JSONDecodeError:
        logger.exception("Article response was not valid JSON | endpoint=%s", API_URL)
        raise
    except (KeyError, TypeError):
        logger.exception("Crossref payload structure was invalid")
        raise
    except requests.RequestException:
        logger.exception("Unexpected request failure | endpoint=%s", API_URL)
        raise

    logger.info("Collection completed | raw_records=%s", len(items))
    return items


# ---------------------------------------------------------------------------
# SECTION 5 - PARSING HELPERS
# ---------------------------------------------------------------------------

def clean_text(value: Any) -> str:
    """Return a whitespace-normalized string or an empty string."""

    if not isinstance(value, str):
        return ""
    return " ".join(value.split())


def extract_title(item: dict[str, Any]) -> str:
    """Extract the first Crossref title safely."""

    titles = item.get("title", [])
    if not isinstance(titles, list) or not titles:
        return ""
    return clean_text(titles[0])


def extract_authors(item: dict[str, Any]) -> str:
    """Combine available author names or return a readable fallback."""

    raw_authors = item.get("author", [])
    if not isinstance(raw_authors, list) or not raw_authors:
        return "Author unavailable"

    names: list[str] = []
    for author in raw_authors:
        if not isinstance(author, dict):
            continue

        given = clean_text(author.get("given"))
        family = clean_text(author.get("family"))
        full_name = " ".join(part for part in (given, family) if part)

        if full_name:
            names.append(full_name)

    return ", ".join(names) if names else "Author unavailable"


def extract_publication_year(item: dict[str, Any]) -> int | None:
    """Try Crossref date fields in priority order and return a valid year."""

    date_fields = ("published-print", "published-online", "published")

    for field_name in date_fields:
        date_data = item.get(field_name)
        if not isinstance(date_data, dict):
            continue

        date_parts = date_data.get("date-parts")
        if not isinstance(date_parts, list) or not date_parts:
            continue
        if not isinstance(date_parts[0], list) or not date_parts[0]:
            continue

        year = date_parts[0][0]
        if isinstance(year, int) and 1000 <= year <= 9999:
            return year

    return None


def parse_and_validate_articles(
    raw_items: list[dict[str, Any]],
    logger: logging.Logger,
) -> list[dict[str, Any]]:
    """Parse raw records, reject invalid records, and remove duplicate DOIs.

    Required fields: title, DOI, publisher, and publication year.
    Authors are optional, so missing author data produces WARNING, not ERROR.
    """

    accepted_articles: list[dict[str, Any]] = []
    seen_dois: set[str] = set()

    logger.info("Parsing and validation started | records=%s", len(raw_items))

    for position, item in enumerate(raw_items, start=1):
        logger.debug("Raw record received | position=%s | data=%r", position, item)

        if not isinstance(item, dict):
            logger.error(
                "Record rejected: expected dictionary | position=%s | type=%s",
                position,
                type(item).__name__,
            )
            continue

        title = extract_title(item)
        doi = clean_text(item.get("DOI")).lower()
        authors = extract_authors(item)
        publisher = clean_text(item.get("publisher"))
        publication_year = extract_publication_year(item)

        missing_fields: list[str] = []
        if not title:
            missing_fields.append("title")
        if not doi:
            missing_fields.append("doi")
        if not publisher:
            missing_fields.append("publisher")
        if publication_year is None:
            missing_fields.append("publication_year")

        if missing_fields:
            logger.error(
                "Record rejected: required data missing | position=%s | fields=%s",
                position,
                ",".join(missing_fields),
            )
            continue

        if doi in seen_dois:
            logger.warning(
                "Duplicate DOI skipped | position=%s | doi=%s",
                position,
                doi,
            )
            continue

        if authors == "Author unavailable":
            logger.warning(
                "Optional author data missing | position=%s | doi=%s",
                position,
                doi,
            )

        article = {
            "title": title,
            "doi": doi,
            "authors": authors,
            "publisher": publisher,
            "publication_year": publication_year,
        }

        seen_dois.add(doi)
        accepted_articles.append(article)

        logger.info(
            "Record accepted | position=%s | doi=%s | year=%s",
            position,
            doi,
            publication_year,
        )

    logger.info(
        "Validation completed | accepted=%s | rejected=%s",
        len(accepted_articles),
        len(raw_items) - len(accepted_articles),
    )
    return accepted_articles


# ---------------------------------------------------------------------------
# SECTION 6 - DISPLAY AND EXPORT
# ---------------------------------------------------------------------------

def display_articles(articles: list[dict[str, Any]]) -> None:
    """Display accepted records for human inspection."""

    print("\n--- ACCEPTED SPACE RESEARCH ARTICLES ---")

    if not articles:
        print("No accepted articles were available.")
        return

    for position, article in enumerate(articles, start=1):
        print(f"\nArticle {position}")
        print(f"Title: {article['title']}")
        print(f"DOI: {article['doi']}")
        print(f"Authors: {article['authors']}")
        print(f"Publisher: {article['publisher']}")
        print(f"Publication year: {article['publication_year']}")


def export_articles(
    articles: list[dict[str, Any]],
    logger: logging.Logger,
) -> None:
    """Export accepted articles to JSON and CSV.

    Possible errors:
    - PermissionError: a target is a directory, is open/locked, or is protected.
    - FileNotFoundError: a parent path is missing when not created first.
    - OSError: disk, path, device, or filesystem failure.
    - TypeError: json.dump receives a non-serializable object.
    - csv.Error: malformed CSV configuration or write operation.
    """

    logger.info("Export started | records=%s", len(articles))

    with JSON_FILE.open("w", encoding="utf-8") as json_file:
        json.dump(articles, json_file, indent=4, ensure_ascii=False)

    logger.info(
        "JSON export completed | path=%s | records=%s",
        JSON_FILE.resolve(),
        len(articles),
    )

    fieldnames = [
        "title",
        "doi",
        "authors",
        "publisher",
        "publication_year",
    ]

    with CSV_FILE.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(articles)

    logger.info(
        "CSV export completed | path=%s | records=%s",
        CSV_FILE.resolve(),
        len(articles),
    )


# ---------------------------------------------------------------------------
# SECTION 7 - CONTROLLED ERROR EXAMPLES
# ---------------------------------------------------------------------------

def demonstrate_error_examples(logger: logging.Logger) -> None:
    """Raise and catch deterministic examples of today's common exceptions.

    These examples explain what can raise an error without breaking the normal
    collector. They run only when --error-examples is supplied.
    """

    logger.info("Controlled error examples started")

    examples: list[tuple[str, type[BaseException], str]] = [
        (
            "Timeout",
            requests.Timeout,
            "A request exceeded its permitted waiting time",
        ),
        (
            "ConnectionError",
            requests.ConnectionError,
            "DNS, internet, TLS, or server connection failed",
        ),
        (
            "HTTPError",
            requests.HTTPError,
            "raise_for_status() received a 4xx or 5xx response",
        ),
        (
            "RequestException",
            requests.RequestException,
            "Another requests-library operation failed",
        ),
        (
            "KeyError",
            KeyError,
            "Code requested a dictionary key that was not present",
        ),
        (
            "TypeError",
            TypeError,
            "A value had the wrong type for the attempted operation",
        ),
        (
            "IndexError",
            IndexError,
            "Code requested a list position that did not exist",
        ),
        (
            "ValueError",
            ValueError,
            "A value had the correct general type but invalid content",
        ),
        (
            "PermissionError",
            PermissionError,
            "A file path was protected, locked, or was a directory",
        ),
        (
            "FileNotFoundError",
            FileNotFoundError,
            "A required file or parent path did not exist",
        ),
        (
            "OSError",
            OSError,
            "A broader operating-system or filesystem operation failed",
        ),
    ]

    for label, exception_type, cause in examples:
        try:
            raise exception_type(cause)
        except exception_type:
            logger.error(
                "Controlled %s example | possible_cause=%s",
                label,
                cause,
                exc_info=True,
            )

    # A real deterministic JSON serialization failure: sets are not supported
    # by json.dumps unless a custom conversion is supplied.
    try:
        json.dumps({"unsupported_value": {1, 2, 3}})
    except TypeError:
        logger.exception(
            "Controlled JSON TypeError | cause=set is not JSON serializable"
        )

    # A real deterministic payload-shape failure.
    try:
        malformed_payload: dict[str, Any] = {"message": {}}
        malformed_payload["message"]["items"]
    except KeyError:
        logger.exception(
            "Controlled payload KeyError | missing_path=message.items"
        )

    logger.info(
        "Controlled error examples completed | all_exceptions_were_caught=true"
    )


# ---------------------------------------------------------------------------
# SECTION 8 - MAIN PROGRAM AND EXCEPTION PROPAGATION
# ---------------------------------------------------------------------------

def main(*, use_sample_data: bool = False, run_error_examples: bool = False) -> None:
    """Run the complete logged collection, validation, and export pipeline."""

    logger = create_logger()

    try:
        logger.info("International Space Research Article Monitor started")

        if run_error_examples:
            demonstrate_error_examples(logger)
            logger.info("Error-example mode completed successfully")
            return

        if use_sample_data:
            logger.info("Offline sample mode enabled | network_request=false")
            raw_articles = SAMPLE_ITEMS
            logger.info("Collection completed | raw_records=%s", len(raw_articles))
        else:
            raw_articles = collect_articles(logger)

        try:
            accepted_articles = parse_and_validate_articles(raw_articles, logger)
            display_articles(accepted_articles)
            export_articles(accepted_articles, logger)
        except (OSError, TypeError, ValueError, csv.Error):
            # exc_info=True explicitly adds the active exception traceback.
            logger.error(
                "Processing or export stage failed",
                exc_info=True,
            )
            # Bare raise preserves the original exception and traceback. It
            # stops the caller from mistaking a partial run for success.
            raise

        logger.info(
            "Program completed successfully | accepted_records=%s",
            len(accepted_articles),
        )

    except Exception:
        # This outer boundary records any failure not already handled above.
        # logger.exception() automatically includes the active traceback.
        logger.exception("Program terminated because an operation failed")
        raise
    finally:
        close_logger(logger)


def parse_arguments() -> argparse.Namespace:
    """Read simple command-line modes for revision and testing."""

    parser = argparse.ArgumentParser(
        description=(
            "Day 61 logged Crossref collection, validation, export, and "
            "controlled error examples"
        )
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--sample",
        action="store_true",
        help="run with built-in records instead of making a network request",
    )
    mode.add_argument(
        "--error-examples",
        action="store_true",
        help="raise and catch controlled examples of common exceptions",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_arguments()
    main(
        use_sample_data=arguments.sample,
        run_error_examples=arguments.error_examples,
    )
