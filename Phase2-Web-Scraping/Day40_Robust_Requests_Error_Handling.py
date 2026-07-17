"""
Day 40 — Robust Requests and Error Handling
Phase 2: Web Scraping

Topic:
Handling request failures gracefully with timeout, try/except,
RequestException, continue, and HTTP status-code checking.

Professional commit message:
Implement robust request handling with timeouts and exceptions
"""

import random
import time

import requests
from bs4 import BeautifulSoup


# ============================================================
# 1. TOPIC OVERVIEW
# ============================================================

# requests.get() can fail before Python receives a response.
#
# Examples:
# - Slow website
# - No internet connection
# - DNS failure
# - Server closes the connection
# - Too many redirects
#
# If requests.get() fails before creating a response object:
# - response does not exist
# - response.status_code cannot be checked
# - without exception handling, the program crashes


# ============================================================
# 2. TIMEOUT
# ============================================================

# Syntax:
#
# response = requests.get(
#     url,
#     headers=headers,
#     timeout=10
# )
#
# timeout=10 means:
# - wait up to 10 seconds
# - if the request takes too long, raise a Timeout exception
#
# A scraper should not wait forever for one page.


# ============================================================
# 3. BASIC TRY/EXCEPT PATTERN
# ============================================================

# try:
#     response = requests.get(url, timeout=10)
#
# except requests.exceptions.Timeout:
#     print("Request timed out")
#
# Without try/except:
# - exception occurs
# - program stops
# - later pages are never scraped
#
# With try/except:
# - error is handled
# - an error message can be shown
# - the scraper can continue


# ============================================================
# 4. REQUESTEXCEPTION
# ============================================================

# Professional pattern:
#
# try:
#     response = requests.get(url, timeout=10)
#
# except requests.exceptions.RequestException as e:
#     print("Request failed:", e)
#
# RequestException is the parent of most requests-related errors.
#
# It can catch errors such as:
# - Timeout
# - ConnectionError
# - HTTPError
# - TooManyRedirects
#
# "as e" stores the real error message inside variable e.


# ============================================================
# 5. WHY NOT USE BARE EXCEPT
# ============================================================

# Avoid:
#
# except:
#     print("Something went wrong")
#
# A bare except catches almost every error, including unrelated
# programming mistakes such as:
# - NameError
# - TypeError
# - AttributeError
#
# This can hide bugs.
#
# Better:
#
# except requests.exceptions.RequestException as e:
#     print("Request failed:", e)


# ============================================================
# 6. CONTINUE INSIDE PAGINATION
# ============================================================

# continue tells Python:
# "Skip the rest of the current loop iteration and start the next one."
#
# Example:
#
# for page in range(1, 4):
#     try:
#         response = requests.get(...)
#     except requests.exceptions.RequestException:
#         continue
#
# If page 2 fails:
# - remaining code for page 2 is skipped
# - page 3 still runs
#
# continue is necessary because response may not exist after a failed request.


# ============================================================
# 7. TRY/EXCEPT VS STATUS CODE CHECKING
# ============================================================

# These solve different problems.
#
# try/except handles request-level failures:
# - no response received
# - timeout
# - connection error
# - DNS failure
#
# status_code handles HTTP response results:
# - 200 Success
# - 403 Forbidden
# - 404 Not Found
# - 429 Too Many Requests
# - 500 Server Error
#
# Professional scrapers normally use both.


# ============================================================
# 8. PROFESSIONAL REQUEST PATTERN
# ============================================================

def demonstrate_request_pattern(url, headers):
    """Demonstrate the professional request-handling structure."""

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None

    print("Status Code:", response.status_code)

    if response.status_code == 200:
        return response

    print("Failed to load page")
    return None


# ============================================================
# 9. COMMON BEGINNER MISTAKES
# ============================================================

# Mistake 1:
# Using requests.get() without timeout.
#
# Mistake 2:
# Checking response.status_code without protecting requests.get().
#
# Mistake 3:
# Using only status-code checking and assuming it handles timeouts.
#
# Mistake 4:
# Using bare except.
#
# Mistake 5:
# Forgetting continue inside a pagination loop after request failure.
#
# Mistake 6:
# Parsing HTML before confirming status code 200.
#
# Mistake 7:
# Assuming response always exists.


# ============================================================
# 10. INTERVIEW NOTES
# ============================================================

# Question:
# Why should requests.get() use a timeout?
#
# Answer:
# A timeout prevents the scraper from waiting indefinitely for a slow
# or unresponsive server.
#
#
# Question:
# Why use RequestException instead of bare except?
#
# Answer:
# RequestException catches requests-related failures without hiding
# unrelated programming errors.
#
#
# Question:
# Why use continue after a failed request in pagination?
#
# Answer:
# continue skips the remaining code for the failed page and starts the
# next page. It also prevents later code from using a response object
# that was never created.
#
#
# Question:
# Are try/except and status-code checking interchangeable?
#
# Answer:
# No. try/except handles failures before a response is received, while
# status-code checking handles HTTP results after a response is received.


# ============================================================
# 11. FINAL HACKER NEWS SCRAPER
# ============================================================

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_articles = []

for page in range(1, 4):
    url = f"https://news.ycombinator.com/news?p={page}"

    print(f"Scraping page {page}")
    print("URL:", url)

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        continue

    print("Status Code:", response.status_code)

    if response.status_code == 200:
        print("Page loaded successfully")

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select(".athing")

        print("Articles Found:", len(articles))

        for article in articles:
            headline_tag = article.select_one(".titleline a")

            if headline_tag:
                title = headline_tag.get_text(strip=True)
                link = headline_tag.get("href")
            else:
                title = "N/A"
                link = "N/A"

            subtext_row = article.find_next_sibling("tr")

            if subtext_row:
                author_tag = subtext_row.select_one(".hnuser")
                time_tag = subtext_row.select_one(".age")
            else:
                author_tag = None
                time_tag = None

            author = (
                author_tag.get_text(strip=True)
                if author_tag
                else "N/A"
            )

            posted_time = (
                time_tag.get_text(strip=True)
                if time_tag
                else "N/A"
            )

            article_data = {
                "title": title,
                "link": link,
                "author": author,
                "time": posted_time
            }

            all_articles.append(article_data)

    else:
        print("Failed to load page")

    delay = random.uniform(1, 3)
    print(f"Waiting {delay:.2f} seconds...\n")
    time.sleep(delay)

print(f"Total articles scraped: {len(all_articles)}")


# ============================================================
# 12. PROFESSIONAL SCRAPER CHECKLIST
# ============================================================

# [x] User-Agent header
# [x] Pagination
# [x] timeout
# [x] try/except
# [x] RequestException
# [x] continue after request failure
# [x] HTTP status-code checking
# [x] Parse only after status code 200
# [x] Missing-element handling
# [x] List of dictionaries
# [x] Random delay
# [x] Final record count


# ============================================================
# 13. DAY 40 SUMMARY
# ============================================================

# Completed:
# - Request-level failures
# - timeout=10
# - try
# - except
# - requests.exceptions.RequestException
# - as e
# - continue
# - Difference between exceptions and status codes
# - Professional request flow
# - Final Hacker News scraper integration
#
# Next roadmap topic:
# Day 41 — requests.Session() and Cookies
