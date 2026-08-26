"""
Day 79 - Screenshots and Selenium Checkpoint
=============================================

Canonical coverage
------------------
1. driver.save_screenshot(): captures the current browser viewport.
2. element.screenshot(): captures one element's rectangular area.
3. Timestamped evidence filenames that do not overwrite earlier runs.
4. Success screenshots and failure screenshots.
5. Structured logging with INFO and ERROR records.
6. A complete Selenium checkpoint: overlay, form, dynamic content,
   verification, evidence collection, exception propagation, and cleanup.

Important rules
---------------
- Wait for and verify the required state before capturing evidence.
- A screenshot is evidence; it does not prove that an assertion passed.
- Re-raise failures after logging and screenshot capture so automation is not
  falsely reported as successful.
- Use finally to close the browser reliably.
- If JavaScript removes a DOM element, do not reuse the stored WebElement.
"""

import logging
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


PORTAL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Warranty Claim Portal</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        #privacy-overlay {
            position: fixed; inset: 0; background: rgba(0, 0, 0, .65);
            display: flex; align-items: center; justify-content: center;
            z-index: 10;
        }
        #overlay-card, form, #claim-result {
            background: white; padding: 20px; border: 1px solid #999;
            max-width: 520px;
        }
        form, #claim-result { margin-top: 20px; }
        label { display: block; margin-top: 14px; }
        input, select, textarea, button { margin-top: 6px; padding: 8px; }
        #loading-message { margin-top: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <div id="privacy-overlay">
        <div id="overlay-card">
            <p>Authorized training portal</p>
            <button id="close-overlay">Continue</button>
        </div>
    </div>

    <h1>Warranty Claim Review Portal</h1>
    <form id="claim-form">
        <label for="claim-number">Claim number</label>
        <input id="claim-number" type="text">

        <label for="customer-name">Customer name</label>
        <input id="customer-name" type="text">

        <label for="product-category">Product category</label>
        <select id="product-category">
            <option value="">Choose a category</option>
            <option value="laptop">Laptop</option>
            <option value="tablet">Tablet</option>
            <option value="monitor">Monitor</option>
        </select>

        <label for="issue-details">Issue details</label>
        <textarea id="issue-details"></textarea>

        <label>
            <input id="proof-confirmed" type="checkbox">
            Purchase proof verified
        </label>
        <button id="submit-claim" type="submit">Review Claim</button>
    </form>

    <div id="loading-message" hidden>Reviewing warranty claim...</div>
    <section id="claim-result" hidden></section>

    <script>
        document.getElementById("close-overlay").addEventListener(
            "click", () => document.getElementById("privacy-overlay").remove()
        );

        document.getElementById("claim-form").addEventListener(
            "submit",
            function (event) {
                event.preventDefault();
                const claimNumber = document.getElementById("claim-number").value.trim();
                const customer = document.getElementById("customer-name").value.trim();
                const category = document.getElementById("product-category").value;
                const issue = document.getElementById("issue-details").value.trim();
                const proof = document.getElementById("proof-confirmed").checked;
                const loader = document.getElementById("loading-message");
                const result = document.getElementById("claim-result");

                loader.hidden = false;
                result.hidden = true;

                setTimeout(function () {
                    const approved = claimNumber === "WC-901"
                        && customer === "Morgan Reed"
                        && category === "laptop"
                        && issue.length >= 10
                        && proof;

                    result.innerHTML = `
                        <h2>Claim Review Complete</h2>
                        <p id="result-status">Status: ${
                            approved
                                ? "Approved for inspection"
                                : "Additional information required"
                        }</p>
                        <p id="result-reference">Reference: ${claimNumber}</p>
                    `;
                    loader.hidden = true;
                    result.hidden = false;
                    document.title = "Warranty Claim Reviewed";
                }, 1400);
            }
        );
    </script>
</body>
</html>
"""


def configure_logging() -> logging.Logger:
    """Create console and UTF-8 file logging for the checkpoint."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler("warranty_claim_automation.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger("warranty_claim_checkpoint")


def create_evidence_path(
    directory: Path,
    label: str,
    extension: str = "png",
) -> Path:
    """Return a Windows-safe, collision-resistant timestamped path."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
    return directory / f"{timestamp}_{label}.{extension}"


def create_portal(path: Path) -> None:
    """Create the authorized offline practice portal."""
    path.write_text(PORTAL_HTML, encoding="utf-8")


def run_checkpoint() -> None:
    """Run the complete Day 79 Selenium checkpoint."""
    logger = configure_logging()
    evidence_directory = Path("warranty_claim_evidence")
    evidence_directory.mkdir(parents=True, exist_ok=True)

    portal_path = Path("warranty_claim_portal.html").resolve()
    create_portal(portal_path)

    driver = None

    try:
        logger.info("Starting Microsoft Edge")
        driver = webdriver.Edge()
        wait = WebDriverWait(driver, timeout=6, poll_frequency=0.25)

        logger.info("Opening portal: %s", portal_path.as_uri())
        driver.get(portal_path.as_uri())
        print(f"Initial title: {driver.title}")

        # Read state before the click because JavaScript removes the overlay.
        overlay = wait.until(
            EC.visibility_of_element_located((By.ID, "privacy-overlay"))
        )
        overlay_initially_visible = overlay.is_displayed()

        wait.until(
            EC.element_to_be_clickable((By.ID, "close-overlay"))
        ).click()
        wait.until(
            EC.invisibility_of_element_located((By.ID, "privacy-overlay"))
        )
        print(f"Overlay initially visible: {overlay_initially_visible}")
        print("Overlay closed: True")

        claim_input = wait.until(
            EC.visibility_of_element_located((By.ID, "claim-number"))
        )
        customer_input = driver.find_element(By.ID, "customer-name")
        issue_input = driver.find_element(By.ID, "issue-details")
        proof_checkbox = driver.find_element(By.ID, "proof-confirmed")
        category = Select(driver.find_element(By.ID, "product-category"))

        claim_input.send_keys("WC-901")
        customer_input.send_keys("Morgan Reed")
        category.select_by_value("laptop")
        issue_input.send_keys(
            "The laptop display flickers during normal operation."
        )
        if not proof_checkbox.is_selected():
            proof_checkbox.click()

        form_checks = {
            "claim": claim_input.get_attribute("value") == "WC-901",
            "customer": customer_input.get_attribute("value") == "Morgan Reed",
            "category": category.first_selected_option.text == "Laptop",
            "proof": proof_checkbox.is_selected(),
        }
        failed_fields = [name for name, passed in form_checks.items() if not passed]
        if failed_fields:
            raise AssertionError(f"Form verification failed: {failed_fields}")
        logger.info("Warranty form completed and verified")

        wait.until(
            EC.element_to_be_clickable((By.ID, "submit-claim"))
        ).click()
        wait.until(
            EC.visibility_of_element_located((By.ID, "loading-message"))
        )
        wait.until(
            EC.invisibility_of_element_located((By.ID, "loading-message"))
        )
        result_panel = wait.until(
            EC.visibility_of_element_located((By.ID, "claim-result"))
        )
        wait.until(EC.title_is("Warranty Claim Reviewed"))

        actual_status = driver.find_element(By.ID, "result-status").text
        actual_reference = driver.find_element(By.ID, "result-reference").text
        expected_status = "Status: Approved for inspection"
        expected_reference = "Reference: WC-901"

        if actual_status != expected_status:
            raise AssertionError(
                f"Status mismatch: expected {expected_status!r}, "
                f"received {actual_status!r}"
            )
        if actual_reference != expected_reference:
            raise AssertionError(
                f"Reference mismatch: expected {expected_reference!r}, "
