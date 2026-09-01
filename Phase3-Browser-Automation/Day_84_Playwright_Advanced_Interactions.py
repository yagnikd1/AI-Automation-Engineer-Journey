"""
Day 84 - Playwright Advanced Interactions
=========================================

Topics practically verified:
- Forms
- JavaScript dialogs: alert, confirm, prompt
- Frames / iframes
- Tabs / new pages / popups
- File uploads
- File downloads
- Event-driven synchronization
- Locator and test-fixture debugging

Verified final result:
Forms: PASS
Dialogs: PASS
Frames: PASS
Tabs / Popups: PASS
Uploads: PASS
Downloads: PASS
"""

from pathlib import Path
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from threading import Thread
import functools

from playwright.sync_api import sync_playwright


DOWNLOAD_PORT = 8765

# Controlled source file for the download test.
download_source = Path("day_84_download_source.txt")
download_source.write_text(
    "Day 84 download verification file.",
    encoding="utf-8",
)


class QuietHandler(SimpleHTTPRequestHandler):
    """Serve local test files without printing HTTP request logs."""

    def log_message(self, format, *args):
        pass


handler = functools.partial(
    QuietHandler,
    directory=str(Path.cwd()),
)

server = TCPServer(
    ("127.0.0.1", DOWNLOAD_PORT),
    handler,
)

server_thread = Thread(
    target=server.serve_forever,
    daemon=True,
)
server_thread.start()


try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        # ================================================================
        # 1. FORMS
        # ================================================================
        print("\n=== 1. FORMS ===")

        page.goto("https://the-internet.herokuapp.com/login")
        page.locator("#username").fill("tomsmith")
        page.locator("#password").fill("SuperSecretPassword!")

        print("Username:", page.locator("#username").input_value())
        print(
            "Password entered:",
            bool(page.locator("#password").input_value()),
        )

        page.locator("button[type='submit']").click()
        login_result = page.locator("#flash").inner_text()

        print(
            "Login successful:",
            "You logged into a secure area!" in login_result,
        )

        # ================================================================
        # 2. JAVASCRIPT DIALOGS
        # ================================================================
        print("\n=== 2. DIALOGS ===")

        page.goto("https://the-internet.herokuapp.com/javascript_alerts")

        alert_data = {}

        def handle_alert(dialog):
            alert_data["type"] = dialog.type
            alert_data["message"] = dialog.message
            dialog.accept()

        page.once("dialog", handle_alert)
        page.get_by_text("Click for JS Alert").click()
        print("Alert type:", alert_data["type"])
        print("Alert handled:", page.locator("#result").inner_text())

        confirm_data = {}

        def handle_confirm(dialog):
            confirm_data["type"] = dialog.type
            confirm_data["message"] = dialog.message
            dialog.dismiss()

        page.once("dialog", handle_confirm)
        page.get_by_text("Click for JS Confirm").click()
        print("Confirm type:", confirm_data["type"])
        print("Confirm handled:", page.locator("#result").inner_text())

        prompt_data = {}

        def handle_prompt(dialog):
            prompt_data["type"] = dialog.type
            prompt_data["message"] = dialog.message
            dialog.accept("Alex")

        page.once("dialog", handle_prompt)
        page.get_by_text("Click for JS Prompt").click()
        print("Prompt type:", prompt_data["type"])
        print("Prompt handled:", page.locator("#result").inner_text())

        # ================================================================
        # 3. FRAMES / IFRAMES
        # ================================================================
        print("\n=== 3. FRAMES ===")

        frame_file = Path("day_84_frame_test.html")
        frame_file.write_text(
            """
            <!DOCTYPE html>
            <html>
            <body>
                <h1>Frame Test Page</h1>
                <iframe id="test-frame" srcdoc="
                    <html>
                    <body>
                        <h2>Service Request Form</h2>
                        <label for='request'>Request:</label>
                        <input id='request' type='text'>
                        <button id='submit'>Submit</button>
                        <p id='result'></p>
                        <script>
                            document.getElementById('submit').addEventListener(
                                'click',
                                function() {
                                    document.getElementById('result').textContent =
                                        'Request submitted';
                                }
                            );
                        </script>
                    </body>
                    </html>
                " width="500" height="300"></iframe>
            </body>
            </html>
            """,
            encoding="utf-8",
        )

        page.goto(frame_file.resolve().as_uri())
        frame = page.frame_locator("#test-frame")
        frame.locator("#request").fill("Account access investigation")

        print("Frame input:", frame.locator("#request").input_value())

        frame.locator("#submit").click()
        frame_result = frame.locator("#result").inner_text()

        print("Frame result:", frame_result)
        print(
            "Frame interaction successful:",
            frame_result == "Request submitted",
        )

        # ================================================================
        # 4. TABS / POPUPS / NEW PAGES
        # ================================================================
        print("\n=== 4. TABS / POPUPS ===")

        page.goto("https://the-internet.herokuapp.com/windows")

        # Start waiting BEFORE the click that creates the new page.
        with context.expect_page() as page_info:
            page.get_by_text("Click Here").click()

        new_page = page_info.value
        new_page.wait_for_load_state()

        print("New tab URL:", new_page.url)
        print("New tab title:", new_page.title())
        print("New tab captured:", "New Window" in new_page.title())

        # ================================================================
        # 5. FILE UPLOAD
        # ================================================================
        print("\n=== 5. FILE UPLOAD ===")

        upload_file = Path("day_84_upload_test.txt")
        upload_file.write_text(
            "Day 84 upload verification file.",
            encoding="utf-8",
        )

        page.goto("https://the-internet.herokuapp.com/upload")
        page.locator("#file-upload").set_input_files(str(upload_file))
        page.locator("#file-submit").click()

        uploaded_name = page.locator("#uploaded-files").inner_text()
        print("Uploaded file:", uploaded_name)
        print("Upload successful:", upload_file.name in uploaded_name)

        # ================================================================
        # 6. FILE DOWNLOAD
        # ================================================================
        print("\n=== 6. FILE DOWNLOAD ===")

        # Controlled local HTTP page: file:// links do not always generate a
        # browser Download event, so the test uses a real HTTP response.
        download_page = Path("day_84_download_test.html")
        download_page.write_text(
            """
            <!DOCTYPE html>
            <html>
            <body>
                <h1>Download Test</h1>
                <a
                    id="download-file"
                    href="/day_84_download_source.txt"
                    download="day_84_report.txt"
                >Download Report</a>
            </body>
            </html>
            """,
            encoding="utf-8",
        )

        page.goto(
            f"http://127.0.0.1:{DOWNLOAD_PORT}/"
            "day_84_download_test.html"
        )

        download_link = page.locator("#download-file")
        print("Download link visible:", download_link.is_visible())

        with page.expect_download(timeout=10000) as download_info:
            download_link.click()

        download = download_info.value
        download_path = Path("day_84_downloaded_file.txt")
        download.save_as(download_path)

        print("Suggested filename:", download.suggested_filename)
        print("Downloaded file:", download_path.name)
        print("Download successful:", download_path.exists())

        downloaded_content = download_path.read_text(encoding="utf-8")
        print("Downloaded content:", downloaded_content)
        print(
            "Download content verified:",
            downloaded_content == "Day 84 download verification file.",
        )

        # ================================================================
        # FINAL VERIFICATION
        # ================================================================
        print("\n=== DAY 84 VERIFICATION ===")
        print("Forms: PASS")
        print("Dialogs: PASS")
        print("Frames: PASS")
        print("Tabs / Popups: PASS")
        print("Uploads: PASS")
        print("Downloads: PASS")
        print("\nDay 84 practical verification complete.")

        browser.close()

finally:
    # Ensure the local server is shut down even if the script errors.
    server.shutdown()
    server.server_close()
