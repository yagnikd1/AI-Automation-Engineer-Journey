"""
=========================================================
Day 32 - BeautifulSoup Attribute Extraction + First Scraper
AI Automation Engineer Journey | Phase 2 - Web Scraping
=========================================================

Topics covered:
1. requests.get()
2. response.text
3. BeautifulSoup parsing
4. find_all()
5. Repeated container scraping
6. Attribute extraction with .get()
7. Extracting book title and book link from Books to Scrape

Practice website:
https://books.toscrape.com/
"""

import requests
from bs4 import BeautifulSoup


# ------------------------------------------------------------
# 1. Website URL
# ------------------------------------------------------------
# website_url is the page we want to download.

website_url = "https://books.toscrape.com/"


# ------------------------------------------------------------
# 2. Download the webpage
# ------------------------------------------------------------
# requests gets the HTML from the website.

response = requests.get(website_url)
html = response.text


# ------------------------------------------------------------
# 3. Parse HTML with BeautifulSoup
# ------------------------------------------------------------
# BeautifulSoup converts the raw HTML string into a searchable object.

soup = BeautifulSoup(html, "html.parser")


# ------------------------------------------------------------
# 4. Find repeated book containers
# ------------------------------------------------------------
# Golden scraping rule:
# Find the repeated container first, then extract related data inside it.
# On Books to Scrape, each book is stored inside:
# <article class="product_pod">

books = soup.find_all("article", class_="product_pod")


# ------------------------------------------------------------
# 5. Loop through each book and extract data
# ------------------------------------------------------------
# Each book contains an <a> tag inside <h3>.
# The full book title is stored in the title attribute.
# The book page link is stored in the href attribute.

for book in books:
    title_tag = book.find("h3").find("a")

    title = title_tag.get("title", "")
    book_url = title_tag.get("href", "")

    print("-" * 45)
    print("Book Title:", title)
    print("Book Link :", book_url)


print("-" * 45)
print("Day 32 scraper completed successfully!")
