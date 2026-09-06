"""
DAY 88 — CAPTCHAs & AUTOMATION BOUNDARIES
Phase 3 — Browser Automation
Status: COMPLETED AND PRACTICALLY VERIFIED

ROADMAP
Day 87 — Sessions and Login State
Day 88 — CAPTCHAs and Automation Boundaries
Day 89 — Network Inspection

TOPICS COVERED
1. Why CAPTCHAs exist
2. Recognising CAPTCHA challenges
3. Ethical and Terms-of-Service boundaries
4. Manual handoff
5. Avoiding prohibited CAPTCHA bypasses
6. Legitimate automation in authorised test environments

VERIFIED OUTPUT
Test page created: day_88_captcha_test.html
Test page opened: PASS
CAPTCHA detected: PASS
CAPTCHA visible: True
Automation boundary: PASS
Manual intervention required
CAPTCHA bypass attempted: NO
Report saved: day_88_captcha_report.json
Report verification: PASS
Browser cleanup: PASS

CORE MENTAL MODEL
Navigate -> Locate -> Detect -> Decide -> Continue or Stop

CAPTCHA boundary:
Detect -> Stop automated challenge handling -> Manual handoff
-> Resume only when the authorised workflow permits it.

Do not automate CAPTCHA circumvention or bypass.
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

HTML_FILE = "day_88_captcha_test.html"
REPORT_FILE = "day_88_captcha_report.json"

HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>Authorised CAPTCHA Test</title>
</head>
<body>
    <h1>Automation Security Test</h1>

    <form>
        <label>
            Username:
            <input id="username" type="text">
        </label>

        <br><br>

        <label>
            Password:
            <input id="password" type="password">
        </label>

        <br><br>

        <div data-testid="captcha"
             style="border: 1px solid black; padding: 20px;">
            CAPTCHA CHALLENGE
        </div>

        <br>

        <button id="login">Login</button>
    </form>
</body>
</html>
"""

async def main():

    html_path = Path(HTML_FILE)

    html_path.write_text(
        HTML_CONTENT,
        encoding="utf-8"
    )

    print(f"Test page created: {HTML_FILE}")

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )

        context = await browser.new_context()
        page = await context.new_page()

        try:

            url = html_path.resolve().as_uri()

            await page.goto(url)

            print("Test page opened: PASS")

            captcha = page.locator(
                "[data-testid='captcha']"
            )

            captcha_count = await captcha.count()

            if captcha_count > 0:
                captcha_detected = True
                print("CAPTCHA detected: PASS")
            else:
                captcha_detected = False
                print("CAPTCHA detected: FAIL")

            if captcha_detected:
                captcha_visible = await captcha.is_visible()
                print(f"CAPTCHA visible: {captcha_visible}")
            else:
                captcha_visible = False

            if captcha_visible:

                automation_action = (
                    "STOP_AND_REQUEST_MANUAL_HANDOFF"
                )

                print("Automation boundary: PASS")
                print("Manual intervention required")

            else:

                automation_action = "CONTINUE"
                print("Automation boundary: CONTINUE")

            bypass_attempted = False

            print("CAPTCHA bypass attempted: NO")

            report = {
                "captcha_detected": captcha_detected,
                "captcha_visible": captcha_visible,
                "automation_action": automation_action,
                "bypass_attempted": bypass_attempted
            }

            with open(
                REPORT_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    report,
                    file,
                    indent=4
                )

            print(f"Report saved: {REPORT_FILE}")

            report_path = Path(REPORT_FILE)

            if report_path.exists():
                print("Report verification: PASS")
            else:
                print("Report verification: FAIL")

        finally:

            await context.close()
            await browser.close()

            print("Browser cleanup: PASS")


if __name__ == "__main__":
    asyncio.run(main())
