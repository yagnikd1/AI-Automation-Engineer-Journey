"""
DAY 85 - PLAYWRIGHT BROWSER CONTEXTS, COOKIES, SESSIONS & AUTHENTICATION STATE

Status: COMPLETED AND PRACTICALLY VERIFIED

ROADMAP TOPICS COVERED
1. Browser contexts
2. Context isolation and lifecycle
3. Cookies: read, add, clear
4. Session state
5. Save and reuse authentication state
6. Real authorized login integration

KEY SYNTAX
browser = playwright.chromium.launch()
context = browser.new_context()
page = context.new_page()
context.add_cookies([...])
cookies = context.cookies()
context.clear_cookies()
context.storage_state(path="auth_state.json")
new_context = browser.new_context(storage_state="auth_state.json")
context.close()
browser.close()

IMPORTANT
A BrowserContext is an isolated browser environment. Different contexts can
have independent cookies, storage, and authentication state.

DAY 85 PRACTICAL VERIFICATION
- Context A used customer cookie state.
- Context B used administrator cookie state.
- Clearing Context A did not affect Context B.
- Authentication-like state was saved with storage_state().
- A new context loaded the saved state.
- A real authorized login was performed against Sauce Demo.
- Saved authentication state allowed a new context to reach Products without
  performing login again.
- A fresh context had no session-username cookie, proving auth state isolation.

REAL LOGIN REFERENCE WORKFLOW

from playwright.sync_api import sync_playwright
from pathlib import Path

BASE_URL = "https://www.saucedemo.com/"
AUTH_FILE = Path("day_85_real_auth_state.json")
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)

    # Fresh context for the authorized login.
    login_context = browser.new_context()
    login_page = login_context.new_page()
    login_page.goto(BASE_URL)

    login_page.locator("#user-name").fill(USERNAME)
    login_page.locator("#password").fill(PASSWORD)
    login_page.locator("#login-button").click()

    inventory_title = login_page.locator(".title").inner_text()
    print("Authenticated page:", inventory_title)
    print("Real login:", "PASS" if inventory_title == "Products" else "FAIL")

    # Inspect authenticated cookies.
    authenticated_cookies = login_context.cookies()
    print("Authenticated cookies:", len(authenticated_cookies))
    for cookie in authenticated_cookies:
        print(cookie["name"], "=", cookie["value"])

    # Save auth state and close the original authenticated context.
    login_context.storage_state(path=str(AUTH_FILE))
    print("Auth state saved:", AUTH_FILE)
    login_context.close()

    # Reuse the saved auth state in a brand-new context.
    reused_context = browser.new_context(storage_state=str(AUTH_FILE))
    reused_page = reused_context.new_page()
    reused_page.goto(BASE_URL + "inventory.html")

    reused_title = reused_page.locator(".title").inner_text()
    print("Reused authenticated page:", reused_title)
    print(
        "Authentication state reuse:",
        "PASS" if reused_title == "Products" else "FAIL"
    )

    # Create a completely fresh context and prove auth state was not shared.
    isolated_context = browser.new_context()
    isolated_page = isolated_context.new_page()
    isolated_page.goto(BASE_URL + "inventory.html")

    fresh_cookies = isolated_context.cookies()
    session_cookie_found = False

    for cookie in fresh_cookies:
        if cookie["name"] == "session-username":
            session_cookie_found = True
            break

    print("Fresh context session cookie found:", session_cookie_found)
    print(
        "Context authentication isolation:",
        "PASS" if not session_cookie_found else "FAIL"
    )

    print("Reused context cookies:", len(reused_context.cookies()))
    print("Fresh context cookies:", len(fresh_cookies))

    isolated_context.close()
    reused_context.close()
    browser.close()

    print("All contexts and browser closed")

# SECURITY NOTES
# - Only automate accounts/systems you are authorized to use.
# - Authentication-state files can contain sensitive session information.
# - Do not commit real credentials or private auth-state files to public repos.
# - Prefer dedicated test accounts and add auth-state JSON files to .gitignore.
