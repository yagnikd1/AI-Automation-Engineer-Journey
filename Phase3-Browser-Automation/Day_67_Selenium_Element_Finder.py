"""
Day 67: Selenium Finding Elements — Foundations

Project:
    Selenium Country Element Inspector

Learning goals:
    - Understand how Selenium searches the browser's live DOM.
    - Distinguish find_element() from find_elements().
    - Use ID, name, class-name, tag-name, and CSS-selector locators.
    - Search inside a parent WebElement to preserve record relationships.
    - Read visible text through the WebElement.text property.
    - Handle missing and empty elements without stopping the program.
    - Store validated browser data in dictionaries inside a list.
    - Guarantee browser cleanup with try/except/finally.

Verified Day 67 browser results:
    - Microsoft Edge: PASS
    - Google Chrome: PASS
    - Brave: optional isolated-profile test attempted; Brave crashed during
      session creation. Existing personal Brave tabs were not affected.

This final portfolio version uses Microsoft Edge because Edge was the assigned
and fully verified Day 67 browser. The element-finding logic was also verified
unchanged in Google Chrome.
"""

from __future__ import annotations

from typing import Final

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


# ---------------------------------------------------------------------------
# SECTION 1: CONFIGURATION
# ---------------------------------------------------------------------------
# Constants keep values that should not change during one program run in a
# visible, central location. Final communicates that these are configuration
# values rather than ordinary working variables.

TARGET_URL: Final[str] = "https://www.scrapethissite.com/pages/simple/"
DISPLAY_LIMIT: Final[int] = 10


# ---------------------------------------------------------------------------
# SECTION 2: SAFE CHILD-ELEMENT TEXT EXTRACTION
# ---------------------------------------------------------------------------

def get_text_or_default(
    parent: WebElement,
    locator: str,
    value: str,
    default: str,
) -> str:
    """Return stripped visible text or a fallback for missing/empty content.

    parent.find_element() raises NoSuchElementException when no child matches.
    An existing element may still have empty visible text. This helper treats
    those as different runtime situations but safely returns the requested
    fallback for either one.
    """
    try:
        element = parent.find_element(locator, value)
        text = element.text.strip()

        if text:
            return text

        return default

    except NoSuchElementException:
        return default


# ---------------------------------------------------------------------------
# SECTION 3: POPULATION CONVERSION
# ---------------------------------------------------------------------------

def parse_population(population_text: str) -> int | None:
    """Convert population text to an integer; return None when invalid.

    The live page currently provides plain numeric strings, but defensive
    conversion prevents one unexpected value from crashing the full loop.
    """
    cleaned_text = population_text.replace(",", "").strip()

    try:
        population = int(cleaned_text)
    except ValueError:
        return None

    if population < 0:
        return None

    return population


# ---------------------------------------------------------------------------
# SECTION 4: ONE COUNTRY-CARD EXTRACTION
# ---------------------------------------------------------------------------

def extract_country(card: WebElement) -> tuple[dict[str, str | int] | None, str | None]:
    """Extract and validate one country card.

    Searching from ``card`` limits every child lookup to the current repeated
    container. This preserves the relationship between one country's name,
    capital, and population.
    """
    name = get_text_or_default(
        card,
        By.CLASS_NAME,
        "country-name",
        "",
    )
    capital = get_text_or_default(
        card,
        By.CLASS_NAME,
        "country-capital",
        "Capital unavailable",
    )
    population_text = get_text_or_default(
        card,
        By.CLASS_NAME,
        "country-population",
        "",
    )
    population = parse_population(population_text)

    rejection_reasons: list[str] = []

    if not name:
        rejection_reasons.append("missing or empty country name")

    if population is None:
        rejection_reasons.append("missing or invalid population")

    if rejection_reasons:
        return None, "; ".join(rejection_reasons)

    return {
        "name": name,
        "capital": capital,
        "population": population,
    }, None


# ---------------------------------------------------------------------------
# SECTION 5: LOCATOR-BEHAVIOUR VERIFICATION
# ---------------------------------------------------------------------------

def verify_locator_behaviour(
    browser: webdriver.Edge,
    countries_container: WebElement,
) -> None:
    """Demonstrate tag, CSS, one-result, and multiple-result behaviour."""
    print("\n[5/8] Verifying locator behaviour...")

    # By.TAG_NAME finds the first h1 on the page. Its .text includes visible
    # descendant text, which is why the live output also contains "250 items".
    page_heading = browser.find_element(By.TAG_NAME, "h1")
    print(f"      Page heading: {page_heading.text.strip()}")

    # By.CSS_SELECTOR uses familiar CSS syntax. A leading dot selects a class.
    first_country = countries_container.find_element(
        By.CSS_SELECTOR,
        ".country",
    )
    first_country_name = first_country.find_element(
        By.CSS_SELECTOR,
        ".country-name",
    ).text.strip()
    print(f"      First country located with CSS: {first_country_name}")

    # find_elements() returns an empty list instead of raising an exception.
    missing_elements = countries_container.find_elements(
        By.CLASS_NAME,
        "nonexistent-country",
    )
    print(f"      Missing multiple-element result: {missing_elements}")

    # The helper catches the exception raised by a missing find_element().
    missing_text = get_text_or_default(
        first_country,
        By.CSS_SELECTOR,
        ".nonexistent-field",
        "Fallback used safely",
    )
    print(f"      Missing single-element result: {missing_text}")


# ---------------------------------------------------------------------------
# SECTION 6: MAIN SELENIUM WORKFLOW
# ---------------------------------------------------------------------------

def run_country_inspector() -> None:
    """Open Edge, locate DOM elements, validate records, and clean up."""
    browser: webdriver.Edge | None = None

    try:
        print("[1/8] Starting Microsoft Edge...")
        browser = webdriver.Edge()

        print("[2/8] Opening the permitted practice page...")
        browser.get(TARGET_URL)
        print(f"      Page title: {browser.title}")
        print(f"      Current URL: {browser.current_url}")

        print("[3/8] Locating the main countries container by ID...")
        countries_container = browser.find_element(By.ID, "countries")
        print("      Main countries container found.")

        print("[4/8] Collecting country cards inside the container...")
        country_cards = countries_container.find_elements(
            By.CLASS_NAME,
            "country",
        )
        print(f"      Country cards found: {len(country_cards)}")

        verify_locator_behaviour(browser, countries_container)

        print("\n[6/8] Extracting and validating country records...")
        valid_countries: list[dict[str, str | int]] = []
        rejected_records: list[dict[str, str | int]] = []

        for position, card in enumerate(country_cards, start=1):
            country, rejection_reason = extract_country(card)

            if country is None:
                rejected_records.append(
                    {
                        "position": position,
                        "reason": rejection_reason or "unknown rejection",
                    }
                )
                continue

            valid_countries.append(country)

        print(f"      Valid countries: {len(valid_countries)}")
        print(f"      Rejected records: {len(rejected_records)}")

        print(f"\n[7/8] Displaying the first {DISPLAY_LIMIT} valid countries...")
        for position, country in enumerate(
            valid_countries[:DISPLAY_LIMIT],
            start=1,
        ):
            print(
                f"      {position}. {country['name']} | "
                f"Capital: {country['capital']} | "
                f"Population: {country['population']:,}"
            )

        combined_population = sum(
            int(country["population"])
            for country in valid_countries[:DISPLAY_LIMIT]
        )

        print("\n[8/8] Creating the final summary...")
        print(f"      Displayed records: {min(DISPLAY_LIMIT, len(valid_countries))}")
        print(f"      Combined displayed population: {combined_population:,}")
        print("      Day 67 element-finding workflow completed successfully.")

    except NoSuchElementException as error:
        print(f"Required webpage element was not found: {error}")

    except WebDriverException as error:
        print(f"Browser automation failed: {error}")

    finally:
        if browser is not None:
            browser.quit()
            print("Microsoft Edge closed safely.")


# ---------------------------------------------------------------------------
# SECTION 7: PROGRAM ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_country_inspector()


# ---------------------------------------------------------------------------
# DAY 67 QUICK REFERENCE
# ---------------------------------------------------------------------------
# find_element():
#   - Returns the first matching WebElement.
#   - Raises NoSuchElementException when nothing matches.
#
# find_elements():
#   - Returns a list containing every matching WebElement.
#   - Returns [] when nothing matches.
#
# Basic locator examples:
#   browser.find_element(By.ID, "login-form")
#   browser.find_element(By.NAME, "email")
#   browser.find_elements(By.CLASS_NAME, "product-card")
#   browser.find_elements(By.TAG_NAME, "a")
#   browser.find_element(By.CSS_SELECTOR, "#catalog .product-title")
#
# CSS selector reminders:
#   #catalog                         -> element with ID catalog
#   .product-card                    -> element with class product-card
#   article.product-card.featured    -> article with both classes
#   article[data-status="available"] -> exact attribute value
#   #catalog .product-title          -> descendant relationship
#   #catalog > article               -> direct-child relationship
#
# By.CLASS_NAME accepts only one raw class name:
#   Correct:   By.CLASS_NAME, "primary"
#   Incorrect: By.CLASS_NAME, "button primary"
#   Multiple classes require CSS: By.CSS_SELECTOR, ".button.primary"
