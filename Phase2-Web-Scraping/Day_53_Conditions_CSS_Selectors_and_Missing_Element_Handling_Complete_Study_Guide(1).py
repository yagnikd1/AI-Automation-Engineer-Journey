"""
Day 53: Conditions, CSS Selectors, and Missing-Element Handling

Guided revision project:
Independent Bookstore Inventory Monitor

Topics covered:
- if, elif, and else
- comparison and logical operators
- in, not in, truthy/falsy values, and nested conditions
- BeautifulSoup find(), find_all(), select_one(), and select()
- CSS selectors for IDs, classes, attributes, descendants, and children
- safe text and attribute extraction
- missing, empty, and invalid values
- fallback selectors
- numeric conversion, validation, skip reasons, and record skipping
- final analysis and reporting
"""

from bs4 import BeautifulSoup


print("Starting Independent Bookstore Inventory Monitor...")

# ---------------------------------------------------------------------------
# SECTION 1: CONDITIONS REVISION
# ---------------------------------------------------------------------------

book_title = "Practical Automation"
price = 24.50
rating = 4.7
stock_status = "In Stock"
book_format = "Paperback"

if stock_status == "In Stock":
    print(f"{book_title} is available.")
else:
    print(f"{book_title} is unavailable.")

if rating >= 4.5:
    rating_category = "Highly Rated"
elif rating >= 4.0:
    rating_category = "Well Rated"
elif rating >= 3.0:
    rating_category = "Average"
else:
    rating_category = "Low Rated"

print(f"Rating category: {rating_category}")

if stock_status == "In Stock" and price <= 25:
    print("Purchase status: Affordable and available")
else:
    print("Purchase status: Does not meet both requirements")

if book_format in ["Paperback", "Hardcover"]:
    print("Format status: Physical book")
else:
    print("Format status: Non-physical or unknown format")


# ---------------------------------------------------------------------------
# SECTION 2: CSS SELECTORS
# ---------------------------------------------------------------------------

bookstore_html = """
<section id="book-inventory">
    <article class="book-card featured" data-format="Paperback">
        <h2 class="book-title">Practical Automation</h2>
        <p class="author">Morgan Blake</p>
        <span class="price">$24.50</span>
        <span class="rating">4.7</span>
        <span class="stock in-stock">In Stock</span>
    </article>

    <article class="book-card" data-format="Hardcover">
        <h2 class="book-title">Reliable Web Scraping</h2>
        <p class="author">Taylor Reed</p>
        <span class="price">$31.00</span>
        <span class="rating">4.3</span>
        <span class="stock out-of-stock">Out of Stock</span>
    </article>

    <article class="book-card" data-format="Ebook">
        <h2 class="book-title">Python Data Workflows</h2>
        <p class="author">Jordan Lee</p>
        <span class="price">$18.75</span>
        <span class="rating">4.1</span>
        <span class="stock in-stock">In Stock</span>
    </article>
</section>
"""

soup = BeautifulSoup(bookstore_html, "html.parser")

print("\n--- CSS SELECTOR PRACTICE ---")

inventory = soup.select_one("#book-inventory")
print(f"Inventory found: {inventory is not None}")

first_title = soup.select_one(".book-title")
print(
    "First title:",
    first_title.get_text(strip=True)
    if first_title is not None
    else "Title missing",
)

first_card = soup.select_one("article.book-card")
print(f"First card found: {first_card is not None}")

all_cards = soup.select("article.book-card")
print(f"Total book cards: {len(all_cards)}")

all_titles = soup.select("#book-inventory .book-title")
print("All titles:")
for title_element in all_titles:
    print(f"- {title_element.get_text(strip=True)}")

featured_book = soup.select_one(".book-card.featured")
featured_title = (
    featured_book.select_one(".book-title")
    if featured_book is not None
    else None
)
print(
    "Featured book:",
    featured_title.get_text(strip=True)
    if featured_title is not None
    else "Featured title missing",
)

paperback_book = soup.select_one('[data-format="Paperback"]')
paperback_title = (
    paperback_book.select_one(".book-title")
    if paperback_book is not None
    else None
)
print(
    "Paperback selection:",
    paperback_title.get_text(strip=True)
    if paperback_title is not None
    else "Paperback title missing",
)

direct_articles = soup.select("#book-inventory > article")
print(f"Direct article children: {len(direct_articles)}")


# ---------------------------------------------------------------------------
# SECTION 3: MISSING, EMPTY, AND OPTIONAL VALUES
# ---------------------------------------------------------------------------

incomplete_html = """
<section id="new-arrivals">
    <article class="book-card" data-format="Paperback">
        <h2 class="book-title">Automation Patterns</h2>
        <span class="price">$22.00</span>
        <span class="stock">In Stock</span>
    </article>

    <article class="book-card">
        <h2 class="book-title">Resilient Data Collection</h2>
        <span class="rating">4.4</span>
        <span class="stock"></span>
    </article>

    <article class="book-card" data-format="Hardcover">
        <span class="price">Price unavailable</span>
        <span class="stock">Out of Stock</span>
    </article>
</section>
"""

incomplete_soup = BeautifulSoup(incomplete_html, "html.parser")
incomplete_cards = incomplete_soup.select(
    "#new-arrivals > article.book-card"
)

print("\n--- MISSING-ELEMENT HANDLING ---")

for card_number, card in enumerate(incomplete_cards, start=1):
    title_element = card.select_one(".book-title")
    price_element = card.select_one(".price")
    rating_element = card.select_one(".rating")
    stock_element = card.select_one(".stock")

    if title_element is not None:
        title = title_element.get_text(strip=True)
    else:
        title = "Unknown title"

    price_text = (
        price_element.get_text(strip=True)
        if price_element is not None
        else "Price missing"
    )

    rating_text = (
        rating_element.get_text(strip=True)
        if rating_element is not None
        else "Not rated"
    )

    if stock_element is None:
        stock = "Stock element missing"
    elif not stock_element.get_text(strip=True):
        stock = "Stock status empty"
    else:
        stock = stock_element.get_text(strip=True)

    extracted_format = card.get("data-format", "Format missing")

    print(f"\nBook card {card_number}")
    print(f"Title: {title}")
    print(f"Price: {price_text}")
    print(f"Rating: {rating_text}")
    print(f"Stock: {stock}")
    print(f"Format: {extracted_format}")


# ---------------------------------------------------------------------------
# SECTION 4: FIND METHODS VERSUS CSS SELECTORS
# ---------------------------------------------------------------------------

print("\n--- FIND METHODS VERSUS CSS SELECTORS ---")

title_with_find = incomplete_soup.find("h2", class_="book-title")
title_with_selector = incomplete_soup.select_one("h2.book-title")

print(
    "find() first title:",
    title_with_find.get_text(strip=True)
    if title_with_find is not None
    else "Title missing",
)

print(
    "select_one() first title:",
    title_with_selector.get_text(strip=True)
    if title_with_selector is not None
    else "Title missing",
)

cards_with_find_all = incomplete_soup.find_all(
    "article",
    class_="book-card",
)
cards_with_select = incomplete_soup.select(
    "#new-arrivals > article.book-card"
)

print(f"find_all() card count: {len(cards_with_find_all)}")
print(f"select() card count: {len(cards_with_select)}")

hardcover_with_find = incomplete_soup.find(
    "article",
    attrs={"data-format": "Hardcover"},
)
hardcover_with_selector = incomplete_soup.select_one(
    'article[data-format="Hardcover"]'
)

print(
    "Hardcover found with find():",
    hardcover_with_find is not None,
)
print(
    "Hardcover found with select_one():",
    hardcover_with_selector is not None,
)

missing_author = incomplete_soup.find("p", class_="author")

if missing_author is None:
    print("Author handling: No author element found")
else:
    print("Author:", missing_author.get_text(strip=True))


# ---------------------------------------------------------------------------
# SECTION 5: FALLBACK SELECTORS AND REUSABLE SAFE EXTRACTION
# ---------------------------------------------------------------------------

print("\n--- FALLBACK SELECTORS AND SAFE EXTRACTION ---")

fallback_html = """
<section id="supplier-books">
    <article class="supplier-book" data-format="Paperback">
        <h2 class="book-title">Robust Python Automation</h2>
        <span class="sale-price">$19.50</span>
        <span class="availability">Available</span>
    </article>

    <article class="supplier-book" data-format="Hardcover">
        <h3 class="title">Defensive Web Scraping</h3>
        <span class="price">$28.00</span>
        <span class="stock">Limited Stock</span>
    </article>

    <article class="supplier-book">
        <h2 class="book-title"></h2>
        <span class="sale-price">Contact store</span>
    </article>
</section>
"""

fallback_soup = BeautifulSoup(fallback_html, "html.parser")
supplier_cards = fallback_soup.select(
    "#supplier-books > article.supplier-book"
)


def safe_text(parent, selectors, default):
    """Return the first non-empty selector result, or a default value."""
    for selector in selectors:
        element = parent.select_one(selector)

        if element is not None:
            text = element.get_text(strip=True)

            if text:
                return text

    return default


for card_number, card in enumerate(supplier_cards, start=1):
    title = safe_text(
        card,
        [".book-title", ".title"],
        "Unknown title",
    )
    price_text = safe_text(
        card,
        [".sale-price", ".price"],
        "Price missing",
    )
    stock = safe_text(
        card,
        [".availability", ".stock"],
        "Stock status missing",
    )
    extracted_format = card.get("data-format") or "Format missing"

    print(f"\nSupplier card {card_number}")
    print(f"Title: {title}")
    print(f"Price: {price_text}")
    print(f"Stock: {stock}")
    print(f"Format: {extracted_format}")


# ---------------------------------------------------------------------------
# SECTION 6: INVALID VALUES AND RECORD SKIPPING
# ---------------------------------------------------------------------------

print("\n--- INVALID VALUES AND RECORD SKIPPING ---")


def parse_price(price_text):
    """Convert '$19.50' to 19.5; return None for missing or invalid text."""
    if not price_text:
        return None

    cleaned_price = price_text.replace("$", "").replace(",", "").strip()

    try:
        return float(cleaned_price)
    except ValueError:
        return None


valid_supplier_books = []
skipped_supplier_books = []

for card_number, card in enumerate(supplier_cards, start=1):
    title = safe_text(
        card,
        [".book-title", ".title"],
        "Unknown title",
    )
    price_text = safe_text(
        card,
        [".sale-price", ".price"],
        "Price missing",
    )
    stock = safe_text(
        card,
        [".availability", ".stock"],
        "Stock status missing",
    )
    extracted_format = card.get("data-format", "Format missing")
    numeric_price = parse_price(price_text)

    skip_reasons = []

    if title == "Unknown title":
        skip_reasons.append("missing title")

    if numeric_price is None:
        skip_reasons.append("invalid price")

    if stock == "Stock status missing":
        skip_reasons.append("missing stock status")

    if skip_reasons:
        skipped_supplier_books.append(
            {
                "card_number": card_number,
                "title": title,
                "reasons": skip_reasons,
            }
        )
        continue

    valid_supplier_books.append(
        {
            "title": title,
            "price": numeric_price,
            "stock": stock,
            "format": extracted_format,
        }
    )

print(f"Valid records: {len(valid_supplier_books)}")
print(f"Skipped records: {len(skipped_supplier_books)}")

print("\nValid books:")
for book in valid_supplier_books:
    print(
        f"- {book['title']} | "
        f"${book['price']:.2f} | "
        f"{book['stock']} | "
        f"{book['format']}"
    )

print("\nSkipped books:")
for skipped_book in skipped_supplier_books:
    reasons = ", ".join(skipped_book["reasons"])
    print(
        f"- Card {skipped_book['card_number']}: "
        f"{skipped_book['title']} | "
        f"Reasons: {reasons}"
    )


# ---------------------------------------------------------------------------
# SECTION 7: FINAL INVENTORY MONITOR REPORT
# ---------------------------------------------------------------------------

print("\n--- FINAL INVENTORY MONITOR REPORT ---")

available_books = []
affordable_available_books = []
physical_books = []

for book in valid_supplier_books:
    stock = book["stock"]
    price = book["price"]
    extracted_format = book["format"]

    if stock == "Available" or stock == "Limited Stock":
        available_books.append(book)

        if price <= 25:
            affordable_available_books.append(book)

    if extracted_format not in ["Paperback", "Hardcover"]:
        format_status = "Unsupported or unknown format"
    else:
        format_status = "Physical book"
        physical_books.append(book)

    if price <= 20:
        price_category = "Budget"
    elif price <= 30:
        price_category = "Standard"
    else:
        price_category = "Premium"

    print(f"\nTitle: {book['title']}")
    print(f"Price category: {price_category}")
    print(f"Stock: {stock}")
    print(f"Format status: {format_status}")

if not valid_supplier_books:
    print("\nNo valid books are available for analysis.")
else:
    cheapest_book = min(
        valid_supplier_books,
        key=lambda book: book["price"],
    )
    average_price = sum(
        book["price"] for book in valid_supplier_books
    ) / len(valid_supplier_books)

    print("\nInventory summary:")
    print(f"Valid books monitored: {len(valid_supplier_books)}")
    print(f"Skipped books: {len(skipped_supplier_books)}")
    print(f"Available books: {len(available_books)}")
    print(
        "Affordable and available books: "
        f"{len(affordable_available_books)}"
    )
    print(f"Physical books: {len(physical_books)}")
    print(
        f"Cheapest valid book: {cheapest_book['title']} "
        f"(${cheapest_book['price']:.2f})"
    )
    print(f"Average valid price: ${average_price:.2f}")

print("\nIndependent Bookstore Inventory Monitor completed.")
