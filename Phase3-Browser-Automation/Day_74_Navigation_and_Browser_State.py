"""
DAY 74 — NAVIGATION AND BROWSER STATE
======================================

Phase 3: Browser Automation
Roadmap area: Selenium — Interacting with Pages

DAY 74 COVERAGE
---------------
1. Back navigation
2. Forward navigation
3. Refresh
4. Current URL
5. Page title
6. Page source
7. Tabs and windows
8. Window handles
9. Switching between windows and tabs
10. Closing the intended tab or window safely

INSTALLATION REQUIREMENTS
-------------------------
Run this program with the Phase 3 virtual environment active:

    pip install selenium beautifulsoup4

The program uses authorised offline HTML data pages. It does not scrape or
interact with a third-party website.

IMPORTANT DIFFERENCE
--------------------
driver.close(): closes only the currently selected tab or window.
driver.quit(): closes the complete WebDriver session and every browser window.
"""

from urllib.parse import quote

from bs4 import BeautifulSoup
from selenium import webdriver


# ---------------------------------------------------------------------------
# SECTION 1 — OFFLINE PRACTICE PAGES
# ---------------------------------------------------------------------------
# quote() percent-encodes the HTML so it can be safely placed inside a data URL.

page_one_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Customer Dashboard</title>
</head>
<body>
    <main id="dashboard">
        <h1>Customer Dashboard</h1>
        <p>Account status: Active</p>
    </main>
</body>
</html>
"""

page_two_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Order History</title>
</head>
<body>
    <main id="orders">
        <h1>Order History</h1>
        <p>Orders found: 4</p>
    </main>
</body>
</html>
"""

report_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Activity Report</title>
</head>
<body>
    <main>
        <h1>Activity Report</h1>
        <p>Report status: Ready</p>
    </main>
</body>
</html>
"""

help_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Help Centre</title>
</head>
<body>
    <main>
        <h1>Help Centre</h1>
        <p>Support status: Available</p>
    </main>
</body>
</html>
"""


def make_data_url(html):
    """Convert an HTML string into an encoded offline data URL."""
    return "data:text/html;charset=utf-8," + quote(html)


page_one_url = make_data_url(page_one_html)
page_two_url = make_data_url(page_two_html)
report_url = make_data_url(report_html)
help_url = make_data_url(help_html)


# ---------------------------------------------------------------------------
# SECTION 2 — START MICROSOFT EDGE
# ---------------------------------------------------------------------------

driver = webdriver.Edge()


try:
    # -----------------------------------------------------------------------
    # SECTION 3 — OPEN AND VERIFY THE FIRST PAGE
    # -----------------------------------------------------------------------
    driver.get(page_one_url)

    print(f"First page title: {driver.title}")
    print(
        f"First page URL verified: "
        f"{driver.current_url == page_one_url}"
    )

    # -----------------------------------------------------------------------
    # SECTION 4 — CREATE A BROWSER-HISTORY ENTRY
    # -----------------------------------------------------------------------
    # driver.get() navigates to another page. The previous page becomes a
    # browser-history entry that back() can revisit.
    driver.get(page_two_url)

    print(f"Second page title: {driver.title}")
    print(
        f"Second page URL verified: "
        f"{driver.current_url == page_two_url}"
    )

    # -----------------------------------------------------------------------
    # SECTION 5 — BACK NAVIGATION
    # -----------------------------------------------------------------------
    # back() moves one entry backward through the current tab's history.
    driver.back()

    print(f"Title after back: {driver.title}")
    print(
        f"Back navigation verified: "
        f"{driver.current_url == page_one_url}"
    )

    # -----------------------------------------------------------------------
    # SECTION 6 — FORWARD NAVIGATION
    # -----------------------------------------------------------------------
    # forward() moves one entry forward after a previous back operation.
    driver.forward()

    print(f"Title after forward: {driver.title}")
    print(
        f"Forward navigation verified: "
        f"{driver.current_url == page_two_url}"
    )

    # -----------------------------------------------------------------------
    # SECTION 7 — REFRESH
    # -----------------------------------------------------------------------
    # Save state before refresh so the post-refresh state can be verified.
    url_before_refresh = driver.current_url
    title_before_refresh = driver.title

    driver.refresh()

    print(f"Title after refresh: {driver.title}")
    print(
        f"Refresh URL unchanged: "
        f"{driver.current_url == url_before_refresh}"
    )
    print(
        f"Refresh title unchanged: "
        f"{driver.title == title_before_refresh}"
    )

    # -----------------------------------------------------------------------
    # SECTION 8 — READ THE CURRENT BROWSER STATE
    # -----------------------------------------------------------------------
    # These are WebDriver properties, so they do not use parentheses.
    current_url = driver.current_url
    current_title = driver.title
    current_source = driver.page_source

    print("\nCurrent Browser State")
    print("-" * 50)
    print(f"Current page is Order History: {current_url == page_two_url}")
    print(f"Current title: {current_title}")
    print(f"Page source type: {type(current_source).__name__}")
    print(f"Page source characters: {len(current_source)}")

    # page_source is HTML text, not a screenshot or a WebElement.
    print(
        f"Order heading exists in source: "
        f"{'<h1>Order History</h1>' in current_source}"
    )
    print(
        f"Order count exists in source: "
        f"{'Orders found: 4' in current_source}"
    )

    # Selenium's current HTML source can be parsed with BeautifulSoup.
    source_soup = BeautifulSoup(current_source, "html.parser")
    source_heading = source_soup.select_one("#orders h1")
    source_message = source_soup.select_one("#orders p")

    print(f"Parsed heading: {source_heading.get_text(strip=True)}")
    print(f"Parsed message: {source_message.get_text(strip=True)}")

    # -----------------------------------------------------------------------
    # SECTION 9 — TAB HANDLES AND SWITCHING
    # -----------------------------------------------------------------------
    print("\nTabs and Windows")
    print("-" * 50)

    # A handle is Selenium's unique string identifier for a tab or window.
    original_handle = driver.current_window_handle
    print(f"Initial handle count: {len(driver.window_handles)}")

    # Selenium 4 opens a new tab and automatically switches to it.
    driver.switch_to.new_window("tab")
    report_tab_handle = driver.current_window_handle
    driver.get(report_url)

    print(f"New tab title: {driver.title}")
    print(
        f"New tab has a different handle: "
        f"{report_tab_handle != original_handle}"
    )
    print(f"Handle count after new tab: {len(driver.window_handles)}")

    # Switching requires the exact handle of the intended browsing context.
    driver.switch_to.window(original_handle)
    print(f"Title after switching to original: {driver.title}")
    print(
        f"Original tab restored: "
        f"{driver.current_window_handle == original_handle}"
    )

    # -----------------------------------------------------------------------
    # SECTION 10 — CLOSE ONLY THE INTENDED TAB
    # -----------------------------------------------------------------------
    # First select the report tab. close() always closes the current context.
    driver.switch_to.window(report_tab_handle)
    print(f"Closing intended tab: {driver.title}")
    driver.close()

    # After closing a context, explicitly select a known surviving handle.
    driver.switch_to.window(original_handle)
    print(f"Handle count after closing tab: {len(driver.window_handles)}")
    print(f"Active title after tab closure: {driver.title}")

    # -----------------------------------------------------------------------
    # SECTION 11 — OPEN AND CLOSE A SEPARATE WINDOW
    # -----------------------------------------------------------------------
    driver.switch_to.new_window("window")
    help_window_handle = driver.current_window_handle
    driver.get(help_url)

    print(f"New window title: {driver.title}")
    print(
        f"New window has a different handle: "
        f"{help_window_handle != original_handle}"
    )
    print(f"Handle count with new window: {len(driver.window_handles)}")

    # close() affects only the selected Help Centre window.
    print(f"Closing intended window: {driver.title}")
    driver.close()

    # Return to the original surviving tab before any further browser action.
    driver.switch_to.window(original_handle)
    print(f"Final handle count: {len(driver.window_handles)}")
    print(f"Final active title: {driver.title}")


finally:
    # -----------------------------------------------------------------------
    # SECTION 12 — GUARANTEED CLEANUP
    # -----------------------------------------------------------------------
    # quit() closes every remaining window and ends the WebDriver session.
    driver.quit()
    print("Browser closed safely.")


"""
EXPECTED OUTPUT SUMMARY
-----------------------
The exact page-source character count can vary slightly by browser version.
The important verified results are:

- Customer Dashboard opens first.
- Order History opens second.
- back() restores Customer Dashboard.
- forward() restores Order History.
- refresh() keeps the same URL and title.
- page_source is a string containing the expected HTML.
- BeautifulSoup extracts "Order History" and "Orders found: 4".
- Opening a new tab increases the handle count from 1 to 2.
- The report tab has a different handle from the original tab.
- The intended report tab is selected before close().
- After closing the report tab, the handle count returns to 1.
- Opening a separate window increases the handle count to 2.
- The intended Help Centre window is closed.
- The original Order History tab survives and becomes active again.
- quit() closes the browser safely.

COMMON ERRORS TO AVOID
----------------------
1. Do not write driver.current_url() or driver.title(). They are properties.
2. Do not call close() until the intended handle is selected.
3. Do not continue using a handle after its tab or window has been closed.
4. After close(), switch to a known surviving handle.
5. Do not confuse close() with quit().
6. Do not treat page_source as a screenshot or WebElement.
7. Keep quit() inside finally so cleanup runs after success or failure.
"""
