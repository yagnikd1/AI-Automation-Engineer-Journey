"""
DAY 77 — JAVASCRIPT-LOADED AND SCROLLING CONTENT
Phase 3: Browser Automation

Canonical coverage
------------------
1. Recognising JavaScript-loaded content
2. Scrolling with JavaScript
3. Scrolling an element into view
4. Load-more buttons
5. Infinite scrolling
6. Reliable stopping conditions
7. Duplicate prevention during repeated loads

This file is both a revision reference and a runnable local Selenium demonstration.
It uses an authorised local HTML page, so no external website is automated.
"""

from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# ---------------------------------------------------------------------------
# 1. ESSENTIAL NOTES
# ---------------------------------------------------------------------------
# requests downloads the original server response but does not normally run
# page JavaScript. BeautifulSoup parses the HTML it receives. Selenium controls
# a real browser, executes JavaScript, and can wait for the DOM to change.
#
# Missing content does not automatically prove JavaScript loading. Also check:
# incorrect locators, wrong tabs/windows/frames, consent or login screens,
# failed scripts, Shadow DOM, and elements that never reach the expected state.
#
# JavaScript scrolling:
#   window.scrollBy(0, 600) -> relative movement from the current position.
#   window.scrollTo(0, document.body.scrollHeight) -> absolute page bottom.
#   arguments[0].scrollIntoView(...) -> move a known element into the viewport.
#
# A successful click is not proof that new records loaded. Record an old state
# (usually card count), act, then wait for a measurable state change.
#
# Re-find dynamic buttons inside loops. JavaScript may replace a DOM node,
# making a previously stored WebElement stale.
#
# Strong stopping conditions include: button disappears, button becomes
# disabled, end message appears, expected total is reached, no new IDs appear,
# or a maximum safety limit is reached. Combine a page signal with a safety cap.
#
# Use a set of stable record IDs to prevent duplicates. Do not rely only on
# element indexes or visible positions because dynamic pages can reorder items.


# ---------------------------------------------------------------------------
# 2. AUTHORISED LOCAL DYNAMIC PAGE
# ---------------------------------------------------------------------------
PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dynamic Shipment Feed</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .shipment-card {
            border: 1px solid #777; margin: 20px 0; padding: 20px;
            min-height: 100px;
        }
        #load-more-button { padding: 12px 20px; margin-top: 20px; }
        #end-message { color: darkgreen; font-weight: bold; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>Dynamic Shipment Feed</h1>
    <p id="loading-status">Loading initial shipments...</p>
    <section id="shipment-list"></section>
    <button id="load-more-button" disabled>Load More Shipments</button>
    <p id="end-message" hidden>All shipments loaded</p>

    <script>
        const shipmentBatches = [
            [
                {id: "SH-601", cargo: "Medical Supplies", destination: "Berlin"},
                {id: "SH-602", cargo: "Office Equipment", destination: "Toronto"}
            ],
            [
                {id: "SH-603", cargo: "Replacement Parts", destination: "Oslo"},
                {id: "SH-602", cargo: "Office Equipment", destination: "Toronto"}
            ],
            [
                {id: "SH-604", cargo: "Laboratory Equipment", destination: "Lisbon"},
                {id: "SH-605", cargo: "Safety Equipment", destination: "Helsinki"}
            ]
        ];

        let batchIndex = 0;

        function addBatch() {
            const list = document.getElementById("shipment-list");
            shipmentBatches[batchIndex].forEach((shipment) => {
                const card = document.createElement("article");
                card.className = "shipment-card";
                card.setAttribute("data-id", shipment.id);
                card.innerHTML = `
                    <h2 class="cargo">${shipment.cargo}</h2>
                    <p class="destination">${shipment.destination}</p>`;
                list.appendChild(card);
            });

            batchIndex += 1;
            if (batchIndex >= shipmentBatches.length) {
                document.getElementById("load-more-button").remove();
                document.getElementById("end-message").hidden = false;
            }
        }

        setTimeout(() => {
            addBatch();
            document.getElementById("loading-status").textContent =
                "Initial shipments ready";
            const button = document.getElementById("load-more-button");
            if (button) button.disabled = false;
        }, 1200);

        document.getElementById("load-more-button").addEventListener("click", () => {
            const button = document.getElementById("load-more-button");
            button.disabled = true;
            button.textContent = "Loading...";
            setTimeout(() => {
                addBatch();
                const updated = document.getElementById("load-more-button");
                if (updated) {
                    updated.disabled = false;
                    updated.textContent = "Load More Shipments";
                }
            }, 800);
        });
    </script>
</body>
</html>
"""


def collect_unique_shipments(driver, wait, max_load_attempts=10):
    """Load repeated batches and return unique shipment dictionaries."""
    cards_locator = (By.CSS_SELECTOR, ".shipment-card")
    button_locator = (By.ID, "load-more-button")
    seen_ids = set()
    unique_shipments = []

    wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, "loading-status"), "Initial shipments ready"
        )
    )
    wait.until(EC.presence_of_all_elements_located(cards_locator))
    print("Initial JavaScript content loaded")

    for attempt in range(1, max_load_attempts + 1):
        cards = driver.find_elements(*cards_locator)

        for card in cards:
            shipment_id = card.get_attribute("data-id")
            if not shipment_id or shipment_id in seen_ids:
                continue

            seen_ids.add(shipment_id)
            unique_shipments.append(
                {
                    "id": shipment_id,
                    "cargo": card.find_element(By.CSS_SELECTOR, ".cargo").text,
                    "destination": card.find_element(
                        By.CSS_SELECTOR, ".destination"
                    ).text,
                }
            )

        print(
            f"Attempt {attempt}: {len(cards)} displayed cards, "
            f"{len(unique_shipments)} unique shipments"
        )

        buttons = driver.find_elements(*button_locator)
        if not buttons:
            print("Stopped: load-more button disappeared")
            break

        driver.execute_script(
            """
            arguments[0].scrollIntoView({
                behavior: "instant",
                block: "center"
            });
            """,
            buttons[0],
        )

        old_count = len(cards)
        button = wait.until(EC.element_to_be_clickable(button_locator))
        button.click()

        try:
            wait.until(
                lambda browser: len(browser.find_elements(*cards_locator))
                > old_count
            )
        except TimeoutException:
            print("Stopped: no new cards appeared")
            break
    else:
        print("Stopped: maximum attempts reached")

    return unique_shipments, cards_locator


def main():
    page_file = Path("dynamic_shipment_feed.html").resolve()
    page_file.write_text(PAGE_HTML, encoding="utf-8")

    driver = webdriver.Edge()
    wait = WebDriverWait(driver, timeout=5, poll_frequency=0.25)

    try:
        driver.get(page_file.as_uri())
        print(f"Title: {driver.title}")

        shipments, cards_locator = collect_unique_shipments(driver, wait)
        wait.until(EC.visibility_of_element_located((By.ID, "end-message")))

        print("\nUNIQUE SHIPMENT REPORT")
        print("-" * 60)
        for shipment in shipments:
            print(
                f'{shipment["id"]} | {shipment["cargo"]} | '
                f'{shipment["destination"]}'
            )
        print("-" * 60)
        print(f"Displayed cards: {len(driver.find_elements(*cards_locator))}")
        print(f"Unique shipments: {len(shipments)}")

    except TimeoutException as error:
        print(f"Dynamic-content operation timed out: {error}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()


# EXPECTED RESULT
# Title: Dynamic Shipment Feed
# Initial JavaScript content loaded
# Attempt 1: 2 displayed cards, 2 unique shipments
# Attempt 2: 4 displayed cards, 3 unique shipments
# Attempt 3: 6 displayed cards, 5 unique shipments
# Stopped: load-more button disappeared
# Displayed cards: 6
# Unique shipments: 5
