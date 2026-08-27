"""
Day 80 - Why Playwright and Installation
=========================================

Complete revision notes and verified first-session example for the
AI Automation Engineer Journey, Phase 3 - Browser Automation.

Canonical Day 80 coverage
-------------------------
1. Why Playwright exists
2. Selenium versus Playwright
3. Supported browser engines
4. Installing the Python package
5. Installing Playwright browsers
6. Browser, context, and page architecture
7. Synchronous versus asynchronous APIs
8. First Playwright browser session

Verified learning environment
-----------------------------
- Python: 3.14
- Virtual environment: Phase 3 - Browser Automation/myenv
- Playwright: 1.62.0 during the lesson
- Browser installed: Chromium only
- Operating system: Windows 10 (not in the current officially supported
  Windows list, but package installation and a real Chromium launch both
  succeeded during the lesson)

Important environment rule
--------------------------
Activate myenv in every new PowerShell window:

    & ".\\Phase 3 - Browser Automation\\myenv\\Scripts\\Activate.ps1"

Verify the selected interpreter:

    python -c "import sys; print(sys.executable)"

The path must end with:

    Phase 3 - Browser Automation\\myenv\\Scripts\\python.exe

Installation commands
---------------------
Install the Python library in the active environment:

    python -m pip install playwright

Install only Chromium to reduce download and storage use:

    python -m playwright install chromium

These commands do different jobs:

- pip installs the Python Playwright package and Python dependencies.
- playwright install downloads compatible browser binaries.

Playwright normally stores its downloaded browsers in a shared Windows-user
cache such as:

    %LOCALAPPDATA%\\ms-playwright

The Playwright Python package remains isolated inside myenv, while Chromium
can live in the shared browser cache. Removing a global pip installation does
not by itself remove the separately downloaded Chromium cache.

Why Playwright exists
---------------------
Playwright was designed for modern end-to-end browser automation. It combines
browser control, reliable locators, automatic waiting, isolated sessions,
network tools, screenshots, videos, and traces in one automation system.

Important strengths:
- automatic waiting before actions;
- Chromium, Firefox, and WebKit through one API;
- lightweight isolated BrowserContext objects;
- role-, label-, placeholder-, text-, and CSS-based locators;
- network inspection and interception;
- built-in screenshots, tracing, video, and debugging tools;
- synchronous and asynchronous Python APIs.

Selenium versus Playwright
--------------------------
Selenium is not obsolete. It remains widely used and has a mature WebDriver
ecosystem. Playwright provides a more integrated model for modern web apps.

Selenium                         Playwright
--------                         ----------
driver                           browser + context + page
driver.get(url)                  page.goto(url)
window/tab handle                Page object
profile/session                  BrowserContext
frequent explicit waits          built-in action auto-waiting
screenshots + external tooling   screenshots + video + traces + inspector

Supported browser engines
-------------------------
- Chromium: the open-source engine family related to Chrome and Edge.
- Firefox: Playwright's patched Firefox build, not ordinary branded Firefox.
- WebKit: the engine family related to Safari, not installed Safari itself.

Playwright can also automate installed Chrome or Edge through browser channels,
but bundled Chromium is the usual default for learning and most testing.

Architecture
------------
Playwright
    -> Browser
        -> BrowserContext
            -> Page

- Playwright: entry point that exposes browser engines.
- Browser: a running browser process.
- BrowserContext: an isolated environment with its own cookies, storage, and
  sessions. Multiple contexts can represent different users efficiently.
- Page: a browser tab or popup inside a context.

The method context.new_page() creates a tab. The variable receiving its return
value is the Page object:

    page = context.new_page()

Synchronous versus asynchronous APIs
------------------------------------
Synchronous API:

    from playwright.sync_api import sync_playwright

It reads sequentially and matches the learner's current Selenium and Python
knowledge. It is the correct starting point for this roadmap.

Asynchronous API:

    from playwright.async_api import async_playwright

It uses async def, await, and async with. It is useful when a project already
uses asyncio or must coordinate asynchronous work. Async is not automatically
better for every browser script. Python async foundations are assigned to Day
84 and full Async Playwright to Day 85.

Locator concept
---------------
A locator is a reusable query for one or more elements. It resolves against the
current page when an operation such as count(), click(), or text_content() is
performed. Detailed locator strategies belong to Day 81.

Cleanup rule
------------
The with sync_playwright() block manages the Playwright service lifecycle.
Explicit context.close() and browser.close() make resource ownership clear.
For larger scripts, cleanup should remain guaranteed when errors occur.

Official documentation
----------------------
- https://playwright.dev/python/docs/library
- https://playwright.dev/python/docs/intro
- https://playwright.dev/python/docs/browsers
"""

from pathlib import Path

from playwright.sync_api import sync_playwright


PRACTICE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Automation Operations Portal</title>
</head>
<body>
    <main>
        <h1>Automation Operations Portal</h1>

        <article class="job-card" data-job-id="JOB-801">
            <h2>Inventory Synchronization</h2>
            <p class="status">Completed</p>
        </article>

        <article class="job-card" data-job-id="JOB-802">
            <h2>Customer Report Export</h2>
            <p class="status">Running</p>
        </article>
    </main>
</body>
</html>
"""


def run_first_session() -> None:
    """Launch Chromium, inspect a safe local page, and save evidence."""
    screenshot_path = Path(
        "day_80_first_playwright_session.png"
    ).resolve()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        page.set_content(PRACTICE_HTML)

        heading = page.locator("h1")
        job_cards = page.locator(".job-card")

        page.screenshot(
            path=str(screenshot_path),
            full_page=True,
        )

        print(f"Page title: {page.title()}")
        print(f"Heading: {heading.text_content()}")
        print(f"Job cards: {job_cards.count()}")
        print(f"Screenshot exists: {screenshot_path.exists()}")

        context.close()
        browser.close()


if __name__ == "__main__":
    run_first_session()

