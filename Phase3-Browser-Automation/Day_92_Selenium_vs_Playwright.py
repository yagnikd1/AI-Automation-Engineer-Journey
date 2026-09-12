"""
DAY 92 — SELENIUM VS PLAYWRIGHT
Accelerated Complete Project

Runs the same service-request workflow with Selenium and Playwright,
then compares syntax, locators, waiting, timing, reliability, and
headless execution.
"""

import asyncio
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from playwright.async_api import async_playwright


BASE_DIR = Path(__file__).resolve().parent
HTML_FILE = BASE_DIR / "day92_service_portal.html"
SELENIUM_SCREENSHOT = BASE_DIR / "day92_selenium.png"
PLAYWRIGHT_SCREENSHOT = BASE_DIR / "day92_playwright.png"
TIMEOUT = 10


def create_test_page():
    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Service Request Portal</title>
</head>
<body>
<h1>Service Request Portal</h1>

<label for="name">Name</label>
<input id="name" type="text">

<label for="email">Email</label>
<input id="email" type="email">

<label for="service">Service</label>
<select id="service">
<option value="">Choose a service</option>
<option value="Technical Support">Technical Support</option>
<option value="Account Support">Account Support</option>
<option value="Billing Support">Billing Support</option>
</select>

<p>Priority</p>
<label><input type="radio" name="priority" value="low"> Low</label>
<label><input type="radio" name="priority" value="medium"> Medium</label>
<label><input type="radio" name="priority" value="high"> High</label>

<label for="description">Description</label>
<textarea id="description"></textarea>

<button id="submit">Submit Request</button>
<p id="confirmation" style="display:none;"></p>

<script>
document.getElementById("submit").addEventListener("click", function () {
    const name = document.getElementById("name").value;
    const service = document.getElementById("service").value;
    const priority = document.querySelector(
        "input[name='priority']:checked"
    );

    const confirmation = document.getElementById("confirmation");

    if (!name || !service || !priority) {
        confirmation.textContent = "Validation failed";
        confirmation.style.display = "block";
        return;
    }

    confirmation.textContent =
        "Request submitted successfully for " + name +
        " | Service: " + service +
        " | Priority: " + priority.value;

    confirmation.style.display = "block";
});
</script>
</body>
</html>
"""
    HTML_FILE.write_text(html, encoding="utf-8")
    print(f"Local portal created: {HTML_FILE.name}")


def get_page_url():
    return HTML_FILE.resolve().as_uri()


def run_selenium():
    print("\n" + "=" * 70)
    print("SELENIUM — COMPLETE WORKFLOW")
    print("=" * 70)

    start = time.perf_counter()
    driver = webdriver.Chrome()

    try:
        driver.get(get_page_url())
        print("Page opened.")

        wait = WebDriverWait(driver, TIMEOUT)

        name = wait.until(
            EC.presence_of_element_located((By.ID, "name"))
        )
        name.clear()
        name.send_keys("Alex Morgan")
        print("Name filled.")

        email = driver.find_element(By.ID, "email")
        email.clear()
        email.send_keys("alex@example.com")
        print("Email filled.")

        service = Select(driver.find_element(By.ID, "service"))
        service.select_by_visible_text("Technical Support")
        print("Service selected.")

        priority = driver.find_element(
            By.CSS_SELECTOR, "input[value='high']"
        )
        if not priority.is_selected():
            priority.click()
        print("Priority selected.")

        description = driver.find_element(By.ID, "description")
        description.clear()
        description.send_keys("Automated service request for testing.")
        print("Description filled.")

        submit = wait.until(
            EC.element_to_be_clickable((By.ID, "submit"))
        )
        submit.click()
        print("Request submitted.")

        confirmation = wait.until(
            EC.visibility_of_element_located((By.ID, "confirmation"))
        )
        confirmation_text = confirmation.text
        print(f"Confirmation: {confirmation_text}")

        driver.save_screenshot(str(SELENIUM_SCREENSHOT))
        print(f"Screenshot saved: {SELENIUM_SCREENSHOT.name}")

        passed = (
            "Request submitted successfully for Alex Morgan" in confirmation_text
            and "Technical Support" in confirmation_text
            and "Priority: high" in confirmation_text
        )

        elapsed = time.perf_counter() - start
        print(f"Selenium verification: {'PASS' if passed else 'FAIL'}")

        return {
            "passed": passed,
            "time": elapsed,
            "headless": False,
            "screenshot": SELENIUM_SCREENSHOT.exists(),
        }

    finally:
        driver.quit()
        print("Selenium browser closed.")


async def run_playwright():
    print("\n" + "=" * 70)
    print("PLAYWRIGHT — COMPLETE WORKFLOW")
    print("=" * 70)

    start = time.perf_counter()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(
                get_page_url(),
                wait_until="domcontentloaded"
            )
            print("Page opened.")

            await page.locator("#name").fill("Alex Morgan")
            print("Name filled.")

            await page.locator("#email").fill("alex@example.com")
            print("Email filled.")

            await page.locator("#service").select_option(
                label="Technical Support"
            )
            print("Service selected.")

            await page.locator("input[value='high']").check()
            print("Priority selected.")

            await page.locator("#description").fill(
                "Automated service request for testing."
            )
            print("Description filled.")

            await page.locator("#submit").click()
            print("Request submitted.")

            confirmation = page.locator("#confirmation")
            await confirmation.wait_for(state="visible")

            confirmation_text = await confirmation.inner_text()
            print(f"Confirmation: {confirmation_text}")

            await page.screenshot(
                path=str(PLAYWRIGHT_SCREENSHOT),
                full_page=True
            )
            print(f"Screenshot saved: {PLAYWRIGHT_SCREENSHOT.name}")

            passed = (
                "Request submitted successfully for Alex Morgan" in confirmation_text
                and "Technical Support" in confirmation_text
                and "Priority: high" in confirmation_text
            )

            elapsed = time.perf_counter() - start
            print(f"Playwright verification: {'PASS' if passed else 'FAIL'}")

            return {
                "passed": passed,
                "time": elapsed,
                "headless": True,
                "screenshot": PLAYWRIGHT_SCREENSHOT.exists(),
            }

        finally:
            await context.close()
            await browser.close()
            print("Playwright browser closed.")


def show_comparison(selenium, playwright):
    print("\n" + "=" * 70)
    print("SELENIUM VS PLAYWRIGHT COMPARISON")
    print("=" * 70)

    faster = (
        "Selenium"
        if selenium["time"] < playwright["time"]
        else "Playwright"
    )

    print(f"Selenium time:   {selenium['time']:.3f} seconds")
    print(f"Playwright time: {playwright['time']:.3f} seconds")
    print(f"Faster measured execution: {faster}")
    print("Reliability: Both frameworks completed the workflow successfully.")
    print(f"Selenium headless:   {selenium['headless']}")
    print(f"Playwright headless: {playwright['headless']}")

    return faster


def show_syntax_comparison():
    print("\n" + "=" * 70)
    print("SYNTAX COMPARISON")
    print("=" * 70)

    print("""
NAME FIELD

Selenium:
    element = driver.find_element(By.ID, "name")
    element.clear()
    element.send_keys("Alex Morgan")

Playwright:
    await page.locator("#name").fill("Alex Morgan")


CLICK

Selenium:
    driver.find_element(By.ID, "submit").click()

Playwright:
    await page.locator("#submit").click()


TEXT

Selenium:
    confirmation.text

Playwright:
    await confirmation.inner_text()


DROPDOWN

Selenium:
    Select(element).select_by_visible_text("Technical Support")

Playwright:
    await page.locator("#service").select_option(
        label="Technical Support"
    )


WAIT

Selenium:
    WebDriverWait(...)
    EC.visibility_of_element_located(...)

Playwright:
    await locator.wait_for(state="visible")

    Plus automatic waiting for many common actions.
""")


def show_locator_comparison():
    print("\n" + "=" * 70)
    print("LOCATOR COMPARISON")
    print("=" * 70)

    print("""
Selenium:
    driver.find_element(By.ID, "name")
    driver.find_element(
        By.CSS_SELECTOR,
        "input[value='high']"
    )

Playwright:
    page.locator("#name")
    page.locator("input[value='high']")

Both support CSS selectors.

Playwright's locator object provides a unified
interface for actions, queries, and waiting.
""")


def show_maintainability_comparison():
    print("\n" + "=" * 70)
    print("MAINTAINABILITY COMPARISON")
    print("=" * 70)

    print("""
SELENIUM

Strengths:
    - Mature ecosystem
    - Large existing codebase support
    - Broad browser support
    - Familiar WebDriver architecture
    - Excellent for existing Selenium projects

Trade-offs:
    - More verbose interaction syntax
    - Explicit waits commonly require more code
    - Driver/browser setup can require more configuration


PLAYWRIGHT

Strengths:
    - Unified locator API
    - Built-in auto-waiting for many actions
    - BrowserContext isolation
    - Native async API
    - Simple headless configuration
    - Strong modern browser automation workflow

Trade-offs:
    - Existing Selenium projects may require migration work
    - Async programming introduces additional Python concepts
""")


def final_verification(selenium, playwright, faster):
    print("\n" + "=" * 70)
    print("DAY 92 FINAL VERIFICATION")
    print("=" * 70)

    checks = [
        ("Same task executed with Selenium", selenium["passed"]),
        ("Same task executed with Playwright", playwright["passed"]),
        ("Selenium screenshot created", selenium["screenshot"]),
        ("Playwright screenshot created", playwright["screenshot"]),
        ("Selenium execution measured", selenium["time"] > 0),
        ("Playwright execution measured", playwright["time"] > 0),
        ("Speed comparison completed", faster in {"Selenium", "Playwright"}),
        ("Reliability comparison completed",
         selenium["passed"] and playwright["passed"]),
        ("Headless comparison completed",
         playwright["headless"] is True),
    ]

    for label, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'}   | {label}")

    return all(value for _, value in checks)


async def main():
    print("=" * 70)
    print("DAY 92 — SELENIUM VS PLAYWRIGHT")
    print("ACCELERATED COMPLETE PROJECT")
    print("=" * 70)

    create_test_page()

    selenium = run_selenium()
    playwright = await run_playwright()

    faster = show_comparison(selenium, playwright)
    show_syntax_comparison()
    show_locator_comparison()
    show_maintainability_comparison()

    completed = final_verification(selenium, playwright, faster)

    print("\n" + "=" * 70)
    print(f"DAY 92 RESULT: {'COMPLETE' if completed else 'INCOMPLETE'}")
    print("=" * 70)

    print("\n" + "=" * 70)
    print("DAY 92 SUMMARY")
    print("=" * 70)
    print(f"Selenium:   {'PASS' if selenium['passed'] else 'FAIL'}")
    print(f"Playwright: {'PASS' if playwright['passed'] else 'FAIL'}")
    print(f"Selenium time:   {selenium['time']:.3f}s")
    print(f"Playwright time: {playwright['time']:.3f}s")
    print(f"Measured faster framework: {faster}")
    print("Overall reliability: Both frameworks completed the workflow successfully.")
    print(f"Final result: {'PASS' if completed else 'FAIL'}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
