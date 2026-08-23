"""
Day 76 - Selenium Expected Conditions
=====================================

Canonical topics covered:
1. Presence of an element
2. Visibility of an element
3. Element clickability
4. Element invisibility
5. Waiting for text
6. URL conditions
7. Title conditions
8. Choosing the correct condition
9. Timeout handling
10. Diagnosing timing-related failures

This runnable example creates a local dynamic support portal. A local file URL
is used because Edge may not expose fragment changes reliably for a data: URL.
"""

from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Loading Support Portal</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 30px; }
        #loading-overlay { padding: 15px; background: #ffe9a8; }
        #ticket-panel {
            display: none; margin-top: 20px; padding: 20px;
            border: 2px solid #333;
        }
        #review-button { margin-top: 15px; padding: 10px 18px; }
        #confirmation {
            display: none; margin-top: 15px; color: green;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>Support Ticket Portal</h1>
    <div id="loading-overlay">Loading ticket information...</div>
    <section id="ticket-panel">
        <h2 id="ticket-title">Priority Ticket</h2>
        <p id="ticket-status">Preparing ticket...</p>
        <button id="review-button" disabled>Review Ticket</button>
        <p id="confirmation">Ticket opened for review</p>
    </section>
    <script>
        setTimeout(function () {
            document.getElementById("ticket-panel").style.display = "block";
        }, 2000);

        setTimeout(function () {
            document.getElementById("loading-overlay").style.display = "none";
            document.getElementById("ticket-status").textContent =
                "Ready for review";
            document.getElementById("review-button").disabled = false;
            document.title = "Support Portal - Ticket Ready";
        }, 4000);

        document.getElementById("review-button").addEventListener(
            "click",
            function () {
                document.getElementById("confirmation").style.display =
                    "block";
                window.location.hash = "ticket-review";
                document.title = "Ticket Review Open";
            }
        );
    </script>
</body>
</html>
"""


def build_local_portal() -> str:
    """Write the demonstration page and return its file URL."""
    html_file = Path("day_76_support_portal.html").resolve()
    html_file.write_text(HTML, encoding="utf-8")
    return html_file.as_uri()


def run_expected_conditions_demo() -> None:
    """Run and diagnose a complete expected-conditions workflow."""
    driver = webdriver.Edge()
    wait = WebDriverWait(driver, 6, poll_frequency=0.25)

    try:
        driver.get(build_local_portal())
        print(f"Initial title: {driver.title}")

        # Presence proves DOM existence; it does not prove visibility.
        panel_locator = (By.ID, "ticket-panel")
        ticket_panel = wait.until(EC.presence_of_element_located(panel_locator))
        print("Ticket panel present: True")
        print(f"Panel initially displayed: {ticket_panel.is_displayed()}")

        # Visibility proves that the panel exists and is displayed.
        wait.until(EC.visibility_of_element_located(panel_locator))
        print("Ticket panel visible: True")

        # Wait for a blocking loader or overlay to disappear.
        wait.until(
            EC.invisibility_of_element_located((By.ID, "loading-overlay"))
        )
        print("Loading overlay invisible: True")

        # Text conditions return a successful Boolean-like result, not the text.
        status_locator = (By.ID, "ticket-status")
        wait.until(
            EC.text_to_be_present_in_element(status_locator, "Ready for review")
        )
        status = driver.find_element(*status_locator).text
        print(f"Ticket status: {status}")

        # Partial title check for the dynamically updated ready state.
        wait.until(EC.title_contains("Ticket Ready"))
        print(f"Ready-page title: {driver.title}")

        # Clickability requires the button to be visible and enabled.
        review_button = wait.until(
            EC.element_to_be_clickable((By.ID, "review-button"))
        )
        print(f"Review button enabled: {review_button.is_enabled()}")

        old_url = driver.current_url
        review_button.click()

        # One condition proves change; the next verifies the destination marker.
        wait.until(EC.url_changes(old_url))
        wait.until(EC.url_contains("#ticket-review"))
        print("URL changed after click: True")
        print(f"Review hash detected: {'#ticket-review' in driver.current_url}")

        # Exact title check verifies the final page state.
        wait.until(EC.title_is("Ticket Review Open"))
        print(f"Final title: {driver.title}")

        confirmation = wait.until(
            EC.visibility_of_element_located((By.ID, "confirmation"))
        )
        print(f"Confirmation: {confirmation.text}")

        # An optional control receives a short independent timeout.
        optional_locator = (By.ID, "export-button")
        try:
            WebDriverWait(driver, 1, poll_frequency=0.25).until(
                EC.element_to_be_clickable(optional_locator)
            )
            print("Export button available: True")
        except TimeoutException:
            matches = driver.find_elements(*optional_locator)
            print("Export button available: False")
            print(f"Export locator matches: {len(matches)}")
            print("Optional export-button timeout handled safely.")

    except TimeoutException:
        # Critical failure diagnostics: page identity and current browser state.
        print("A critical expected condition timed out.")
        print(f"Current URL: {driver.current_url}")
        print(f"Current title: {driver.title}")
        raise
    finally:
        driver.quit()


if __name__ == "__main__":
    run_expected_conditions_demo()
