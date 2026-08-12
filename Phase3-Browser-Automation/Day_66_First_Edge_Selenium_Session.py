"""
Day 66 — First Microsoft Edge Selenium Session

Learning goals:
1. Configure Microsoft Edge and EdgeDriver.
2. Create a WebDriver-controlled browser session.
3. Navigate to a webpage with browser.get().
4. Read the page title, current URL, and page-source length.
5. Always terminate the complete session with browser.quit().
"""

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.remote.webdriver import WebDriver


# ============================================================================
# SECTION 1: PROGRAM CONFIGURATION
# ============================================================================

TARGET_URL = "https://example.com"
DRIVER_PATH = Path("drivers") / "msedgedriver.exe"
DRIVER_LOG_PATH = "day66_edgedriver.log"


def print_indicator(step: int, message: str) -> None:
    """Print a clear numbered progress indicator in the terminal."""
    print(f"[{step}/5] {message}")


# ============================================================================
# SECTION 2: EDGE OPTIONS AND WEBDRIVER CREATION
# ============================================================================

def create_browser() -> WebDriver:
    """Configure EdgeDriver and return a Selenium-controlled Edge browser."""
    if not DRIVER_PATH.is_file():
        raise FileNotFoundError(
            f"EdgeDriver was not found at: {DRIVER_PATH.resolve()}"
        )

    options = Options()

    # Skip Edge's first-run screen so automation can start immediately.
    options.add_argument("--no-first-run")

    # Use operating-system pipes instead of a temporary localhost DevTools
    # port. This solved the Day 66 connection-reset problem on this computer.
    options.add_argument("--remote-debugging-pipe")

    service = Service(
        executable_path=str(DRIVER_PATH),
        log_output=DRIVER_LOG_PATH,
        service_args=["--verbose"],
    )

    return webdriver.Edge(service=service, options=options)


# ============================================================================
# SECTION 3: PAGE INFORMATION
# ============================================================================

def display_page_information(browser: WebDriver) -> None:
    """Read and print useful information from the current webpage."""
    print("\n--- PAGE INFORMATION ---")
    print(f"Title                 : {browser.title}")
    print(f"Current URL           : {browser.current_url}")
    print(f"Page-source characters: {len(browser.page_source)}")


# ============================================================================
# SECTION 4: MAIN AUTOMATION WORKFLOW
# ============================================================================

def main() -> None:
    """Run the complete Day 66 Edge automation workflow."""
    browser: WebDriver | None = None

    print("=" * 60)
    print("DAY 66 — FIRST EDGE SELENIUM SESSION")
    print("=" * 60)

    try:
        print_indicator(1, "Checking the local EdgeDriver path...")
        print(f"      Driver: {DRIVER_PATH.resolve()}")

        print_indicator(2, "Starting a Selenium-controlled Edge session...")
        browser = create_browser()
        print("      Edge session created successfully.")

        print_indicator(3, f"Navigating to {TARGET_URL}...")
        browser.get(TARGET_URL)
        print("      Navigation completed.")

        print_indicator(4, "Reading browser and webpage information...")
        display_page_information(browser)

        print("\nRESULT: Day 66 browser automation completed successfully.")

    except FileNotFoundError as error:
        print(f"\nCONFIGURATION ERROR: {error}")
        print("Place the compatible msedgedriver.exe inside the drivers folder.")
        raise

    except Exception as error:
        print(f"\nAUTOMATION ERROR: {type(error).__name__}: {error}")
        raise

    finally:
        print_indicator(5, "Cleaning up the browser session...")

        if browser is not None:
            browser.quit()
            print("      Edge windows closed.")
            print("      WebDriver session ended.")
        else:
            print("      No completed WebDriver session was available to quit.")

        print("=" * 60)


# ============================================================================
# SECTION 5: PROGRAM ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
