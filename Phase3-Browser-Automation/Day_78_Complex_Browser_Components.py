"""
Day 78 - Complex Browser Components
Phase 3: Browser Automation

Canonical coverage:
1. Native dropdowns compared with custom dropdowns
2. Pop-ups and overlays
3. JavaScript alerts
4. Confirm dialogs
5. Prompt dialogs
6. Iframes
7. Switching into an iframe
8. Returning to the main document

This self-contained Selenium practice uses a data URL, so no external website
or network connection is required.
"""

from urllib.parse import quote

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Automation Support Portal</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; }
        section { border: 1px solid #999; margin-bottom: 20px; padding: 15px; }
        #custom-options { display: none; border: 1px solid #555; width: 180px; padding: 0; }
        #custom-options li { cursor: pointer; list-style: none; padding: 8px; }
        #custom-options li:hover { background: #ddd; }
        #overlay {
            position: fixed; inset: 0; display: flex; align-items: center;
            justify-content: center; background: rgba(0, 0, 0, 0.65);
        }
        #popup { background: white; padding: 25px; width: 300px; }
        iframe { width: 100%; height: 140px; }
    </style>
</head>
<body>
    <h1>Automation Support Portal</h1>

    <div id="overlay">
        <div id="popup">
            <h2>Maintenance Notice</h2>
            <p>The support portal is operating normally.</p>
            <button id="close-overlay"
                    onclick="document.getElementById('overlay').style.display='none'">
                Continue
            </button>
        </div>
    </div>

    <section>
        <h2>Native Dropdown</h2>
        <select id="priority">
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
        </select>
    </section>

    <section>
        <h2>Custom Dropdown</h2>
        <button id="department-button" onclick="toggleDepartments()">
            Choose department
        </button>
        <ul id="custom-options">
            <li data-value="billing" onclick="chooseDepartment(this)">Billing</li>
            <li data-value="technical" onclick="chooseDepartment(this)">Technical Support</li>
            <li data-value="accounts" onclick="chooseDepartment(this)">Accounts</li>
        </ul>
        <p id="department-result">No department selected</p>
    </section>

    <section>
        <h2>JavaScript Dialogs</h2>
        <button id="alert-button" onclick="alert('Ticket information saved')">Show Alert</button>
        <button id="confirm-button" onclick="handleConfirmation()">Show Confirm</button>
        <button id="prompt-button" onclick="handlePrompt()">Show Prompt</button>
        <p id="confirm-result">No confirmation response</p>
        <p id="prompt-result">No agent entered</p>
    </section>

    <section>
        <h2>Embedded Knowledge Base</h2>
        <iframe id="knowledge-frame" srcdoc="
            <html><body>
                <h3 id='article-title'>Password Reset Guide</h3>
                <button id='open-article'
                        onclick=&quot;document.getElementById('frame-result').textContent='Article opened';&quot;>
                    Open Article
                </button>
                <p id='frame-result'>Article not opened</p>
            </body></html>
        "></iframe>
    </section>

    <p id="main-document-status">Main document available</p>

    <script>
        function toggleDepartments() {
            const options = document.getElementById("custom-options");
            options.style.display = options.style.display === "block" ? "none" : "block";
        }
        function chooseDepartment(element) {
            document.getElementById("department-result").textContent = element.textContent.trim();
            document.getElementById("custom-options").style.display = "none";
        }
        function handleConfirmation() {
            const accepted = confirm("Submit the support ticket?");
            document.getElementById("confirm-result").textContent =
                accepted ? "Ticket submitted" : "Submission cancelled";
        }
        function handlePrompt() {
            const agent = prompt("Enter the assigned agent:");
            document.getElementById("prompt-result").textContent =
                agent === null ? "Prompt cancelled" : "Assigned agent: " + agent;
        }
    </script>
</body>
</html>
"""


def main():
    """Run the complete Day 78 browser-component demonstration."""
    driver = webdriver.Edge()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("data:text/html;charset=utf-8," + quote(HTML))
        print(f"Title: {driver.title}")

        # A DOM overlay is an HTML element, not a JavaScript alert.
        overlay = wait.until(EC.visibility_of_element_located((By.ID, "overlay")))
        print(f"Overlay initially visible: {overlay.is_displayed()}")
        wait.until(EC.element_to_be_clickable((By.ID, "close-overlay"))).click()
        wait.until(EC.invisibility_of_element_located((By.ID, "overlay")))
        print("Overlay closed: True")

        # Select works only with a real HTML <select> element.
        native_dropdown = Select(driver.find_element(By.ID, "priority"))
        native_dropdown.select_by_visible_text("High")
        print(f"Native priority: {native_dropdown.first_selected_option.text}")

        # A custom dropdown is handled with ordinary locators and clicks.
        driver.find_element(By.ID, "department-button").click()
        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#custom-options [data-value='technical']")
            )
        ).click()
        department = driver.find_element(By.ID, "department-result").text
        print(f"Custom department: {department}")

        # alert(): read its text and choose OK with accept().
        driver.find_element(By.ID, "alert-button").click()
        alert_dialog = wait.until(EC.alert_is_present())
        print(f"Alert message: {alert_dialog.text}")
        alert_dialog.accept()

        # confirm(): choose Cancel with dismiss().
        driver.find_element(By.ID, "confirm-button").click()
        confirm_dialog = wait.until(EC.alert_is_present())
        print(f"Confirm message: {confirm_dialog.text}")
        confirm_dialog.dismiss()
        confirm_updated = wait.until(
            EC.text_to_be_present_in_element(
                (By.ID, "confirm-result"), "Submission cancelled"
            )
        )
        print(f"Confirm dismissed: {confirm_updated}")
        print(f"Confirm result: {driver.find_element(By.ID, 'confirm-result').text}")

        # prompt(): enter text, then choose OK.
        driver.find_element(By.ID, "prompt-button").click()
        prompt_dialog = wait.until(EC.alert_is_present())
        print(f"Prompt message: {prompt_dialog.text}")
        prompt_dialog.send_keys("Morgan Lee")
        prompt_dialog.accept()
        prompt_updated = wait.until(
            EC.text_to_be_present_in_element((By.ID, "prompt-result"), "Morgan Lee")
        )
        print(f"Prompt updated: {prompt_updated}")
        print(f"Prompt result: {driver.find_element(By.ID, 'prompt-result').text}")

        # The iframe contains a separate document and therefore a separate context.
        wait.until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "knowledge-frame"))
        )
        frame_title = wait.until(
            EC.visibility_of_element_located((By.ID, "article-title"))
        ).text
        print(f"Iframe article: {frame_title}")
        driver.find_element(By.ID, "open-article").click()
        print(f"Iframe result: {driver.find_element(By.ID, 'frame-result').text}")

        # default_content() returns directly to the top-level document.
        driver.switch_to.default_content()
        main_status = driver.find_element(By.ID, "main-document-status").text
        print(f"Main document result: {main_status}")

    except TimeoutException as error:
        print(f"Timed out while handling a component: {error}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()


# QUICK REVISION NOTES
#
# Native dropdown:
#   Select(element).select_by_visible_text("High")
#   Select works only when element.tag_name == "select".
#
# Custom dropdown:
#   Click the control, wait for the desired option, then click the option.
#
# DOM modal/overlay:
#   Locate it with By, wait for visibility/clickability, close it normally,
#   then wait for invisibility if it was blocking other controls.
#
# JavaScript dialog:
#   dialog = wait.until(EC.alert_is_present())
#   dialog.text          -> reads the message
#   dialog.accept()      -> OK
#   dialog.dismiss()     -> Cancel
#   dialog.send_keys()   -> enters prompt text
#
# Iframe:
#   driver.switch_to.frame(frame)            -> enter a frame
#   driver.switch_to.parent_frame()           -> move upward one frame level
#   driver.switch_to.default_content()        -> return to the top document
#
# Common failures:
#   UnexpectedTagNameException -> Select received a non-<select> element.
#   NoAlertPresentException    -> code switched before the dialog appeared.
#   NoSuchElementException     -> often wrong document/frame context.
#   TimeoutException           -> expected state did not arrive in time.
#   ElementClickInterceptedException -> overlay or another element blocked click.
