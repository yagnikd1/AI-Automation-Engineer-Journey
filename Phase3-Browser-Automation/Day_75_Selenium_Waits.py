"""
Day 75 - Selenium Waits
AI Automation Engineer Journey | Phase 3: Browser Automation

This reference file contains:
1. The completed rapid revision program: Website Incident Triage Report.
2. The main Day 75 practical: implicit and explicit Selenium waits.
3. Notes explaining polling, timeouts, expected conditions, and time.sleep().

Run the two demonstrations separately by changing RUN_SECTION below.
"""

import csv
from urllib.parse import quote

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


RUN_SECTION = "waits"  # Change to "revision" to run the revision program.


def run_revision_program():
    """Revise Python, BeautifulSoup, Selenium, CSV, and tab handling."""

    dashboard_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head><meta charset="UTF-8"><title>Website Incident Dashboard</title></head>
    <body>
        <main id="incident-dashboard">
            <h1>Website Incident Dashboard</h1>
            <article class="incident unresolved" data-incident-id="INC-401">
                <h2 class="service">Payment API</h2>
                <p class="severity">Severity: 5</p>
                <p class="response-time">Response time: 18 minutes</p>
                <p class="status">Unresolved</p>
            </article>
            <article class="incident resolved" data-incident-id="INC-402">
                <h2 class="service">Customer Portal</h2>
                <p class="severity">Severity: 2</p>
                <p class="response-time">Response time: 9 minutes</p>
                <p class="status">Resolved</p>
            </article>
            <article class="incident unresolved" data-incident-id="INC-403">
                <h2 class="service">Order Processor</h2>
                <p class="severity">Severity: 4</p>
                <p class="response-time">Response time: 27 minutes</p>
                <p class="status">Unresolved</p>
            </article>
            <article class="incident unresolved" data-incident-id="INC-404">
                <h2 class="service">Email Service</h2>
                <p class="severity">Severity: unknown</p>
                <p class="response-time">Response time: 12 minutes</p>
                <p class="status">Unresolved</p>
            </article>
        </main>
    </body>
    </html>
    """

    driver = webdriver.Edge()

    try:
        driver.get("data:text/html;charset=utf-8," + quote(dashboard_html))
        print("Dashboard title:", driver.title)

        selenium_cards = driver.find_elements(By.CSS_SELECTOR, ".incident")
        print("Incident cards found:", len(selenium_cards))

        # Parse the browser's current HTML, not a separate network request.
        soup = BeautifulSoup(driver.page_source, "html.parser")
        incidents = []

        for card in soup.select(".incident"):
            try:
                severity = int(
                    card.select_one(".severity")
                    .get_text(strip=True)
                    .replace("Severity:", "")
                    .strip()
                )
                response_minutes = int(
                    card.select_one(".response-time")
                    .get_text(strip=True)
                    .replace("Response time:", "")
                    .replace("minutes", "")
                    .strip()
                )
                incidents.append(
                    {
                        "incident_id": card.get("data-incident-id"),
                        "service": card.select_one(".service").get_text(strip=True),
                        "severity": severity,
                        "response_minutes": response_minutes,
                        "status": card.select_one(".status").get_text(strip=True),
                    }
                )
            except (AttributeError, TypeError, ValueError) as error:
                print(f"Skipped {card.get('data-incident-id', 'Unknown')}: {error}")

        unresolved = [item for item in incidents if item["status"] == "Unresolved"]
        unresolved.sort(key=lambda item: item["severity"], reverse=True)

        total_minutes = sum(item["response_minutes"] for item in unresolved)
        average_minutes = total_minutes / len(unresolved) if unresolved else 0
        highest_priority = max(
            unresolved,
            key=lambda item: item["severity"],
            default=None,
        )

        print("Unresolved valid incidents:", len(unresolved))
        print("Total response time:", total_minutes)
        print(f"Average response time: {average_minutes:.2f}")
        if highest_priority:
            print("Highest-priority service:", highest_priority["service"])

        with open(
            "website_incident_report.csv",
            "w",
            newline="",
            encoding="utf-8",
        ) as csv_file:
            fieldnames = [
                "incident_id",
                "service",
                "severity",
                "response_minutes",
                "status",
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(unresolved)

        dashboard_handle = driver.current_window_handle
        summary_html = f"""
        <html><head><title>Incident Report Summary</title></head>
        <body><h1>Incident Report Summary</h1>
        <p>Unresolved valid incidents: {len(unresolved)}</p>
        <p>Average response time: {average_minutes:.2f} minutes</p></body></html>
        """
        driver.switch_to.new_window("tab")
        driver.get("data:text/html;charset=utf-8," + quote(summary_html))
        print("Report tab title:", driver.title)
        driver.close()
        driver.switch_to.window(dashboard_handle)
        print("Returned to:", driver.title)

    finally:
        driver.quit()


def build_dynamic_page():
    """Return a page whose ticket card is inserted two seconds after load."""

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head><meta charset="UTF-8"><title>Dynamic Support Portal</title></head>
    <body>
        <h1>Support Portal</h1>
        <div id="ticket-area">Loading ticket...</div>
        <script>
            setTimeout(() => {
                document.getElementById("ticket-area").innerHTML = `
                    <section id="ticket-card">
                        <h2>Priority Ticket</h2>
                        <p class="status">Ready for review</p>
                        <button id="review-button">Review Ticket</button>
                    </section>
                `;
            }, 2000);
        </script>
    </body>
    </html>
    """


def demonstrate_waits():
    """Demonstrate immediate lookup, implicit wait, and explicit wait."""

    page_url = "data:text/html;charset=utf-8," + quote(build_dynamic_page())

    # 1. Immediate search: the dynamic element does not exist yet.
    driver = webdriver.Edge()
    try:
        driver.get(page_url)
        try:
            driver.find_element(By.ID, "ticket-card")
        except NoSuchElementException:
            print("Immediate search: ticket not available yet")
    finally:
        driver.quit()

    # 2. Implicit wait: global maximum delay for later element searches.
    driver = webdriver.Edge()
    driver.implicitly_wait(5)
    try:
        driver.get(page_url)
        ticket = driver.find_element(By.ID, "ticket-card")
        print("Implicit wait found:", ticket.find_element(By.TAG_NAME, "h2").text)
    finally:
        driver.quit()

    # 3. Explicit wait: wait for precise, named conditions.
    driver = webdriver.Edge()
    try:
        driver.get(page_url)
        wait = WebDriverWait(driver, timeout=5, poll_frequency=0.25)

        ticket = wait.until(
            EC.visibility_of_element_located((By.ID, "ticket-card"))
        )
        review_button = wait.until(
            EC.element_to_be_clickable((By.ID, "review-button"))
        )

        print("Ticket found:", ticket.find_element(By.TAG_NAME, "h2").text)
        print("Status:", ticket.find_element(By.CLASS_NAME, "status").text)
        print("Review button enabled:", review_button.is_enabled())

        short_wait = WebDriverWait(driver, timeout=1, poll_frequency=0.2)
        try:
            short_wait.until(
                EC.element_to_be_clickable((By.ID, "export-button"))
            )
        except TimeoutException:
            print("Export button was not available within 1 second")
    finally:
        driver.quit()


if __name__ == "__main__":
    if RUN_SECTION == "revision":
        run_revision_program()
    elif RUN_SECTION == "waits":
        demonstrate_waits()
    else:
        raise ValueError("RUN_SECTION must be 'revision' or 'waits'.")

