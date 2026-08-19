"""
DAY 72 — BASIC PAGE INTERACTIONS
================================

Program: Service Request Submission Portal

Roadmap area:
    Selenium — Interacting with Pages

Day 72 learning goals:
    1. Type into input fields with send_keys().
    2. Remove existing input with clear().
    3. Click buttons and links with click().
    4. Submit a form through a submit button.
    5. Verify the page state after each interaction.
    6. Close the browser safely with finally and driver.quit().

The page is embedded in this file as an authorised offline practice portal.
No external website is modified.
"""

# ================================================================
# BLOCK 1 — IMPORTS
# ================================================================

from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By


# ================================================================
# BLOCK 2 — AUTHORISED OFFLINE PRACTICE PAGE
# ================================================================

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Service Request Portal</title>
</head>
<body>
    <main>
        <h1>Submit a Service Request</h1>

        <form id="request-form">
            <label for="customer-name">Customer name</label>
            <input
                id="customer-name"
                name="customer-name"
                type="text"
                value=""
            >

            <label for="request-title">Request title</label>
            <input
                id="request-title"
                name="request-title"
                type="text"
                value=""
            >

            <button id="submit-request" type="submit">
                Submit Request
            </button>
        </form>

        <p id="submission-status">Not submitted</p>

        <a id="confirmation-link" href="#confirmation">
            View Confirmation
        </a>

        <section
            id="confirmation"
            data-state="hidden"
            style="display: none;"
        >
            <h2>Request Confirmation</h2>
            <p>Your service request was recorded.</p>
        </section>
    </main>

    <script>
        const form = document.getElementById("request-form");
        const status = document.getElementById("submission-status");

        form.addEventListener("submit", function(event) {
            // Keep the offline practice page loaded after submission.
            event.preventDefault();

            const customer =
                document.getElementById("customer-name").value;
            const request =
                document.getElementById("request-title").value;

            status.textContent =
                `Submitted: ${customer} — ${request}`;
            status.setAttribute("data-state", "submitted");
        });

        const confirmationLink =
            document.getElementById("confirmation-link");
        const confirmationSection =
            document.getElementById("confirmation");

        confirmationLink.addEventListener("click", function(event) {
            event.preventDefault();
            confirmationSection.style.display = "block";
            confirmationSection.setAttribute("data-state", "visible");
        });
    </script>
</body>
</html>
"""

# quote() percent-encodes the HTML for safe placement inside a data URL.
# Encoding is not encryption.
page_url = "data:text/html;charset=utf-8," + quote(html)


# ================================================================
# BLOCK 3 — START MICROSOFT EDGE
# ================================================================

driver = webdriver.Edge()


try:
    # ============================================================
    # BLOCK 4 — OPEN THE PAGE AND LOCATE THE INPUTS
    # ============================================================

    driver.get(page_url)

    customer_name_input = driver.find_element(By.ID, "customer-name")
    request_title_input = driver.find_element(By.ID, "request-title")

    # ============================================================
    # BLOCK 5 — TYPE WITH send_keys()
    # ============================================================

    # send_keys() simulates keyboard input.
    customer_name_input.send_keys("Morgan Lee")
    request_title_input.send_keys("Reset customer password")

    print(
        "Before clear:",
        request_title_input.get_attribute("value"),
    )

    # ============================================================
    # BLOCK 6 — REMOVE AND REPLACE TEXT WITH clear()
    # ============================================================

    # clear() removes the existing content but does not type new text.
    request_title_input.clear()
    request_title_input.send_keys("Update account permissions")

    print(
        "After replacement:",
        request_title_input.get_attribute("value"),
    )
    print(f"Page: {driver.title}")
    print(
        "Customer:",
        customer_name_input.get_attribute("value"),
    )

    # Why get_attribute("value")?
    # The .text property reads visible text between HTML tags. The current
    # content of an <input> is stored in its value property instead.

    # ============================================================
    # BLOCK 7 — CLICK A SUBMIT BUTTON
    # ============================================================

    submit_button = driver.find_element(By.ID, "submit-request")
    submit_button.click()

    # type="submit" makes the button submit its enclosing form.
    submission_status = driver.find_element(By.ID, "submission-status")

    print(f"Status: {submission_status.text}")
    print(
        "State:",
        submission_status.get_attribute("data-state"),
    )

    # The action is verified in two independent ways:
    #   1. Visible status text changed.
    #   2. data-state changed to "submitted".

    # ============================================================
    # BLOCK 8 — CLICK A LINK AND VERIFY VISIBILITY
    # ============================================================

    confirmation_link = driver.find_element(By.ID, "confirmation-link")
    confirmation_section = driver.find_element(By.ID, "confirmation")

    print(
        "Displayed before click:",
        confirmation_section.is_displayed(),
    )

    confirmation_link.click()

    confirmation_heading = driver.find_element(
        By.CSS_SELECTOR,
        "#confirmation h2",
    )

    print(f"Link text: {confirmation_link.text}")
    print(f"Confirmation: {confirmation_heading.text}")
    print(
        "Displayed after click:",
        confirmation_section.is_displayed(),
    )
    print(
        "Confirmation state:",
        confirmation_section.get_attribute("data-state"),
    )

    # find_element() proves the section exists in the DOM.
    # is_displayed() proves it is currently visible to the user.

finally:
    # ============================================================
    # BLOCK 9 — SAFE CLEANUP
    # ============================================================

    # finally runs whether the interaction succeeds or an error occurs.
    driver.quit()


# ================================================================
# EXPECTED OUTPUT
# ================================================================

# Before clear: Reset customer password
# After replacement: Update account permissions
# Page: Service Request Portal
# Customer: Morgan Lee
# Status: Submitted: Morgan Lee — Update account permissions
# State: submitted
# Displayed before click: False
# Link text: View Confirmation
# Confirmation: Request Confirmation
# Displayed after click: True
# Confirmation state: visible


# ================================================================
# DAY 72 QUICK REFERENCE
# ================================================================

# element.send_keys("text")
#     Types text or key input into an interactive element.

# element.clear()
#     Removes the current content of a text-capable field.

# element.click()
#     Activates a clickable element such as a button or link.

# element.get_attribute("value")
#     Reads the current value of an input field.

# element.text
#     Reads visible text contained by an element.

# element.is_displayed()
#     Returns True when the element is visible and False when hidden.

# driver.title
#     Reads the current page title.

# driver.quit()
#     Closes every window in the controlled browser session and ends the
#     WebDriver process.


# ================================================================
# IMPORTANT DISTINCTIONS AND TROUBLESHOOTING
# ================================================================

# 1. clear() versus send_keys()
#    clear() removes content; send_keys() enters content.

# 2. Existing in the DOM versus visible
#    find_element() may locate a hidden element. is_displayed() checks
#    whether the user can currently see it.

# 3. Button click versus form submission
#    click() activates the button. type="submit" gives that button the
#    browser behaviour of submitting its form.

# 4. NameError encountered during practice
#    confirmation_link was printed before the Python variable had been
#    assigned. The correction was to locate and assign the link before using
#    confirmation_link.text or confirmation_link.click().

# 5. Fragment verification on encoded data pages
#    Edge did not update the URL fragment for the encoded data page. The
#    reliable offline verification was changed to a direct observable state
#    change: the hidden section became visible and data-state became visible.

# 6. Day 73 boundary
#    Text areas, checkboxes, radio buttons, native dropdowns, Selenium Select,
#    keyboard keys, and validation messages belong to Day 73 — Forms and
#    Controls. They are not unfinished Day 72 topics.

