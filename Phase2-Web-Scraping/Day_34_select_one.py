"""
Day 34 - BeautifulSoup select_one()
Phase 2: Web Scraping

Learning goals
--------------
1. Understand the difference between select() and select_one().
2. Use select() to collect multiple matching HTML elements.
3. Use select_one() to extract one matching element from each container.
4. Extract visible text with get_text(strip=True).
5. Extract HTML attributes with get().
6. Store scraped data in dictionaries and a list.
7. Add a basic safety check before extracting data.

Key rule
--------
- select() returns a list of matching tags.
- select_one() returns the first matching tag, or None if nothing matches.

This program uses the exact Day 33 book-catalog structure and refactors it
with select_one() without changing its purpose or output.
"""

from bs4 import BeautifulSoup


HTML = """
<div class="book">
    <h2 class="title">Python Automation</h2>
    <p class="price">$25</p>
    <a href="python.html">View Book</a>
</div>

<div class="book">
    <h2 class="title">Web Scraping Basics</h2>
    <p class="price">$30</p>
    <a href="scraping.html">View Book</a>
</div>
"""


def build_book_catalog(html: str) -> list[dict[str, str]]:
    """Parse HTML and return a list containing one dictionary per book."""

    soup = BeautifulSoup(html, "html.parser")

    # select() is used because the HTML contains multiple book containers.
    books = soup.select("div.book")

    book_catalog: list[dict[str, str]] = []

    for book in books:
        # select_one() is used because each book contains one title,
        # one price, and one link.
        title_tag = book.select_one("h2.title")
        price_tag = book.select_one("p.price")
        link_tag = book.select_one("a")

        # select_one() returns None when an element is missing.
        # This check prevents attribute errors during data extraction.
        if not (title_tag and price_tag and link_tag):
            continue

        title = title_tag.get_text(strip=True)
        price = price_tag.get_text(strip=True)
        link = link_tag.get("href", "")

        book_data = {
            "title": title,
            "price": price,
            "link": link,
        }

        book_catalog.append(book_data)

    return book_catalog


def display_book_catalog(book_catalog: list[dict[str, str]]) -> None:
    """Print the book catalog in a clean, readable format."""

    print("========== BOOK CATALOG ==========")
    print()

    for book_data in book_catalog:
        print("Title :", book_data["title"])
        print("Price :", book_data["price"])
        print("Link :", book_data["link"])
        print("----------------------------------")


def main() -> None:
    """Run the Day 34 demonstration program."""

    catalog = build_book_catalog(HTML)
    display_book_catalog(catalog)


if __name__ == "__main__":
    main()
