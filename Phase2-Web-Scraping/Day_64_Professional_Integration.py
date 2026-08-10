"""
Day 64 — Professional Integration

This application combines:
- object-oriented Python architecture
- Open Library REST API collection
- ethical and rate-limited HTML scraping
- robots.txt and permission verification
- structured record validation
- SQLite transactions and automatic rollback
- database indexing
- component and integration testing
- reliable resource cleanup

Data sources:
- Open Library API
- Books to Scrape educational demonstration website
"""

import sqlite3
import time
from dataclasses import dataclass
from urllib import robotparser
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


@dataclass
class AppConfig:
    api_url: str = "https://openlibrary.org/search.json"
    scrape_url: str = "https://books.toscrape.com/"
    robots_url: str = "https://books.toscrape.com/robots.txt"
    database_path: str = "day_64_books.db"
    request_timeout: int = 15
    request_delay: float = 1.0
    api_result_limit: int = 5
    scrape_result_limit: int = 5
    scraping_permission_reviewed: bool = True
    permission_note: str = (
        "Books to Scrape explicitly identifies itself as a scraping demo."
    )
    terms_reviewed: bool = True
    terms_note: str = (
        "No separate terms page was found; the homepage explicitly permits scraping."
    )


@dataclass
class BookRecord:
    external_id: str
    title: str
    author: str
    year: int | None
    price: float | None
    source: str
    source_url: str


def clean_price(raw_price):
    """Return a numeric price, or None when a price is unavailable."""
    if not raw_price:
        return None

    cleaned = (
        raw_price.replace("Â", "")
        .replace("£", "")
        .replace("$", "")
        .replace(",", "")
        .strip()
    )
    return float(cleaned)


def validate_record(record):
    """Check fields required for safe storage."""
    if not record.external_id.strip() or not record.title.strip():
        return False
    if not record.source.strip():
        return False
    if record.year is not None and record.year <= 0:
        return False
    if record.price is not None and record.price < 0:
        return False
    return True


def run_component_tests():
    assert clean_price("£51.77") == 51.77
    assert clean_price("$1,120.00") == 1120.00
    assert clean_price("Â£51.77") == 51.77
    assert clean_price(None) is None

    valid_record = BookRecord(
        external_id="TEST-1", title="Test Book", author="Test Author",
        year=2020, price=None, source="test", source_url="https://example.com",
    )
    invalid_record = BookRecord(
        external_id="", title="", author="Unknown", year=-1, price=-5.00,
        source="", source_url="https://example.com",
    )
    assert validate_record(valid_record) is True
    assert validate_record(invalid_record) is False
    print("Component tests: PASS")


class EthicalHTTPClient:
    """A reusable HTTP client with a low-volume delay and explicit cleanup."""

    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Day64TrainingCollector/1.0 (educational, low-volume requests)"
        })
        self.last_request_time = 0.0

    def _apply_rate_limit(self):
        elapsed = time.monotonic() - self.last_request_time
        remaining_delay = self.config.request_delay - elapsed
        if remaining_delay > 0:
            time.sleep(remaining_delay)

    def get(self, url, *, params=None, raise_for_status=True):
        self._apply_rate_limit()
        response = self.session.get(
            url, params=params, timeout=self.config.request_timeout
        )
        self.last_request_time = time.monotonic()
        if raise_for_status:
            response.raise_for_status()
        return response

    def close(self):
        self.session.close()


class OpenLibraryCollector:
    """Collect validated book metadata from the Open Library REST API."""

    def __init__(self, config, http_client):
        self.config = config
        self.http_client = http_client

    def collect(self, query):
        print(f"Requesting Open Library API for: {query}")
        response = self.http_client.get(
            self.config.api_url,
            params={
                "q": query,
                "limit": self.config.api_result_limit,
                "fields": "key,title,author_name,first_publish_year",
            },
        )
        records = []
        for item in response.json().get("docs", []):
            work_key = str(item.get("key", "")).strip()
            title = str(item.get("title", "")).strip()
            authors = item.get("author_name") or []
            author = authors[0] if authors else "Author Unavailable"
            raw_year = item.get("first_publish_year")
            year = raw_year if isinstance(raw_year, int) else None
            record = BookRecord(
                external_id=f"OPENLIBRARY:{work_key}", title=title, author=author,
                year=year, price=None, source="Open Library API",
                source_url=urljoin("https://openlibrary.org", work_key),
            )
            if validate_record(record):
                records.append(record)
        return records


class EthicalBookScraper:
    """Collect a small, permitted sample from Books to Scrape."""

    def __init__(self, config, http_client):
        self.config = config
        self.http_client = http_client

    def verify_scraping_access(self):
        if not self.config.scraping_permission_reviewed:
            raise PermissionError("Scraping permission has not been manually reviewed.")
        if not self.config.terms_reviewed:
            raise PermissionError("The website Terms of Service have not been reviewed.")

        response = self.http_client.get(self.config.robots_url, raise_for_status=False)
        if response.status_code == 404:
            print("robots.txt: not published (HTTP 404)")
            print(f"Permission review: {self.config.permission_note}")
            print(f"Terms review: {self.config.terms_note}")
            return

        response.raise_for_status()
        parser = robotparser.RobotFileParser()
        parser.set_url(self.config.robots_url)
        parser.parse(response.text.splitlines())
        user_agent = self.http_client.session.headers["User-Agent"]
        if not parser.can_fetch(user_agent, self.config.scrape_url):
            raise PermissionError("robots.txt disallows this scraping request.")
        print("robots.txt: requested page is allowed")

    def collect(self):
        self.verify_scraping_access()
        print("Requesting Books to Scrape homepage")
        response = self.http_client.get(self.config.scrape_url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        records = []
        for card in soup.select("article.product_pod")[: self.config.scrape_result_limit]:
            link = card.select_one("h3 a")
            price_element = card.select_one(".price_color")
            if link is None:
                continue
            title = str(link.get("title", "")).strip()
            relative_url = str(link.get("href", "")).strip()
            raw_price = price_element.get_text(strip=True) if price_element else None
            record = BookRecord(
                external_id=f"BOOKSTOSCRAPE:{urljoin(self.config.scrape_url, relative_url)}",
                title=title, author="Author Unavailable", year=None,
                price=clean_price(raw_price), source="Books to Scrape",
                source_url=urljoin(self.config.scrape_url, relative_url),
            )
            if validate_record(record):
                records.append(record)
        return records


class BookDatabase:
    """Manage transactional and indexed SQLite storage for book records."""

    def __init__(self, database_path):
        self.database_path = database_path
        self.connection = None

    def open(self):
        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row

    def create_schema(self):
        if self.connection is None:
            raise RuntimeError("Database connection is not open.")
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    external_id TEXT NOT NULL UNIQUE,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER,
                    price REAL,
                    source TEXT NOT NULL,
                    source_url TEXT NOT NULL
                )
            """)
            self.connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_books_source_title
                ON books (source, title)
            """)

    def save_records(self, records):
        if self.connection is None:
            raise RuntimeError("Database connection is not open.")
        values = [
            (r.external_id, r.title, r.author, r.year, r.price, r.source, r.source_url)
            for r in records
        ]
        with self.connection:
            self.connection.executemany("""
                INSERT INTO books (
                    external_id, title, author, year, price, source, source_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(external_id) DO UPDATE SET
                    title = excluded.title,
                    author = excluded.author,
                    year = excluded.year,
                    price = excluded.price,
                    source = excluded.source,
                    source_url = excluded.source_url
            """, values)
        return len(values)

    def count_records(self):
        if self.connection is None:
            raise RuntimeError("Database connection is not open.")
        return self.connection.execute("SELECT COUNT(*) AS total FROM books").fetchone()["total"]

    def get_source_summary(self):
        if self.connection is None:
            raise RuntimeError("Database connection is not open.")
        return self.connection.execute("""
            SELECT source, COUNT(*) AS total
            FROM books GROUP BY source ORDER BY source
        """).fetchall()

    def verify_index(self):
        if self.connection is None:
            raise RuntimeError("Database connection is not open.")
        indexes = self.connection.execute("PRAGMA index_list('books')").fetchall()
        return any(row["name"] == "idx_books_source_title" for row in indexes)

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None


def run_transaction_rollback_test():
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute("""
            CREATE TABLE transaction_test (
                id INTEGER PRIMARY KEY, value TEXT NOT NULL
            )
        """)
        connection.commit()
        try:
            with connection:
                connection.execute(
                    "INSERT INTO transaction_test (value) VALUES (?)",
                    ("This must be rolled back",),
                )
                raise RuntimeError("Intentional transaction failure")
        except RuntimeError:
            pass
        remaining_rows = connection.execute(
            "SELECT COUNT(*) FROM transaction_test"
        ).fetchone()[0]
        assert remaining_rows == 0
        print("Transaction rollback test: PASS")
    finally:
        connection.close()


def run_collection_demo():
    config = AppConfig()
    http_client = EthicalHTTPClient(config)
    try:
        api_records = OpenLibraryCollector(config, http_client).collect("software automation")
        scraped_records = EthicalBookScraper(config, http_client).collect()
        all_records = api_records + scraped_records
        print("\n--- COLLECTION RESULTS ---")
        print(f"API records: {len(api_records)}")
        print(f"Scraped records: {len(scraped_records)}")
        print(f"Combined records: {len(all_records)}\n")
        for position, record in enumerate(all_records, start=1):
            print(f"{position}. {record.title} | {record.source} | Price: {record.price}")
        return all_records
    finally:
        http_client.close()
        print("HTTP session closed.")


def store_and_verify_records(records):
    config = AppConfig()
    database = BookDatabase(config.database_path)
    try:
        database.open()
        database.create_schema()
        processed_count = database.save_records(records)
        stored_count = database.count_records()
        index_exists = database.verify_index()
        source_summary = database.get_source_summary()
        print("\n--- DATABASE RESULTS ---")
        print(f"Records processed: {processed_count}")
        print(f"Records currently stored: {stored_count}")
        print(f"Database index verified: {index_exists}\n")
        print("Records by source:")
        for row in source_summary:
            print(f"- {row['source']}: {row['total']}")
        assert processed_count == len(records)
        assert stored_count >= len(records)
        assert index_exists is True
        print("Database integration verification: PASS")
    finally:
        database.close()
        print("Database connection closed.")


if __name__ == "__main__":
    run_component_tests()
    run_transaction_rollback_test()
    collected_records = run_collection_demo()
    store_and_verify_records(collected_records)
