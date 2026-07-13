"""
Day 36 - Saving and Loading Scraped Data with JSON
Phase 2 - Web Scraping

Topics covered:
1. Why JSON is useful
2. json.dump() - save Python data to a JSON file
3. json.load() - load JSON data back into Python
4. JSON arrays and objects
5. Saving scraped book data as a list of dictionaries
6. Reading the stored JSON file
7. Extracting text and HTML attributes
8. Common mistakes and professional practices
"""

import json

import requests
from bs4 import BeautifulSoup


# ============================================================
# SECTION 1 - IMPORTANT JSON CONCEPTS
# ============================================================

# JSON is useful because it preserves structured data.
#
# Python list       <-> JSON array
# Python dictionary <-> JSON object
#
# json.dump(data, file)
# Saves Python data into a JSON file.
#
# json.load(file)
# Loads JSON data from a file back into Python.
#
# indent=4 is not fixed.
# You can use indent=2, indent=4, indent=6, etc.
# The number controls how many spaces are used for indentation.
# indent=4 is commonly used because it is easy to read.


# ============================================================
# SECTION 2 - SCRAPE BOOK DATA
# ============================================================

URL = "https://books.toscrape.com/"
JSON_FILE = "books.json"


def scrape_books(url):
    """
    Download the webpage and return a list of book dictionaries.
    """

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    books = []

    for book in soup.select(".product_pod"):
        # The title is stored in the <a> tag's title attribute.
        title = book.h3.a["title"]

        # .price_color is a CSS class name from the website's HTML.
        price = book.select_one(".price_color").get_text(strip=True)

        # The rating is stored inside the class attribute.
        # Example:
        # <p class="star-rating Three"></p>
        rating_element = book.select_one(".star-rating")
        rating = rating_element["class"][1]

        book_data = {
            "title": title,
            "price": price,
            "rating": rating,
        }

        books.append(book_data)

    return books


# ============================================================
# SECTION 3 - SAVE DATA WITH json.dump()
# ============================================================


def save_books_to_json(books, filename):
    """
    Save the list of book dictionaries into a JSON file.
    """

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4, ensure_ascii=False)


# ============================================================
# SECTION 4 - LOAD DATA WITH json.load()
# ============================================================


def load_books_from_json(filename):
    """
    Load JSON data from a file and return it as Python data.
    """

    with open(filename, "r", encoding="utf-8") as file:
        books = json.load(file)

    return books


# ============================================================
# SECTION 5 - DISPLAY LOADED DATA
# ============================================================


def display_books(books):
    """
    Print every loaded book in a readable format.
    """

    print(f"Loaded data type: {type(books)}")
    print(f"Total books loaded: {len(books)}")
    print()

    for book in books:
        print(f"Title  : {book['title']}")
        print(f"Price  : {book['price']}")
        print(f"Rating : {book['rating']}")
        print("-" * 40)


# ============================================================
# MAIN PROGRAM
# ============================================================


def main():
    try:
        books = scrape_books(URL)

        save_books_to_json(books, JSON_FILE)
        print("Books saved successfully!")
        print()

        loaded_books = load_books_from_json(JSON_FILE)

        display_books(loaded_books)

        # Accessing only the first book:
        if loaded_books:
            print()
            print("First book title:")
            print(loaded_books[0]["title"])

    except requests.RequestException as error:
        print(f"Website request failed: {error}")

    except FileNotFoundError:
        print(f"The file '{JSON_FILE}' was not found.")

    except json.JSONDecodeError:
        print(f"The file '{JSON_FILE}' does not contain valid JSON data.")

    except (KeyError, IndexError, TypeError) as error:
        print(f"Expected data was missing or structured differently: {error}")


if __name__ == "__main__":
    main()


# ============================================================
# COMMON MISTAKES
# ============================================================

# 1. Wrong:
# json.load("books.json")
#
# Correct:
# with open("books.json", "r") as file:
#     books = json.load(file)
#
# json.load() expects an opened file object, not a filename string.


# 2. Wrong:
# json.dump(file)
#
# Correct:
# json.dump(books, file, indent=4)
#
# json.dump() needs both the data and the file object.


# 3. Wrong:
# book.append(book_data)
#
# Correct:
# books.append(book_data)
#
# book represents one BeautifulSoup HTML element.
# books is the Python list used to store all book dictionaries.


# 4. Wrong method name:
# book.selectone(".price_color")
#
# Correct:
# book.select_one(".price_color")


# 5. Multiple CSS classes on the same element:
#
# HTML:
# <p class="star-rating Three"></p>
#
# Correct selector for both classes:
# .star-rating.Three
#
# A space means a descendant selector:
# .star-rating .Three
#
# That would mean:
# find an element with class "Three" inside an element with class "star-rating".


# ============================================================
# DAY 36 SUMMARY
# ============================================================

# json.dump(data, file, indent=4)
# Python data -> JSON file
#
# json.load(file)
# JSON file -> Python data
#
# A JSON array becomes a Python list.
# A JSON object becomes a Python dictionary.
#
# Scraped records are commonly stored as:
# [
#     {
#         "title": "...",
#         "price": "...",
#         "rating": "..."
#     }
# ]
#
# Day 36 officially completed:
# Saving scraped data to JSON and loading it back into Python.
