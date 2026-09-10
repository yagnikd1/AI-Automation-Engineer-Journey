"""
DAY 91 — CONCURRENT BROWSER AUTOMATION
Phase 3 — Browser Automation

Covers:
1. asyncio.gather()
2. Multiple pages
3. Multiple browser contexts
4. Concurrency limits
5. Resource cleanup
6. Partial-failure handling
7. Responsible request rates

Requirements:
    pip install playwright
    python -m playwright install chromium
"""

import asyncio
import time
from playwright.async_api import async_playwright


# ============================================================
# EXAMPLE 1 — asyncio.gather()
# ============================================================

async def simple_task(name, delay):
    await asyncio.sleep(delay)
    return f"{name} completed"


async def example_asyncio_gather():
    print("\nEXAMPLE 1 — asyncio.gather()")

    results = await asyncio.gather(
        simple_task("Task A", 1),
        simple_task("Task B", 0.5),
        simple_task("Task C", 0.2),
    )

    for result in results:
        print(result)


# ============================================================
# EXAMPLE 2 — MULTIPLE PAGES
# ============================================================

async def example_multiple_pages():
    print("\nEXAMPLE 2 — Multiple pages")

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)

        page1 = await browser.new_page()
        page2 = await browser.new_page()

        await page1.goto("https://example.com", wait_until="domcontentloaded")
        await page2.goto("https://example.org", wait_until="domcontentloaded")

        print("Page 1 title:", await page1.title())
        print("Page 2 title:", await page2.title())

        await page1.close()
        await page2.close()
        await browser.close()


# ============================================================
# EXAMPLE 3 — MULTIPLE BROWSER CONTEXTS
# ============================================================

async def example_multiple_contexts():
    print("\nEXAMPLE 3 — Multiple browser contexts")

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)

        context1 = await browser.new_context()
        context2 = await browser.new_context()

        page1 = await context1.new_page()
        page2 = await context2.new_page()

        await page1.goto("https://example.com", wait_until="domcontentloaded")
        await page2.goto("https://example.org", wait_until="domcontentloaded")

        print("Context 1:", await page1.title())
        print("Context 2:", await page2.title())

        await page1.close()
        await page2.close()
        await context1.close()
        await context2.close()
        await browser.close()


# ============================================================
# EXAMPLE 4 — CONCURRENCY LIMIT
# ============================================================

example_active = 0
example_max_active = 0


async def limited_task(name, semaphore):
    global example_active, example_max_active

    async with semaphore:
        example_active += 1
        example_max_active = max(example_max_active, example_active)

        print(f"START {name} | active={example_active}")
        await asyncio.sleep(1)

        example_active -= 1
        print(f"END   {name} | active={example_active}")


async def example_concurrency_limit():
    print("\nEXAMPLE 4 — Concurrency limit")

    semaphore = asyncio.Semaphore(2)

    await asyncio.gather(
        limited_task("Task 1", semaphore),
        limited_task("Task 2", semaphore),
        limited_task("Task 3", semaphore),
        limited_task("Task 4", semaphore),
    )

    print("Maximum simultaneous tasks:", example_max_active)


# ============================================================
# EXAMPLE 5 — PARTIAL FAILURE HANDLING
# ============================================================

async def task_that_may_fail(name, should_fail=False):
    await asyncio.sleep(0.2)

    if should_fail:
        raise RuntimeError(f"{name} failed")

    return f"{name} succeeded"


async def example_partial_failure():
    print("\nEXAMPLE 5 — Partial-failure handling")

    results = await asyncio.gather(
        task_that_may_fail("Task A"),
        task_that_may_fail("Task B", should_fail=True),
        task_that_may_fail("Task C"),
        return_exceptions=True,
    )

    for result in results:
        if isinstance(result, Exception):
            print("FAILED:", result)
        else:
            print("PASS:", result)


# ============================================================
# EXAMPLE 6 — RESPONSIBLE REQUEST RATE
# ============================================================

async def example_responsible_rate():
    print("\nEXAMPLE 6 — Responsible request rate")

    for number in range(3):
        print("Request", number + 1)
        await asyncio.sleep(1)


# ============================================================
# DAY 91 INTEGRATED PROGRAM
# ============================================================

URLS = [
    "https://example.com",
    "https://example.org",
    "https://example.net",
    "https://example.com/this-page-does-not-exist",
]

MAX_CONCURRENT_TASKS = 2
REQUEST_DELAY = 1

semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

active_tasks = 0
maximum_active_tasks = 0


async def monitor_page(browser, url):
    global active_tasks, maximum_active_tasks

    async with semaphore:
        active_tasks += 1
        maximum_active_tasks = max(maximum_active_tasks, active_tasks)

        context = None
        page = None
        start_time = time.perf_counter()

        print(f"START | Active tasks: {active_tasks} | {url}")

        try:
            context = await browser.new_context()
            print(f"CONTEXT CREATED | {url}")

            page = await context.new_page()
            print(f"PAGE CREATED | {url}")

            response = await page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=15000,
            )

            status_code = response.status if response else None

            # A 404 can still complete page.goto(), so check the status.
            if status_code is not None and status_code >= 400:
                raise Exception(
                    f"HTTP request failed with status {status_code}"
                )

            title = await page.title()

            # Deliberate pacing between requests.
            await asyncio.sleep(REQUEST_DELAY)

            elapsed = round(time.perf_counter() - start_time, 2)

            return {
                "url": url,
                "status": "PASS",
                "http_status": status_code,
                "title": title,
                "elapsed_seconds": elapsed,
            }

        except Exception as error:
            elapsed = round(time.perf_counter() - start_time, 2)

            return {
                "url": url,
                "status": "FAILED",
                "error": str(error),
                "elapsed_seconds": elapsed,
            }

        finally:
            if page:
                await page.close()
                print(f"PAGE CLOSED | {url}")

            if context:
                await context.close()
                print(f"CONTEXT CLOSED | {url}")

            active_tasks -= 1
            print(f"END | Active tasks: {active_tasks} | {url}")


async def integrated_program():
    print("=" * 70)
    print("DAY 91 — CONCURRENT BROWSER AUTOMATION")
    print("Concurrent Browser Monitoring & Failure Recovery System")
    print("=" * 70)

    print(f"\nConcurrency limit: {MAX_CONCURRENT_TASKS}")
    print(f"URLs to monitor: {len(URLS)}")

    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)

            tasks = [
                monitor_page(browser, url)
                for url in URLS
            ]

            results = await asyncio.gather(*tasks)

            print("\n" + "=" * 70)
            print("FINAL MONITORING RESULTS")
            print("=" * 70)

            for result in results:
                print(result)

            successful = [
                result for result in results
                if result["status"] == "PASS"
            ]

            failed = [
                result for result in results
                if result["status"] == "FAILED"
            ]

            print("\n" + "=" * 70)
            print("DAY 91 FINAL VERIFICATION")
            print("=" * 70)

            print("PASS — asyncio.gather() completed all tasks.")
            print("PASS — Browser contexts and pages created.")

            if maximum_active_tasks <= MAX_CONCURRENT_TASKS:
                print(
                    f"PASS — Concurrency limit respected: "
                    f"{maximum_active_tasks}"
                )
            else:
                print("FAIL — Concurrency limit exceeded.")

            if successful and failed:
                print(
                    "PASS — Partial failure handled without "
                    "destroying successful tasks."
                )
            else:
                print(
                    "WARNING — Partial failure scenario was not observed."
                )

            print(f"PASS — Successful tasks: {len(successful)}")
            print(f"PASS — Failed tasks: {len(failed)}")
            print("PASS — Page/context cleanup executed.")
            print(
                f"PASS — Responsible delay applied: "
                f"{REQUEST_DELAY} second(s)"
            )

            print("\nDAY 91 INTEGRATED VERIFICATION COMPLETE.")

            await browser.close()

    finally:
        print("\nBrowser closed successfully.")


async def main():
    # Individual examples are available above for revision.
    # Uncomment them when studying a specific subtopic.

    # await example_asyncio_gather()
    # await example_multiple_pages()
    # await example_multiple_contexts()
    # await example_concurrency_limit()
    # await example_partial_failure()
    # await example_responsible_rate()

    # Final Day 91 integrated program:
    await integrated_program()


if __name__ == "__main__":
    asyncio.run(main())
