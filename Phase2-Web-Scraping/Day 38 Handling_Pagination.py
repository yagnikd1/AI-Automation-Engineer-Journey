"""
Day 38 - Handling Pagination.py
Phase 2 - Web Scraping

Topics Covered
--------------
1. What pagination is
2. Page-number pagination using for loops
3. Nested loop pattern (pages -> cards)
4. Real website scraping with requests + BeautifulSoup
5. Handling missing HTML elements
6. Encoding fix
7. Building structured data (list of dictionaries)

-------------------------------------------------------
1. Pagination Concept
-------------------------------------------------------

Page 1
  ↓
Page 2
  ↓
Page 3
  ↓
Collect data from every page.

Use a FOR loop when the total number of pages is known.

-------------------------------------------------------
2. URL Generation
-------------------------------------------------------
"""

for page in range(1, 4):
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    print(url)

"""
-------------------------------------------------------
3. Complete Pagination Skeleton
-------------------------------------------------------
"""

import requests
from bs4 import BeautifulSoup

all_books = []

for page in range(1, 4):

    url = f"https://books.toscrape.com/catalogue/page-{page}.html"

    response = requests.get(url)

    # Encoding fix
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.select("article.product_pod")

    for book in books:

        # Missing HTML handling
        title_tag = book.select_one("h3 a")
        title = title_tag.get("title") if title_tag else "No Title"

        price_tag = book.select_one(".price_color")
        price = (
            price_tag.get_text(strip=True)
            if price_tag
            else "No Price"
        )

        book_data = {
            "title": title,
            "price": price
        }

        all_books.append(book_data)

"""
-------------------------------------------------------
4. View First Five Records
-------------------------------------------------------
"""

for book in all_books[:5]:
    print(book)

"""
-------------------------------------------------------
Key Points
-------------------------------------------------------

• Known pages -> for loop
• Unknown pages -> while loop (Next button)
• Outer loop = pages
• Inner loop = cards
• Use response.apparent_encoding when encoding issues appear.
• Always check if an element exists before calling .get() or .get_text().
• Store dictionaries instead of individual values.
"""
