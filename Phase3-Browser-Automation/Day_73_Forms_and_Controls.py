"""
DAY 73 - FORMS AND CONTROLS
Phase 3: Browser Automation with Selenium

Program name: Event Registration Portal

PURPOSE
-------
This learning file demonstrates how Selenium works with common native HTML
form controls on an authorised offline practice page. The page is embedded in
this file and opened as a data URL, so no external website is contacted.

TOPICS COVERED
--------------
1. Text inputs
2. Text areas
3. Checkboxes
4. Radio buttons and radio-group exclusivity
5. Native HTML dropdowns
6. Selenium Select
7. Selecting dropdown options by visible text, value, and index
8. Submit buttons
9. Keyboard keys
10. Native HTML validation messages
11. Invalid versus valid form submission
12. Verifying the resulting page state

ENVIRONMENT
-----------
- Python 3
- selenium
- Microsoft Edge
- Phase 3 virtual environment: myenv
"""


# ================================================================
# SECTION 1 - IMPORTS
# ================================================================

# quote() percent-encodes the HTML so it can be safely placed in a data URL.
from urllib.parse import quote

# webdriver controls the browser.
from selenium import webdriver

# By supplies locator strategies such as By.ID.
from selenium.webdriver.common.by import By

# Keys supplies special keyboard keys and keyboard shortcuts.
from selenium.webdriver.common.keys import Keys

# Select is Selenium's helper class for native HTML <select> elements.
from selenium.webdriver.support.ui import Select


# ================================================================
# SECTION 2 - AUTHORISED OFFLINE PRACTICE PAGE
# ================================================================

# The HTML contains every native form control required by Day 73.
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Event Registration Portal</title>
</head>
<body>
    <h1>Community Event Registration</h1>

    <form id="registration-form">
        <label for="participant-name">Participant name</label>
        <input
            id="participant-name"
            name="participant_name"
            type="text"
            required
        >

        <br><br>

        <label for="accessibility-notes">Accessibility notes</label>
        <textarea
            id="accessibility-notes"
            name="accessibility_notes"
            rows="4"
        ></textarea>

        <br><br>

        <input
            id="email-updates"
            name="email_updates"
            type="checkbox"
        >
        <label for="email-updates">Receive email updates</label>

        <br><br>

        <p>Experience level</p>

        <!-- Radio buttons with the same name belong to one group. -->
        <input
            id="beginner"
            name="experience"
            type="radio"
            value="beginner"
        >
        <label for="beginner">Beginner</label>

        <input
            id="intermediate"
            name="experience"
            type="radio"
            value="intermediate"
        >
        <label for="intermediate">Intermediate</label>

        <br><br>

        <!-- Select works with this native <select> element. -->
        <label for="event-session">Event session</label>
        <select id="event-session" name="event_session">
            <option value="">Choose a session</option>
            <option value="morning">Morning Session</option>
            <option value="afternoon">Afternoon Session</option>
            <option value="evening">Evening Session</option>
        </select>

        <br><br>

        <!-- type="submit" gives this button form-submission behaviour. -->
        <button id="submit-registration" type="submit">
            Submit Registration
        </button>
    </form>

    <!-- hidden keeps the confirmation invisible until submission succeeds. -->
    <section id="confirmation" data-state="pending" hidden>
        Registration completed successfully.
    </section>

    <script>
        const form = document.getElementById("registration-form");
        const confirmation = document.getElementById("confirmation");

        form.addEventListener("submit", function(event) {
            // Keep this offline practice page from navigating away.
            event.preventDefault();

            confirmation.hidden = false;
            confirmation.dataset.state = "submitted";
        });
    </script>
</body>
</html>
"""


# ================================================================
# SECTION 3 - BUILD THE DATA URL AND START EDGE
# ================================================================

# Encoding is not encryption. quote() only makes unsafe URL characters safe.
page_url = "data:text/html;charset=utf-8," + quote(html)

# Selenium Manager normally locates or manages the matching Edge driver.
driver = webdriver.Edge()


# ================================================================
# SECTION 4 - INTERACT WITH THE FORM
# ================================================================

try:
    # Open the authorised offline page.
    driver.get(page_url)

    # ------------------------------------------------------------
    # 4A. TEXT INPUT AND TEXT AREA
    # ------------------------------------------------------------

    name_input = driver.find_element(By.ID, "participant-name")
    notes_area = driver.find_element(By.ID, "accessibility-notes")

    # send_keys() simulates typing.
    name_input.send_keys("Morgan Reed")
    notes_area.send_keys("Please reserve a seat near the entrance.")

    print("Title:", driver.title)

    # Input and textarea values are stored in the value property/attribute.
    # .text is not the correct way to read the current typed value.
    print("Participant:", name_input.get_attribute("value"))
    print("Accessibility notes:", notes_area.get_attribute("value"))

    # ------------------------------------------------------------
    # 4B. CHECKBOX
    # ------------------------------------------------------------

    email_checkbox = driver.find_element(By.ID, "email-updates")

    # A defensive condition avoids accidentally turning an already-selected
    # checkbox off. Clicking a checkbox toggles its state.
    if not email_checkbox.is_selected():
        email_checkbox.click()

    print("Email updates selected:", email_checkbox.is_selected())

    # ------------------------------------------------------------
    # 4C. RADIO BUTTONS AND GROUP EXCLUSIVITY
    # ------------------------------------------------------------

    beginner_radio = driver.find_element(By.ID, "beginner")
    intermediate_radio = driver.find_element(By.ID, "intermediate")

    beginner_radio.click()
    print("Beginner selected:", beginner_radio.is_selected())

    # Because both radio buttons use name="experience", selecting one
    # automatically deselects the other.
    intermediate_radio.click()

    print(
        "Beginner after selecting Intermediate:",
        beginner_radio.is_selected(),
    )
    print("Intermediate selected:", intermediate_radio.is_selected())

    # ------------------------------------------------------------
    # 4D. NATIVE DROPDOWN AND SELENIUM SELECT
    # ------------------------------------------------------------

    session_element = driver.find_element(By.ID, "event-session")
    session_select = Select(session_element)

    # Method 1: choose using the text visible to the user.
    session_select.select_by_visible_text("Morning Session")
    selected_by_text = session_select.first_selected_option.text

    # Method 2: choose using the option's value attribute.
    session_select.select_by_value("afternoon")
    selected_by_value = session_select.first_selected_option.text

    # Method 3: choose using a zero-based index.
    # 0 = placeholder, 1 = morning, 2 = afternoon, 3 = evening.
    session_select.select_by_index(3)
    selected_by_index = session_select.first_selected_option.text

    print("Selected by text:", selected_by_text)
    print("Selected by value:", selected_by_value)
    print("Selected by index:", selected_by_index)

    # ------------------------------------------------------------
    # 4E. INVALID SUBMISSION AND VALIDATION MESSAGE
    # ------------------------------------------------------------

    submit_button = driver.find_element(By.ID, "submit-registration")
    confirmation = driver.find_element(By.ID, "confirmation")

    # clear() removes the name and creates an invalid required field.
    name_input.clear()
    submit_button.click()

    # validationMessage is a live DOM property created by the browser.
    # The exact wording can depend on the browser's language.
    validation_message = name_input.get_property("validationMessage")

    print("Validation message:", validation_message)
    print(
        "Confirmation after invalid submission:",
        confirmation.is_displayed(),
    )

    # The confirmation stays hidden because native HTML validation stops the
    # submit event before the JavaScript form listener can run.

    # ------------------------------------------------------------
    # 4F. KEYBOARD KEYS AND VALID SUBMISSION
    # ------------------------------------------------------------

    # Restore the required name.
    name_input.send_keys("Morgan Reed")

    # Ctrl+A selects all existing textarea content on Windows.
    notes_area.send_keys(Keys.CONTROL, "a")

    # Typing now replaces the selected content.
    notes_area.send_keys("Wheelchair-accessible seating requested.")

    # Tab moves keyboard focus to the next interactive control.
    notes_area.send_keys(Keys.TAB)

    # All required data is valid, so the submit event can run.
    submit_button.click()

    print("Updated notes:", notes_area.get_attribute("value"))
    print(
        "Confirmation after valid submission:",
        confirmation.is_displayed(),
    )
    print(
        "Submission state:",
        confirmation.get_attribute("data-state"),
    )


# ================================================================
# SECTION 5 - RELIABLE CLEANUP
# ================================================================

finally:
    # quit() closes every browser window created by this WebDriver session and
    # releases its resources even if an exception occurs above.
    driver.quit()


# ================================================================
# VERIFIED OUTPUT
# ================================================================

# Title: Event Registration Portal
# Participant: Morgan Reed
# Accessibility notes: Please reserve a seat near the entrance.
# Email updates selected: True
# Beginner selected: True
# Beginner after selecting Intermediate: False
# Intermediate selected: True
# Selected by text: Morning Session
# Selected by value: Afternoon Session
# Selected by index: Evening Session
# Validation message: Please fill out this field.
# Confirmation after invalid submission: False
# Updated notes: Wheelchair-accessible seating requested.
# Confirmation after valid submission: True
# Submission state: submitted


# ================================================================
# QUICK REFERENCE
# ================================================================

# Type in a control:
#     element.send_keys("text")

# Clear an input:
#     element.clear()

# Click a control:
#     element.click()

# Read the current input/textarea value:
#     element.get_attribute("value")

# Check checkbox/radio/option state:
#     element.is_selected()

# Use a native dropdown:
#     dropdown = Select(select_element)
#     dropdown.select_by_visible_text("Morning Session")
#     dropdown.select_by_value("afternoon")
#     dropdown.select_by_index(2)

# Read the current option:
#     dropdown.first_selected_option.text

# Press special keys:
#     element.send_keys(Keys.TAB)
#     element.send_keys(Keys.CONTROL, "a")

# Read the browser's validation message:
#     element.get_property("validationMessage")

# IMPORTANT LIMITATION:
# Select works only with a native HTML <select>. A custom dropdown built from
# div, button, ul, or li elements requires ordinary locators and clicks. Custom
# dropdowns are scheduled for Day 78 and are not a Day 73 gap.

