"""
DAY 81 — PLAYWRIGHT NAVIGATION AND LOCATORS
===========================================

Deep Notes + Practical Syntax
Phase 3 — Browser Automation

ROADMAP:
1. page.goto()
2. Page title and URL
3. CSS selectors
4. Text selectors
5. Role-based locators
6. Label locators
7. Placeholder locators
8. Strict locator behaviour

Prerequisite:
- Day 80 — Playwright Foundations completed.
- Playwright installed in the Phase 3 virtual environment.
- Browser -> BrowserContext -> Page architecture understood.

Core mental model:
    Playwright
        |
      Browser
        |
    BrowserContext
        |
       Page
        |
    Navigate + Locate
        |
      Interact

Important:
- Navigation is performed by a Page.
- A locator describes how to find an element.
- Locator strictness protects against ambiguous interactions.
- Prefer stable, user-facing locators where practical.
"""

from playwright.sync_api import sync_playwright


# ============================================================
# 1. PAGE.GOTO()
# ============================================================

def navigation_example(page):
    """
    Navigate a Page to a URL.

    Selenium equivalent:
        driver.get(url)

    Playwright:
        page.goto(url)
    """

    page.goto("https://example.com")


# ============================================================
# 2. PAGE TITLE AND URL
# ============================================================

def page_information_example(page):
    page.goto("https://example.com")

    title = page.title()   # method
    url = page.url         # property

    print("Title:", title)
    print("URL:", url)

    # Verification:
    assert "Example" in title


# ============================================================
# 3. CSS SELECTORS
# ============================================================

def css_locator_examples(page):
    # Class
    cards = page.locator(".job-card")

    # ID
    search = page.locator("#search")

    # Element
    buttons = page.locator("button")

    # Attribute
    records = page.locator("[data-job-id]")

    # Combined selector
    articles = page.locator("article.job-card")

    print("Cards:", cards.count())
    print("Buttons:", buttons.count())
    print("Records:", records.count())
    print("Articles:", articles.count())


# ============================================================
# 4. TEXT SELECTORS
# ============================================================

def text_locator_example(page):
    # Exact text is useful when wording is stable and unique.
    job = page.get_by_text(
        "Automation Engineer",
        exact=True
    )

    print(job.text_content())


# ============================================================
# 5. ROLE-BASED LOCATORS
# ============================================================

def role_locator_examples(page):
    heading = page.get_by_role(
        "heading",
        name="Automation Operations Portal"
    )

    button = page.get_by_role(
        "button",
        name="Search"
    )

    link = page.get_by_role(
        "link",
        name="Jobs"
    )

    print(heading.text_content())
    print(button.count())
    print(link.count())


# ============================================================
# 6. LABEL LOCATORS
# ============================================================

def label_locator_example(page):
    email = page.get_by_label("Email")

    email.fill("alex@example.com")


# ============================================================
# 7. PLACEHOLDER LOCATORS
# ============================================================

def placeholder_locator_example(page):
    search = page.get_by_placeholder(
        "Search jobs"
    )

    search.fill("Automation")


# ============================================================
# 8. STRICT LOCATOR BEHAVIOUR
# ============================================================

def strict_locator_example(page):
    """
    If an action requires one element but a locator matches
    multiple elements, Playwright can raise a strictness error.

    Bad / ambiguous:
        page.get_by_role("button", name="Open").click()

    Better:
        identify the specific card first, then locate the
        button inside that card.
    """

    selected_job = page.locator(
        ".job-card"
    ).filter(
        has_text="Automation Engineer"
    )

    open_button = selected_job.get_by_role(
        "button",
        name="Open"
    )

    print(
        "Matching Open buttons:",
        open_button.count()
    )


# ============================================================
# 9. COMPLETE DAY 81 PRACTICAL PROGRAM
# ============================================================

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Automation Operations Portal</title>
</head>

<body>
    <main>

        <h1>Automation Operations Portal</h1>

        <form>

            <label for="email">
                Email
            </label>

            <input
                id="email"
                type="email"
                placeholder="Enter email"
            >

            <input
                id="search"
                placeholder="Search jobs"
            >

            <button type="button">
                Search
            </button>

        </form>

        <section>

            <article
                class="job-card"
                data-job-id="JOB-101"
            >
                <h2>
                    Automation Engineer
                </h2>

                <p>
                    Status: Open
                </p>

                <button>
                    Open
                </button>
            </article>

            <article
                class="job-card"
                data-job-id="JOB-102"
            >
                <h2>
                    QA Automation Engineer
                </h2>

                <p>
                    Status: Open
                </p>

                <button>
                    Open
                </button>
            </article>

        </section>

    </main>
</body>
</html>
"""


def run_day_81():
    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            headless=False
        )

        context = browser.new_context()

        page = context.new_page()

        # ----------------------------------------------------
        # Navigation
        # ----------------------------------------------------
        #
        # For a real website:
        # page.goto("https://example.com")
        #
        # Here we use local HTML so the program is self-contained.
        #

        page.set_content(HTML)

        # ----------------------------------------------------
        # Title and URL
        # ----------------------------------------------------

        print("Title:", page.title())
        print("URL:", page.url)

        # ----------------------------------------------------
        # CSS selector
        # ----------------------------------------------------

        job_cards = page.locator(
            ".job-card"
        )

        print(
            "Job cards:",
            job_cards.count()
        )

        # ----------------------------------------------------
        # Text selector
        # ----------------------------------------------------

        automation_job = page.get_by_text(
            "Automation Engineer",
            exact=True
        )

        print(
            "Job:",
            automation_job.text_content()
        )

        # ----------------------------------------------------
        # Role-based locator
        # ----------------------------------------------------

        heading = page.get_by_role(
            "heading",
            name="Automation Operations Portal"
        )

        print(
            "Heading:",
            heading.text_content()
        )

        # ----------------------------------------------------
        # Label locator
        # ----------------------------------------------------

        email = page.get_by_label(
            "Email"
        )

        email.fill(
            "alex@example.com"
        )

        # ----------------------------------------------------
        # Placeholder locator
        # ----------------------------------------------------

        search = page.get_by_placeholder(
            "Search jobs"
        )

        search.fill(
            "Automation"
        )

        # ----------------------------------------------------
        # Strictness / scoped locator
        # ----------------------------------------------------

        selected_job = page.locator(
            ".job-card"
        ).filter(
            has_text="Automation Engineer"
        )

        open_button = selected_job.get_by_role(
            "button",
            name="Open"
        )

        print(
            "Specific Open button count:",
            open_button.count()
        )

        # ----------------------------------------------------
        # Final verification
        # ----------------------------------------------------

        assert page.title() == (
            "Automation Operations Portal"
        )

        assert job_cards.count() == 2

        assert heading.count() == 1

        assert email.count() == 1

        assert search.count() == 1

        assert open_button.count() == 1

        print("Day 81 practical verification: PASSED")

        browser.close()


if __name__ == "__main__":
    run_day_81()


# ============================================================
# QUICK REFERENCE
# ============================================================
#
# Navigation:
#     page.goto(url)
#
# Page information:
#     page.title()
#     page.url
#
# CSS:
#     page.locator(".class")
#     page.locator("#id")
#     page.locator("button")
#     page.locator("[data-id]")
#
# Text:
#     page.get_by_text("Visible text")
#
# Role:
#     page.get_by_role("button", name="Submit")
#
# Label:
#     page.get_by_label("Email")
#
# Placeholder:
#     page.get_by_placeholder("Search jobs")
#
# Count:
#     locator.count()
#
# Text:
#     locator.text_content()
#
# Scoped locator:
#     page.locator(".job-card").filter(
#         has_text="Automation Engineer"
#     )
#
# Core locator principle:
#     Locate the intended element as specifically and
#     semantically as practical. Avoid ambiguous targets.
#
# NEXT ROADMAP:
#     Day 82 — Playwright Interactions
#     - click()
#     - fill()
#     - typing / keys
#     - text_content()
#     - inner_text()
#     - attributes
#     - checkboxes
#     - radio buttons
#     - dropdowns
