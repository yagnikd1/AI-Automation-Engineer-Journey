"""
Day 54 - Loops and Next-Link Pagination

Practical project: Next-Link Book Catalogue Monitor

Topics demonstrated:
- for loops and range()
- while loops
- loop variables and enumerate()
- counters and accumulators
- nested loops
- break and continue
- fixed-page and next-link pagination concepts
- relative-to-absolute URL joining
- repeated-page protection with a set
- missing-next-link handling
- maximum-page safety limits
- correct stopping conditions

Practice website: https://books.toscrape.com/
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


START_URL = "https://books.toscrape.com/catalogue/page-1.html"
HEADERS = {
    "User-Agent": "LearningScraper/1.0"
}
MAX_PAGES = 3

current_url = START_URL
page_number = 0
total_books = 0
successful_pages = 0

page_summaries = []
all_books = []
visited_urls = set()

print("Starting Next-Link Book Catalogue Monitor...")

while current_url:
    # Safety stop: never request more than the configured page limit.
    if page_number >= MAX_PAGES:
        print(f"\nMaximum page limit reached: {MAX_PAGES}")
        break

    # Safety stop: avoid requesting a page that has already been visited.
    if current_url in visited_urls:
        print(f"\nRepeated page detected: {current_url}")
        print("Pagination stopped to prevent an infinite loop.")
        break

    visited_urls.add(current_url)
    page_number += 1

    print(f"\nRequesting page {page_number}...")
    print(f"URL: {current_url}")

    response = requests.get(
        current_url,
        headers=HEADERS,
        timeout=10
    )

    print(f"Status code: {response.status_code}")

    # Request-level stopping condition for this Day 54 program.
    if response.status_code != 200:
        print(f"Page {page_number} could not be collected.")
        break

    # Prevent mojibake such as "Â£" when displaying prices.
    response.encoding = "utf-8"

    successful_pages += 1

    soup = BeautifulSoup(response.text, "html.parser")
    book_cards = soup.select("article.product_pod")
    books_on_page = len(book_cards)

    total_books += books_on_page

    page_summaries.append({
        "page_number": page_number,
        "book_count": books_on_page,
        "url": current_url
    })

    print(f"Books found: {books_on_page}")
    print(f"Running total: {total_books}")
    print("Book preview:")

    # Nested loop: process every book inside the current page iteration.
    for book_position, book_card in enumerate(book_cards, start=1):
        title_element = book_card.select_one("h3 a")
        price_element = book_card.select_one("p.price_color")
        availability_element = book_card.select_one(
            "p.instock.availability"
        )

        # Book-level continue: skip only an incomplete book record.
        if (
            title_element is None
            or price_element is None
            or availability_element is None
        ):
            print(
                f"Book {book_position}: "
                "required information is missing."
            )
            continue

        title = title_element.get("title")

        if not title:
            title = title_element.get_text(strip=True)

        price = price_element.get_text(strip=True)
        availability = availability_element.get_text(" ", strip=True)

        book_record = {
            "page_number": page_number,
            "position": book_position,
            "title": title,
            "price": price,
            "availability": availability
        }

        all_books.append(book_record)

        # Store every valid book, but print only a three-book preview.
        if book_position <= 3:
            print(
                f"{book_position}. {title} | "
                f"{price} | {availability}"
            )
        elif book_position == 4:
            print("Preview limit reached.")

    # Follow the actual Next link instead of guessing the next URL.
    next_element = soup.select_one("li.next a")

    if next_element is None:
        print("\nNo Next link found. Final catalogue page reached.")
        current_url = None
        break

    next_href = next_element.get("href")

    if not next_href:
        print("\nThe Next link has no URL.")
        current_url = None
        break

    next_url = urljoin(current_url, next_href)

    if next_url in visited_urls:
        print(f"\nNext link repeats a visited page: {next_url}")
        print("Pagination stopped to prevent an infinite loop.")
        break

    current_url = next_url


print("\n--- FINAL COLLECTION SUMMARY ---")
print(f"Maximum pages allowed: {MAX_PAGES}")
print(f"Pages requested: {page_number}")
print(f"Pages collected successfully: {successful_pages}")
print(f"Unique page URLs visited: {len(visited_urls)}")
print(f"Total books counted: {total_books}")
print(f"Book records stored: {len(all_books)}")

print("\nPage summaries:")

for summary in page_summaries:
    print(
        f"Page {summary['page_number']}: "
        f"{summary['book_count']} books | "
        f"{summary['url']}"
    )

