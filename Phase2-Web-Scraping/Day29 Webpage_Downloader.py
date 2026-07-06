"""
Phase 2 - Day 29 - Web Scraping Fundamentals & HTTP Basics

Project: Webpage Downloader

Purpose:
    This beginner web scraping utility sends an HTTP GET request to a webpage,
    stores the returned HTML, saves it into a local file, and reads it back.

Concepts Practiced:
    - requests library
    - HTTP GET request
    - response object
    - response.text
    - file writing
    - file reading
"""

import requests


URL = "https://example.com"
OUTPUT_FILE = "webpage.html"


def download_webpage(url):
    """Send a GET request to the given URL and return the response object."""
    response = requests.get(url)
    return response


def save_html(html, filename):
    """Save HTML content into a local file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html)


def read_html(filename):
    """Read HTML content from a local file and return it."""
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
    return content


def main():
    """Run the webpage downloader program."""
    response = download_webpage(URL)

    print(f"Status Code: {response.status_code}")
    print(f"Final URL: {response.url}")

    html = response.text

    save_html(html, OUTPUT_FILE)
    print(f"HTML saved successfully to {OUTPUT_FILE}.")

    saved_content = read_html(OUTPUT_FILE)
    print("\nSaved HTML Content:")
    print(saved_content)


if __name__ == "__main__":
    main()
