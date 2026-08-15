"""
Day 68 - Text- and Class-Based Locators
========================================

Phase 3: Browser Automation

Learning goals
--------------
1. Locate elements with one class using By.CLASS_NAME.
2. Understand why compound class values cannot be passed to By.CLASS_NAME.
3. Locate links with By.LINK_TEXT and By.PARTIAL_LINK_TEXT.
4. extract visible text with WebElement.text.
5. Read standard and custom HTML attributes with get_attribute().
6. Check visibility, availability, and selection state.
7. Use urllib.parse.quote() to percent-encode a local HTML data URL.
8. Close the Selenium browser safely with try/except/finally.

The practice page is embedded in this file. It does not contact a live
website, consume internet data, or depend on DNS availability.
"""

from urllib.parse import quote

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By


# -----------------------------------------------------------------------------
# SECTION 1 - CONFIGURATION
# -----------------------------------------------------------------------------

REMOTE_DEBUGGING_ARGUMENT = "--remote-debugging-pipe"
DATA_URL_PREFIX = "data:text/html;charset=utf-8,"


# -----------------------------------------------------------------------------
# SECTION 2 - AUTHORISED LOCAL PRACTICE PAGE
# -----------------------------------------------------------------------------

PRACTICE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Automation Course Portal</title>
</head>
<body>
    <section class="course-list featured">
        <article class="course beginner" data-id="C-101">
            <h2>Python Automation</h2>
            <a
                class="course-link"
                href="https://example.com/python"
                title="Open Python course"
            >
                View Python Automation Course
            </a>
        </article>

        <article class="course intermediate" data-id="C-102">
            <h2>Browser Testing</h2>
            <a
                class="course-link"
                href="https://example.com/testing"
                title="Open browser-testing course"
            >
                View Browser Testing Course
            </a>
        </article>
    </section>

    <input class="newsletter-option" type="checkbox" checked>
    <button class="enrol-button" disabled>Enrol Now</button>
    <p class="hidden-message" style="display: none;">
        Registration unavailable
    </p>
</body>
</html>
"""


def build_practice_url(html: str) -> str:
    """Return a percent-encoded data URL containing the supplied HTML."""

    # quote() makes spaces, angle brackets, quotation marks, and other unsafe
    # URL characters safe. Encoding is not encryption.
    return DATA_URL_PREFIX + quote(html)


# -----------------------------------------------------------------------------
# SECTION 3 - BROWSER CREATION
# -----------------------------------------------------------------------------

def create_edge_driver() -> webdriver.Edge:
    """Create Microsoft Edge with the stable remote-debugging pipe option."""

    options = webdriver.EdgeOptions()
    options.add_argument(REMOTE_DEBUGGING_ARGUMENT)
    return webdriver.Edge(options=options)


# -----------------------------------------------------------------------------
# SECTION 4 - CLASS-BASED LOCATORS
# -----------------------------------------------------------------------------

def inspect_course_cards(driver: webdriver.Edge) -> None:
    """Find every course card and display its custom ID and visible heading."""

    course_cards = driver.find_elements(By.CLASS_NAME, "course")
    print(f"\n[3] Course cards found: {len(course_cards)}")

    for card in course_cards:
        course_name = card.find_element(By.TAG_NAME, "h2").text
        course_id = card.get_attribute("data-id")
        print(f"    {course_id}: {course_name}")

    # The section contains two separate classes: course-list and featured.
    # By.CLASS_NAME cannot accept "course-list featured" because of the space.
    featured_list = driver.find_element(
        By.CSS_SELECTOR,
        ".course-list.featured",
    )
    print(
        "[4] Compound-class element displayed:",
        featured_list.is_displayed(),
    )


# -----------------------------------------------------------------------------
# SECTION 5 - LINK-TEXT LOCATORS AND ATTRIBUTES
# -----------------------------------------------------------------------------

def inspect_links(driver: webdriver.Edge) -> None:
    """Demonstrate exact and partial visible-link-text matching."""

    exact_link = driver.find_element(
        By.LINK_TEXT,
        "View Python Automation Course",
    )

    partial_links = driver.find_elements(
        By.PARTIAL_LINK_TEXT,
        "Course",
    )

    print(f"\n[5] Exact link text: {exact_link.text}")
    print(f"    Exact link href: {exact_link.get_attribute('href')}")
    print(f"    Exact link title: {exact_link.get_attribute('title')}")
    print(f"    Partial link matches: {len(partial_links)}")


# -----------------------------------------------------------------------------
# SECTION 6 - ELEMENT-STATE METHODS
# -----------------------------------------------------------------------------

def inspect_element_states(driver: webdriver.Edge) -> None:
    """Check displayed, enabled, and selected states."""

    checkbox = driver.find_element(By.CLASS_NAME, "newsletter-option")
    button = driver.find_element(By.CLASS_NAME, "enrol-button")
    hidden_message = driver.find_element(By.CLASS_NAME, "hidden-message")

    print(f"\n[6] Checkbox displayed: {checkbox.is_displayed()}")
    print(f"    Checkbox enabled: {checkbox.is_enabled()}")
    print(f"    Checkbox selected: {checkbox.is_selected()}")
    print(f"    Button displayed: {button.is_displayed()}")
    print(f"    Button enabled: {button.is_enabled()}")
    print(f"    Hidden message displayed: {hidden_message.is_displayed()}")


# -----------------------------------------------------------------------------
# SECTION 7 - COMPLETE WORKFLOW AND SAFE CLEANUP
# -----------------------------------------------------------------------------

def run_day_68_practice() -> None:
    """Run the complete Day 68 locator demonstration."""

    driver: webdriver.Edge | None = None

    try:
        print("[1] Starting Microsoft Edge...")
        driver = create_edge_driver()

        practice_url = build_practice_url(PRACTICE_HTML)
        driver.get(practice_url)

        print(f"[2] Page title: {driver.title}")
        print(
            "    Current URL begins with data:",
            driver.current_url.startswith("data:"),
        )

        inspect_course_cards(driver)
        inspect_links(driver)
        inspect_element_states(driver)

        print("\n[SUCCESS] Day 68 locator checks completed.")

    except NoSuchElementException as error:
        print(f"\n[LOCATOR ERROR] Required element was not found: {error}")

    except WebDriverException as error:
        print(f"\n[AUTOMATION ERROR] Selenium or Edge failed: {error}")

    except Exception as error:
        print(f"\n[UNEXPECTED ERROR] {type(error).__name__}: {error}")

    finally:
        if driver is not None:
            driver.quit()
            print("[CLEANUP] Browser session ended safely.")
        else:
            print("[CLEANUP] No browser session was created.")


# -----------------------------------------------------------------------------
# SECTION 8 - PROGRAM ENTRY POINT
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    run_day_68_practice()

