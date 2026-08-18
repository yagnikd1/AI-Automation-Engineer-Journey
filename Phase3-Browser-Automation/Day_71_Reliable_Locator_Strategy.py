"""
DAY 71 - RELIABLE LOCATOR STRATEGY
Program: Support Ticket Locator Audit

Purpose
-------
This learning file records the complete Day 71 lesson and provides one
executable Selenium program. It intentionally excludes Day 70 XPath topics.

Covered Day 71 topics
---------------------
1. Locator-priority strategy
2. Unique versus non-unique elements
3. Dynamic IDs and classes
4. Stable data-* attributes
5. Reusable locator constants
6. Handling missing elements
7. Avoiding brittle selectors
8. Clear diagnostic output for locator failures
"""

from urllib.parse import quote

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


# ============================================================================
# SECTION 1 - LOCATOR-PRIORITY STRATEGY
# ============================================================================
# Prefer stable, meaningful locators. A practical priority order is:
#
# 1. Stable unique data-* attribute, such as data-testid
# 2. Stable unique ID
# 3. Stable name attribute
# 4. Short CSS selector using meaningful attributes
# 5. Exact link text when the text is dependable
# 6. XPath when text or DOM relationships genuinely require it
# 7. Class names after confirming uniqueness
# 8. Position- or structure-based selectors only as a last resort
#
# The page below deliberately contains changing-looking IDs and generated
# classes. The program avoids depending on those values.


# ============================================================================
# SECTION 2 - REUSABLE LOCATOR CONSTANTS
# ============================================================================
# Each locator is a two-item tuple:
#     (locating strategy, selector value)
#
# The * operator later unpacks the tuple into the two arguments expected by
# find_element() or find_elements().

TICKET_PANEL = (
    By.CSS_SELECTOR,
    "[data-testid='priority-ticket']",
)

ASSIGNED_AGENT = (
    By.NAME,
    "assigned_agent",
)

RESOLVE_BUTTON = (
    By.CSS_SELECTOR,
    "[data-testid='resolve-ticket']",
)

ACTION_BUTTONS = (
    By.CLASS_NAME,
    "action-button",
)

MISSING_EXPORT_BUTTON = (
    By.CSS_SELECTOR,
    "[data-testid='export-ticket']",
)


# ============================================================================
# SECTION 3 - UNIQUE VERSUS NON-UNIQUE ELEMENTS
# ============================================================================

def check_unique_locator(driver, locator, description):
    """Return the element only when the locator produces exactly one match."""
    matches = driver.find_elements(*locator)
    count = len(matches)

    if count == 1:
        print(f"UNIQUE: {description}")
        return matches[0]

    if count == 0:
        print(f"NOT FOUND: {description}")
        return None

    print(f"NOT UNIQUE: {description} - {count} matches")
    return None


# Why use find_elements() here?
# - It returns a list.
# - No match produces an empty list instead of NoSuchElementException.
# - len(matches) tells us whether a supposedly unique locator returned 0, 1,
#   or several elements.


# ============================================================================
# SECTION 4 - SAFE MISSING-ELEMENT HANDLING AND DIAGNOSTICS
# ============================================================================

def find_optional_element(driver, locator, description):
    """Find an optional element and print useful evidence when it is absent."""
    try:
        element = driver.find_element(*locator)
        print(f"FOUND: {description}")
        return element

    except NoSuchElementException:
        print(f"NOT FOUND: {description}")
        print(f"Strategy: {locator[0]}")
        print(f"Selector: {locator[1]}")
        print(f"Page title: {driver.title}")
        print(f"Current URL type: {driver.current_url.split(':')[0]}")
        return None


# Returning None lets the calling code make a safe decision:
#
#     if optional_element is None:
#         print("Continue without the optional feature.")
#
# A useful failure message identifies the missing element, locating strategy,
# selector, page title, and current page. A message containing only "Error"
# does not give enough evidence for debugging.


# ============================================================================
# SECTION 5 - OFFLINE AUTHORISED PRACTICE PAGE
# ============================================================================

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Support Ticket Portal</title>
</head>
<body>
    <main>
        <section
            id="ticket-48291"
            class="ticket css-k4p81"
            data-testid="priority-ticket"
        >
            <h1>Priority Support Ticket</h1>

            <label for="agent-93517">Assigned agent</label>
            <input
                id="agent-93517"
                name="assigned_agent"
                value="Morgan Lee"
            >

            <button
                class="action-button"
                data-testid="resolve-ticket"
            >
                Resolve Ticket
            </button>

            <button class="action-button">
                Add Internal Note
            </button>
        </section>
    </main>
</body>
</html>
"""

page_url = "data:text/html;charset=utf-8," + quote(html)


# ============================================================================
# SECTION 6 - COMPLETE PRACTICAL WORKFLOW
# ============================================================================

driver = webdriver.Edge()

try:
    driver.get(page_url)

    print(f"Title: {driver.title}")
    print("-" * 50)

    # Stable data-testid instead of dynamic-looking id="ticket-48291" or
    # generated class="css-k4p81".
    ticket_panel = check_unique_locator(
        driver,
        TICKET_PANEL,
        "Priority ticket panel",
    )

    # A stable name attribute can also be a dependable locator.
    assigned_agent = check_unique_locator(
        driver,
        ASSIGNED_AGENT,
        "Assigned-agent input",
    )

    if assigned_agent is not None:
        print(
            "Assigned agent:",
            assigned_agent.get_attribute("value"),
        )

    # This data-testid is stable and produces exactly one match.
    resolve_button = check_unique_locator(
        driver,
        RESOLVE_BUTTON,
        "Resolve Ticket button",
    )

    # The generic class matches two buttons, so it is not reliable when the
    # program needs one particular button.
    check_unique_locator(
        driver,
        ACTION_BUTTONS,
        "Generic action button",
    )

    # This optional button is intentionally absent. The helper catches the
    # exception, prints diagnostic evidence, and returns None.
    export_button = find_optional_element(
        driver,
        MISSING_EXPORT_BUTTON,
        "Export Ticket button",
    )

    if export_button is None:
        print("Program continued safely without the optional button.")

finally:
    driver.quit()
    print("Browser closed safely.")


# ============================================================================
# SECTION 7 - EXPECTED OUTPUT
# ============================================================================
# Title: Support Ticket Portal
# --------------------------------------------------
# UNIQUE: Priority ticket panel
# UNIQUE: Assigned-agent input
# Assigned agent: Morgan Lee
# UNIQUE: Resolve Ticket button
# NOT UNIQUE: Generic action button - 2 matches
# NOT FOUND: Export Ticket button
# Strategy: css selector
# Selector: [data-testid='export-ticket']
# Page title: Support Ticket Portal
# Current URL type: data
# Program continued safely without the optional button.
# Browser closed safely.


# ============================================================================
# SECTION 8 - DAY 71 COMPLETION NOTES
# ============================================================================
# - A locator that works once is not automatically reliable.
# - Stable and meaningful attributes are safer than changing numbers,
#   generated classes, DOM positions, or long structural paths.
# - A locator intended for one element should be checked for exactly one match.
# - Locator constants reduce repetition and make later maintenance easier.
# - Missing optional elements should not crash the complete workflow.
# - Diagnostic output should explain what failed, where it failed, and which
#   selector Selenium attempted.
# - try/finally guarantees that the controlled Edge session closes safely.

