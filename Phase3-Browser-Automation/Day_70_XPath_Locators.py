"""
Day 70 - XPath Locators
Phase 3: Browser Automation

Program name: XPath Country Information Collector

Purpose
-------
Open the Scrape This Site countries page in Microsoft Edge and demonstrate
stable XPath construction, text functions, XPath axes, element indexing,
current-element searches, and safe missing-element handling.

Requirements
------------
    pip install selenium

Main topics demonstrated
------------------------
1. Relative XPath
2. Attribute conditions
3. Exact text matching and normalize-space()
4. parent/ancestor and sibling axes
5. XPath indexing with parentheses
6. find_element() versus find_elements()
7. NoSuchElementException handling
8. Stable locator design
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


URL = "https://www.scrapethissite.com/pages/simple/"


def print_xpath_reference():
    """Print a compact Day 70 XPath syntax reference."""

    examples = {
        "Tag anywhere": "//h3",
        "Attribute": "//input[@name='email']",
        "Two conditions": "//button[@type='submit' and @id='save']",
        "Exact text": "//button[text()='Save']",
        "Normalized text": "//button[normalize-space()='Save']",
        "Partial attribute": "//div[contains(@id, 'message-')]",
        "Attribute prefix": "//input[starts-with(@id, 'email-')]",
        "Complete-result index": "(//button)[3]",
        "Direct parent": "//input[@name='email']/parent::div",
        "Ancestor": "//input[@name='email']/ancestor::form",
        "Following sibling": "//label/following-sibling::input",
        "Preceding sibling": "//input/preceding-sibling::label",
    }

    print("DAY 70 XPATH QUICK REFERENCE")
    print("-" * 55)

    for topic, xpath in examples.items():
        print(f"{topic:<23}: {xpath}")


def collect_first_countries(driver, limit=5):
    """Collect the first country names and capitals using relative XPath."""

    # find_elements() returns every match, or [] if there are no matches.
    country_cards = driver.find_elements(
        By.XPATH,
        "//div[@class='col-md-4 country']",
    )

    print(f"\nTotal country cards: {len(country_cards)}")
    print(f"\nFirst {limit} countries:")

    for number, card in enumerate(country_cards[:limit], start=1):
        # The leading dot means: search from the current card element.
        country_name = card.find_element(
            By.XPATH,
            ".//h3[@class='country-name']",
        ).text.strip()

        capital = card.find_element(
            By.XPATH,
            ".//span[@class='country-capital']",
        ).text.strip()

        print(f"{number}. {country_name} - Capital: {capital}")

    return country_cards


def demonstrate_text_and_axes(driver):
    """Demonstrate exact text, ancestor, and sibling navigation."""

    # normalize-space() protects the comparison from extra whitespace.
    andorra_heading = driver.find_element(
        By.XPATH,
        "//h3[normalize-space()='Andorra']",
    )

    print(f"\nExact-text match: {andorra_heading.text.strip()}")

    # Move upward from the heading to its matching country container.
    andorra_card = andorra_heading.find_element(
        By.XPATH,
        "./ancestor::div[@class='col-md-4 country']",
    )
    print(f"Ancestor container found: {andorra_card is not None}")

    # Move sideways from the heading to a later sibling and then descend.
    andorra_capital = andorra_heading.find_element(
        By.XPATH,
        "./following-sibling::div//span[@class='country-capital']",
    )
    print(f"Andorra capital: {andorra_capital.text.strip()}")


def demonstrate_indexing(driver):
    """Show indexing across the complete XPath result."""

    # Parentheses group the entire result before [3] is applied.
    third_country = driver.find_element(
        By.XPATH,
        "(//h3[@class='country-name'])[3]",
    )
    print(f"\nThird country from complete result: {third_country.text.strip()}")

    last_country = driver.find_element(
        By.XPATH,
        "(//h3[@class='country-name'])[last()]",
    )
    print(f"Last country from complete result: {last_country.text.strip()}")


def demonstrate_missing_elements(driver):
    """Compare missing-result behavior for the two Selenium finder methods."""

    missing_elements = driver.find_elements(
        By.XPATH,
        "//country[@id='does-not-exist']",
    )

    print(f"\nMissing find_elements() result: {missing_elements}")
    print(f"Missing element count: {len(missing_elements)}")

    try:
        driver.find_element(
            By.XPATH,
            "//country[@id='does-not-exist']",
        )
    except NoSuchElementException:
        print("Missing find_element(): NoSuchElementException handled safely")


def main():
    """Run the complete Day 70 Edge demonstration."""

    print_xpath_reference()

    driver = webdriver.Edge()

    try:
        driver.get(URL)

        print(f"\nPage title: {driver.title}")
        print(f"Current URL: {driver.current_url}")

        collect_first_countries(driver)
        demonstrate_text_and_axes(driver)
        demonstrate_indexing(driver)
        demonstrate_missing_elements(driver)

    finally:
        # Always close Edge, even if a locator or another operation fails.
        driver.quit()


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# DAY 70 NOTES
# ---------------------------------------------------------------------------
#
# ABSOLUTE AND RELATIVE XPATH
# ---------------------------
# Absolute XPath begins at the root:
#     /html/body/main/div/form/input
# It is fragile because structural changes can break the complete path.
#
# Relative XPath normally begins with //:
#     //input[@name='email']
# It is preferred when it uses meaningful, stable attributes or relationships.
#
# ATTRIBUTE SYNTAX
# ----------------
#     //tag[@attribute='value']
#     //*[@id='search-box']
#     //button[@type='submit' and @id='submit-order']
#     //a[@href='/products' or @href='/services']
#
# TEXT FUNCTIONS
# --------------
# Exact direct text:
#     //h2[text()='Account Settings']
#
# Exact text with whitespace normalized:
#     //button[normalize-space()='Save Changes']
#
# Partial attribute/text:
#     //div[contains(@id, 'notification')]
#     //p[contains(text(), 'successfully')]
#
# Combined text including nested descendants:
#     //div[contains(., 'Payment completed')]
#
# Prefix matching:
#     //input[starts-with(@id, 'email-field-')]
#
# INDEXING
# --------
# XPath positions start at 1.
#     //li[1]          -> each li that is first among relevant siblings
#     (//li)[1]        -> first li from the complete result
#     (//button)[3]    -> third button from the complete result
#     (//button)[last()] -> final button from the complete result
#
# RELATIONSHIPS AND AXES
# ----------------------
# Direct child:
#     //section/div
#
# Descendant at any depth:
#     //section//button
#
# Direct parent:
#     //input[@name='email']/parent::div
#
# Any matching ancestor:
#     //input[@name='email']/ancestor::section[@id='checkout']
#
# Later sibling:
#     //label[text()='Email']/following-sibling::input
#
# Earlier sibling:
#     //input[@name='email']/preceding-sibling::label
#
# CURRENT-ELEMENT SEARCH
# ----------------------
# When searching inside a WebElement, start with a dot:
#     card.find_element(By.XPATH, ".//h3")
# The dot keeps the search scoped to the current card.
#
# FINDER BEHAVIOR
# ---------------
# find_element():
#     - returns the first matching WebElement
#     - raises NoSuchElementException if no element matches
#
# find_elements():
#     - returns all matching WebElements in a list-like collection
#     - returns [] if no elements match
#
# STABLE XPATH CHECKLIST
# ----------------------
# Prefer:
#     - meaningful id, name, data-testid, aria-label, and type attributes
#     - exact or normalized text when the text is stable
#     - stable parent/child or sibling relationships
#     - stable portions of dynamic values with contains()/starts-with()
#
# Avoid:
#     - long absolute paths
#     - random or session-generated complete IDs
#     - unnecessary numeric positions
#     - very broad expressions such as //*[contains(., 'Save')]
#
# DEVTOOLS TESTING
# ----------------
# 1. Open the Elements tab.
# 2. Press Ctrl+F.
# 3. Enter the XPath.
# 4. Confirm the match count and highlighted element before using it in code.

