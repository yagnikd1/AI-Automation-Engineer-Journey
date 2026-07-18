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
# Additional Day 40 topics completed:
# - Logging request errors
# - Retry mechanisms
# - Maximum retry attempts
# - Retry delays
# - Exponential backoff
#
# Next roadmap topic:
# Day 41 — requests.Session() and Cookies

# ============================================================
# 14. LOGGING REQUEST ERRORS
# ============================================================

# WHAT IT IS:
# Logging means recording useful details whenever a request fails.
#
# HOW IT WORKS:
# The request is placed inside try/except.
# If requests raises an exception, the except block records:
# - Time of failure
# - URL that failed
# - Error/exception message
# - Optional HTTP status code
#
# WHY IT IS USEFUL:
# In a scraper with many pages, a simple "Error" message is not enough.
# Logging helps identify exactly:
# - Which page failed
# - When it failed
# - Why it failed
#
# Example:
#
# from datetime import datetime
#
# try:
#     response = requests.get(url, timeout=5)
#     response.raise_for_status()
#
# except requests.exceptions.RequestException as e:
#     print("=" * 40)
#     print("ERROR LOG")
#     print("Time   :", datetime.now())
#     print("URL    :", url)
#     print("Reason :", e)
#     print("=" * 40)


# ============================================================
# 15. RETRY MECHANISMS
# ============================================================

# WHAT IT IS:
# A retry mechanism attempts the same request again after a failure.
#
# HOW IT WORKS:
# A loop repeats the request a limited number of times.
# If the request succeeds:
# - break stops the retry loop
#
# If the request fails:
# - the exception is caught
# - the program waits
# - the next attempt begins
#
# WHY IT IS USEFUL:
# Some failures are temporary, such as:
# - Connection timeout
# - Slow server
# - Temporary network issue
# - Temporary server overload
#
# Retrying gives the website a chance to recover and prevents
# unnecessary data loss.
#
# Retry is NOT useful for:
# - Wrong URL
# - Programming mistakes
# - Invalid HTML selectors
# - Permanent 404 pages
#
# Basic example:
#
# for attempt in range(3):
#     try:
#         response = requests.get(url, timeout=5)
#         response.raise_for_status()
#
#         print("Request successful")
#         break
#
#     except requests.exceptions.RequestException as e:
#         print(f"Attempt {attempt + 1} failed:", e)
#         time.sleep(2)


# ============================================================
# 16. MAXIMUM RETRY ATTEMPTS
# ============================================================

# WHAT IT IS:
# Maximum retry attempts set a limit on how many times the scraper
# is allowed to try the same request.
#
# HOW IT WORKS:
#
# max_retries = 3
#
# for attempt in range(max_retries):
#
# range(max_retries) creates:
# - attempt 0
# - attempt 1
# - attempt 2
#
# This means the request can run a maximum of 3 times.
#
# WHY IT IS USEFUL:
# Without a retry limit, the scraper could retry forever.
#
# A retry limit prevents:
# - Infinite loops
# - Wasted time
# - Excessive requests
# - Extra pressure on the server
#
# It also allows the program to fail gracefully after reasonable attempts.
#
# Example:
#
# max_retries = 3
#
# for attempt in range(max_retries):
#     try:
#         response = requests.get(url, timeout=5)
#         response.raise_for_status()
#         print("Success")
#         break
#
#     except requests.exceptions.RequestException as e:
#         print(f"Attempt {attempt + 1} failed:", e)
#
#         if attempt == max_retries - 1:
#             print("Maximum retry attempts reached")


# ============================================================
# 17. RETRY DELAYS
# ============================================================

# WHAT IT IS:
# A retry delay pauses the program before the next retry attempt.
#
# HOW IT WORKS:
#
# time.sleep(2)
#
# pauses the program for 2 seconds.
#
# Important:
# time.sleep(2) does NOT control the number of retries.
# It only controls how long the scraper waits before trying again.
#
# WHY IT IS USEFUL:
# Retrying immediately may fail again because the server may still
# be slow, busy, or temporarily unavailable.
#
# Waiting gives:
# - The server time to recover
# - The network time to reconnect
# - The scraper a better chance of succeeding
#
# Example:
#
# except requests.exceptions.RequestException:
#     print("Request failed")
#     time.sleep(2)


# ============================================================
# 18. EXPONENTIAL BACKOFF
# ============================================================

# WHAT IT IS:
# Exponential backoff increases the waiting time after every failure.
#
# HOW IT WORKS:
#
# wait = 2 ** attempt
#
# Attempt values and delays:
#
# attempt = 0 -> 2 ** 0 -> 1 second
# attempt = 1 -> 2 ** 1 -> 2 seconds
# attempt = 2 -> 2 ** 2 -> 4 seconds
# attempt = 3 -> 2 ** 3 -> 8 seconds
#
# Important:
# *  means multiplication
# ** means exponent or power
#
# WHY IT IS USEFUL:
# If many scrapers retry immediately, they may hit the server again
# at the same time and make the overload worse.
#
# Exponential backoff:
# - Keeps the first retry quick
# - Makes later retries slower
# - Reduces repeated pressure on the server
# - Gives the server more recovery time
# - Improves the chance of a successful request
#
# Example:
#
# max_retries = 4
#
# for attempt in range(max_retries):
#     try:
#         response = requests.get(url, timeout=5)
#         response.raise_for_status()
#
#         print("Request successful")
#         break
#
#     except requests.exceptions.RequestException as e:
#         print(f"Attempt {attempt + 1} failed:", e)
#
#         if attempt < max_retries - 1:
#             wait = 2 ** attempt
#             print(f"Waiting {wait} seconds...")
#             time.sleep(wait)
#         else:
#             print("Maximum retry attempts reached")


# ============================================================
# 19. COMPLETE RETRY PATTERN
# ============================================================

from datetime import datetime


def request_with_retries(url, headers, max_retries=4):
    """Request one URL using logging, retry limits, and backoff."""

    for attempt in range(max_retries):
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            response.raise_for_status()

            print("Request successful")
            return response

        except requests.exceptions.RequestException as e:
            print("=" * 50)
            print("REQUEST ERROR LOG")
            print("Time    :", datetime.now())
            print("URL     :", url)
            print("Attempt :", attempt + 1)
            print("Reason  :", e)
            print("=" * 50)

            if attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"Waiting {wait} seconds before retry...\n")
                time.sleep(wait)

            else:
                print("Maximum retry attempts reached.")
                return None


# ============================================================
# 20. UPDATED DAY 40 SUMMARY
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
# - Logging request errors
# - Retry mechanisms
# - Maximum retry attempts
# - Retry delays
# - Exponential backoff
# - Complete professional retry pattern
#
# Day 40 unfinished subtopics:
# - None
#
# Next roadmap topic:
# Day 41 — requests.Session() and Cookies
