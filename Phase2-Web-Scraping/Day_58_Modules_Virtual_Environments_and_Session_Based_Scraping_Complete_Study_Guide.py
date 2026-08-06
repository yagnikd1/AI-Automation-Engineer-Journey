"""
Day 58 - Modules, Virtual Environments, and Session-Based Scraping

Guided revision topics:
- Standard-library, third-party, and custom modules
- Import styles and aliases
- pip, virtual environments, and requirements.txt
- requests.Session, persistent headers, cookies, connection reuse, and cleanup
- Modular parsing, deduplication, and CSV/JSON export

This file is self-contained for easy review. On its first run, it creates the
companion custom module ``scraper_helpers.py`` beside itself, then imports and
uses that module. An existing helper file is never overwritten.

Required packages:
    python -m pip install requests beautifulsoup4

Run:
    python Day_58_Modules_Virtual_Environments_and_Session_Based_Scraping_Complete_Study_Guide.py
"""

import csv
import importlib
import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
PAGE_LIMIT = 2
OUTPUT_DIRECTORY = Path("day58_output")
HELPER_MODULE_NAME = "scraper_helpers"
HELPER_MODULE_PATH = Path(__file__).with_name(f"{HELPER_MODULE_NAME}.py")

HELPER_MODULE_SOURCE = '''"""Reusable cleaning helpers for the Day 58 scraper."""


def clean_text(text):
    """Remove outer whitespace and collapse repeated internal whitespace."""
    return " ".join(text.split())


def clean_price(price_text):
    """Convert a price such as '£51.77' into the float 51.77."""
    return float(price_text.replace("£", "").strip())


def create_book_record(title, price, availability, page_number):
    """Return one consistently structured and cleaned book record."""
    return {
        "title": clean_text(title),
        "price_gbp": clean_price(price),
        "availability": clean_text(availability),
        "page_number": page_number,
    }
'''


def load_custom_module():
    """Create the Day 58 helper once when missing, then import it."""
    if not HELPER_MODULE_PATH.exists():
        HELPER_MODULE_PATH.write_text(HELPER_MODULE_SOURCE, encoding="utf-8")
        print(f"Custom module created: {HELPER_MODULE_PATH.name}")
    else:
        print(f"Custom module found: {HELPER_MODULE_PATH.name}")

    importlib.invalidate_caches()
    return importlib.import_module(HELPER_MODULE_NAME)


def demonstrate_cookie_persistence(session):
    """Show that a cookie stored in a session is added to a matching request."""
    print("\n--- COOKIE DEMONSTRATION ---")

    session.cookies.set(
        name="training_mode",
        value="day58",
        domain="books.toscrape.com",
        path="/",
    )

    prepared_request = session.prepare_request(
        requests.Request("GET", BASE_URL.format(1))
    )

    print("Stored cookies:", session.cookies.get_dict())
    print("Cookie request header:", prepared_request.headers.get("Cookie"))


def collect_books(session, scraper_helpers):
    """Collect clean, unique book records from the configured page range."""
    books = []
    seen_titles = set()

    for page_number in range(1, PAGE_LIMIT + 1):
        page_url = BASE_URL.format(page_number)

        print(f"\nRequesting page {page_number}...")
        print(f"URL: {page_url}")

        response = session.get(page_url, timeout=15)
        response.raise_for_status()

        # The site content is UTF-8. Setting this explicitly prevents prices
        # such as £51.77 from being decoded incorrectly as Â£51.77.
        response.encoding = "utf-8"

        print(f"Status code: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        book_cards = soup.select("article.product_pod")

        print(f"Books found: {len(book_cards)}")

        for card in book_cards:
            title = card.select_one("h3 a").get("title", "")
            price = card.select_one(".price_color").get_text()
            availability = card.select_one(".availability").get_text()

            cleaned_title = scraper_helpers.clean_text(title)

            if cleaned_title in seen_titles:
                continue

            book = scraper_helpers.create_book_record(
                title=title,
                price=price,
                availability=availability,
                page_number=page_number,
            )

            books.append(book)
            seen_titles.add(cleaned_title)

    return books


def save_json(books):
    """Save the collected records as readable UTF-8 JSON."""
    json_path = OUTPUT_DIRECTORY / "day58_books.json"

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4, ensure_ascii=False)

    print(f"JSON saved: {json_path}")


def save_csv(books):
    """Save the collected records as CSV with an explicit header row."""
    csv_path = OUTPUT_DIRECTORY / "day58_books.csv"
    fieldnames = ["title", "price_gbp", "availability", "page_number"]

    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)

    print(f"CSV saved: {csv_path}")


def main():
    """Configure one session, collect records, export them, and report results."""
    print("Starting Session-Based Book Catalogue Collector...")

    scraper_helpers = load_custom_module()
    OUTPUT_DIRECTORY.mkdir(exist_ok=True)

    with requests.Session() as session:
        session.headers.update(
            {
                "User-Agent": "TrainingResearchBot/1.0",
                "Accept-Language": "en-US,en;q=0.9",
            }
        )

        demonstrate_cookie_persistence(session)
        books = collect_books(session, scraper_helpers)

    save_json(books)
    save_csv(books)

    print("\n--- FINAL RESULTS ---")
    print(f"Unique books collected: {len(books)}")
    print("Session closed automatically.")

    for number, book in enumerate(books[:3], start=1):
        print(
            f"{number}. {book['title']} | "
            f"£{book['price_gbp']:.2f} | "
            f"{book['availability']}"
        )


if __name__ == "__main__":
    main()

