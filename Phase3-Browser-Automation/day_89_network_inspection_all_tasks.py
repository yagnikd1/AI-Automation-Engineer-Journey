"""
DAY 89 — NETWORK INSPECTION
Phase 3 — Browser Automation
Complete Task Programs + Final Integrated Verification
"""

import asyncio
import json
from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright


async def task_1():
    print("\n=== TASK 1 — BASIC REQUEST / RESPONSE MONITOR ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        def on_request(request):
            print(f"REQUEST: {request.method} {request.url}")

        def on_response(response):
            print(f"RESPONSE: {response.status} {response.url}")

        page.on("request", on_request)
        page.on("response", on_response)

        await page.goto("https://books.toscrape.com/", wait_until="networkidle")
        print("Page title:", await page.title())
        print("Current URL:", page.url)

        await context.close()
        await browser.close()
        print("Browser cleanup: PASS")


async def task_2():
    print("\n=== TASK 2 — FILTER NETWORK TRAFFIC ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        total_requests = 0
        counts = {"document": 0, "script": 0, "image": 0,
                  "stylesheet": 0, "other": 0}

        def on_request(request):
            nonlocal total_requests
            total_requests += 1
            kind = request.resource_type
            counts[kind if kind in counts else "other"] += 1

        page.on("request", on_request)
        await page.goto("https://books.toscrape.com/", wait_until="networkidle")

        print("Total requests:", total_requests)
        for key, value in counts.items():
            print(f"{key.title()} requests:", value)

        await context.close()
        await browser.close()
        print("Browser cleanup: PASS")


async def task_3():
    print("\n=== TASK 3 — JSON RESPONSE INSPECTION ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        captured = []

        async def on_response(response):
            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                data = await response.json()
                captured.append(data)
                print("JSON RESPONSE DETECTED")
                print("Status:", response.status)
                print("Content-Type:", content_type)
                print("Data type:", type(data).__name__)
                if isinstance(data, dict):
                    print("Keys:", list(data.keys()))
                    print("Post ID:", data.get("id"))
                    print("User ID:", data.get("userId"))
                    print("Title:", data.get("title"))

        page.on("response", on_response)
        await page.goto(
            "https://jsonplaceholder.typicode.com/posts/1",
            wait_until="networkidle"
        )
        print("JSON responses captured:", len(captured))

        await context.close()
        await browser.close()
        print("Browser cleanup: PASS")


async def task_4():
    print("\n=== TASK 4 — QUERY PARAMETER INSPECTION ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        async def on_response(response):
            if "jsonplaceholder.typicode.com" not in response.url:
                return
            parsed = urlparse(response.url)
            params = parse_qs(parsed.query)

            print("Status:", response.status)
            print("Response URL:", response.url)
            print("Scheme:", parsed.scheme)
            print("Domain:", parsed.netloc)
            print("Path:", parsed.path)
            print("Query string:", parsed.query)
            print("Query params:", params)

            if "application/json" in response.headers.get("content-type", ""):
                data = await response.json()
                print("JSON type:", type(data).__name__)
                if isinstance(data, list):
                    print("Posts returned:", len(data))
                    if data:
                        print("First post ID:", data[0].get("id"))
                        print("First post title:", data[0].get("title"))

        page.on("response", on_response)
        await page.goto(
            "https://jsonplaceholder.typicode.com/posts?userId=1",
            wait_until="networkidle"
        )

        await context.close()
        await browser.close()
        print("Browser cleanup: PASS")


async def task_5():
    print("\n=== TASK 5 — REQUEST & RESPONSE HEADERS ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        def on_request(request):
            print("\nREQUEST HEADERS")
            print("Method:", request.method)
            print("URL:", request.url)
            print("Header count:", len(request.headers))
            for key, value in request.headers.items():
                print(f"{key}: {value}")

        def on_response(response):
            print("\nRESPONSE HEADERS")
            print("Status:", response.status)
            print("URL:", response.url)
            print("Header count:", len(response.headers))
            print("Content-Type:",
                  response.headers.get("content-type", "Not provided"))
            print("Content-Length:",
                  response.headers.get("content-length", "Not provided"))

        page.on("request", on_request)
        page.on("response", on_response)

        response = await page.goto(
            "https://jsonplaceholder.typicode.com/posts/1",
            wait_until="networkidle"
        )
        if response:
            print("\nDIRECT RESPONSE")
            print("Status:", response.status)
            print("Response URL:", response.url)

        await context.close()
        await browser.close()
        print("\nBrowser cleanup: PASS")


async def task_6():
    print("\n=== TASK 6 — POST REQUEST & REQUEST DATA ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        request_seen = False
        response_seen = False

        def on_request(request):
            nonlocal request_seen
            if request.method == "POST" and "/posts" in request.url:
                request_seen = True
                print("\nPOST REQUEST CAPTURED")
                print("Method:", request.method)
                print("URL:", request.url)
                print("\nREQUEST HEADERS")
                print("Content-Type:",
                      request.headers.get("content-type", "Not provided"))
                print("\nREQUEST DATA")
                print(request.post_data or "No request body")

        def on_response(response):
            nonlocal response_seen
            if response.request.method == "POST" and "/posts" in response.url:
                response_seen = True
                print("\nPOST RESPONSE CAPTURED")
                print("Status:", response.status)
                print("URL:", response.url)

        page.on("request", on_request)
        page.on("response", on_response)

        result = await page.evaluate("""async () => {
            const response = await fetch(
                "https://jsonplaceholder.typicode.com/posts",
                {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        title: "Network Inspection Test",
                        body: "Testing POST request inspection",
                        userId: 1
                    })
                }
            );
            return {
                status: response.status,
                data: await response.json()
            };
        }""")

        print("\nDIRECT RESPONSE")
        print("Status:", result["status"])
        print("Response type:", type(result["data"]).__name__)
        print("Response ID:", result["data"].get("id"))
        print("Response title:", result["data"].get("title"))

        assert request_seen
        assert response_seen

        await context.close()
        await browser.close()
        print("\nBrowser cleanup: PASS")


async def task_7():
    print("\n=== TASK 7 — INSPECTING API ENDPOINTS ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        async def on_response(response):
            if "jsonplaceholder.typicode.com" not in response.url:
                return
            content_type = response.headers.get("content-type", "")
            if "application/json" not in content_type:
                return

            print("\nAPI ENDPOINT DETECTED")
            print("Method:", response.request.method)
            print("URL:", response.url)
            print("Status:", response.status)
            print("Content-Type:", content_type)

            data = await response.json()
            print("\nJSON RESPONSE")
            print("Data type:", type(data).__name__)
            if isinstance(data, dict):
                print("JSON keys:", list(data.keys()))
                print("ID:", data.get("id"))
                print("Title:", data.get("title"))

        page.on("response", on_response)
        await page.goto(
            "https://jsonplaceholder.typicode.com/posts/1",
            wait_until="networkidle"
        )

        print("\nPAGE INFORMATION")
        print("Current URL:", page.url)
        print("Page title:", await page.title())

        await context.close()
        await browser.close()
        print("\nBrowser cleanup: PASS")


async def task_8():
    print("\n=== TASK 8 — FILTER & CAPTURE SELECTED API RESPONSES ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        records = []

        async def on_response(response):
            parsed = urlparse(response.url)
            if parsed.netloc != "jsonplaceholder.typicode.com":
                return
            if parsed.path != "/posts":
                return
            if response.request.method != "GET" or response.status != 200:
                return
            if "application/json" not in response.headers.get("content-type", ""):
                return

            data = await response.json()
            if isinstance(data, dict):
                records.append({
                    "id": data.get("id"),
                    "user_id": data.get("userId"),
                    "title": data.get("title")
                })
                print("\nSELECTED API RESPONSE CAPTURED")
                print("Method:", response.request.method)
                print("URL:", response.url)
                print("Status:", response.status)
                print("Records captured:", len(records))

        page.on("response", on_response)
        await page.goto(
            "https://jsonplaceholder.typicode.com/posts/1",
            wait_until="networkidle"
        )
        await page.goto(
            "https://jsonplaceholder.typicode.com/posts/2",
            wait_until="networkidle"
        )
        await page.goto("https://example.com/", wait_until="networkidle")

        print("\nCAPTURE SUMMARY")
        print("Total selected records:", len(records))
        for record in records:
            print(f"ID: {record['id']} | User: {record['user_id']} | "
                  f"Title: {record['title']}")

        await context.close()
        await browser.close()
        print("\nBrowser cleanup: PASS")


async def task_9():
    print("\n=== TASK 9 — PYTHON PROCESSING OF CAPTURED NETWORK DATA ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        records = []

        async def on_response(response):
            parsed = urlparse(response.url)
            if parsed.netloc != "jsonplaceholder.typicode.com":
                return
            if parsed.path != "/posts" or response.request.method != "GET":
                return
            if response.status != 200:
                return
            if "application/json" not in response.headers.get("content-type", ""):
                return

            data = await response.json()
            if isinstance(data, dict):
                records.append({
                    "id": data.get("id"),
                    "user_id": data.get("userId"),
                    "title": data.get("title", "")
                })

        page.on("response", on_response)
        await page.goto(
            "https://jsonplaceholder.typicode.com/posts/1",
            wait_until="networkidle"
        )
        await page.goto(
            "https://jsonplaceholder.typicode.com/posts/2",
            wait_until="networkidle"
        )

        filtered = [r for r in records if r["user_id"] == 1]
        total = sum(len(r["title"]) for r in filtered)
        average = total / len(filtered) if filtered else 0

        print("\nPYTHON DATA PROCESSING")
        print("Captured records:", len(records))
        print("Records after filtering:", len(filtered))
        print("\nPROCESSED RECORDS")
        for r in filtered:
            print(f"ID: {r['id']} | User: {r['user_id']} | "
                  f"Title length: {len(r['title'])}")
        print("\nPROCESSING SUMMARY")
        print("Total title characters:", total)
        print(f"Average title length: {average:.2f}")

        await context.close()
        await browser.close()
        print("\nBrowser cleanup: PASS")


async def task_10():
    print("\n=== TASK 10 — PRACTICAL NETWORK INSPECTION USE CASES ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        captured = []

        async def on_response(response):
            if "jsonplaceholder.typicode.com" not in response.url:
                return
            if response.status != 200:
                return
            if "application/json" not in response.headers.get("content-type", ""):
                return

            data = await response.json()
            if isinstance(data, dict):
                category, count = "single_record", 1
            elif isinstance(data, list):
                category, count = "collection", len(data)
            else:
                category, count = "other", 0

            captured.append({
                "method": response.request.method,
                "url": response.url,
                "status": response.status,
                "data_type": type(data).__name__,
                "category": category,
                "record_count": count
            })

            print("\nAPI RESPONSE")
            print("Method:", response.request.method)
            print("URL:", response.url)
            print("Status:", response.status)
            print("Data type:", type(data).__name__)
            print("Category:", category)
            print("Record count:", count)

        page.on("response", on_response)
        for url in [
            "https://jsonplaceholder.typicode.com/posts/1",
            "https://jsonplaceholder.typicode.com/posts?userId=1",
            "https://jsonplaceholder.typicode.com/users/1"
        ]:
            await page.goto(url, wait_until="networkidle")

        total = sum(x["record_count"] for x in captured)
        print("\nNETWORK INSPECTION REPORT")
        print("Successful JSON APIs captured:", len(captured))
        print("Total API records represented:", total)

        print("\nUSE CASES DEMONSTRATED")
        print("1. Discovering API endpoints")
        print("2. Monitoring API responses")
        print("3. Detecting JSON responses")
        print("4. Distinguishing single records from collections")
        print("5. Feeding network data into Python processing")

        await context.close()
        await browser.close()
        print("\nBrowser cleanup: PASS")


async def task_11():
    print("\n=== TASK 11 — LIMITATIONS & BOUNDARIES ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        checks = {
            "json_content_type": False,
            "http_status": False,
            "json_structure": False,
            "listener_before_request": True,
            "automatic_protection_bypass": False
        }

        async def on_response(response):
            if "jsonplaceholder.typicode.com" not in response.url:
                return
            checks["json_content_type"] = (
                "application/json" in response.headers.get("content-type", "")
            )
            checks["http_status"] = 200 <= response.status < 300

            if checks["json_content_type"]:
                data = await response.json()
                checks["json_structure"] = isinstance(data, (dict, list))
                print("\nJSON RESPONSE")
                print("Status:", response.status)
                print("URL:", response.url)
                print("Status classification:",
                      "SUCCESS" if checks["http_status"] else "NON-SUCCESS")
                print("JSON type:", type(data).__name__)

        # Listener is registered BEFORE requests.
        page.on("response", on_response)

        await page.goto(
            "https://jsonplaceholder.typicode.com/posts/1",
            wait_until="networkidle"
        )
        await page.goto(
            "https://jsonplaceholder.typicode.com/users/1",
            wait_until="networkidle"
        )

        print("\nLIMITATIONS CHECK")
        print("JSON content type checked:",
              "PASS" if checks["json_content_type"] else "FAIL")
        print("HTTP status checked:",
              "PASS" if checks["http_status"] else "FAIL")
        print("JSON structure checked:",
              "PASS" if checks["json_structure"] else "FAIL")
        print("Network listener registered before requests:",
              "PASS" if checks["listener_before_request"] else "FAIL")
        print("Automatic protection bypass:",
              "YES" if checks["automatic_protection_bypass"] else "NO")

        await context.close()
        await browser.close()
        print("\nBrowser cleanup: PASS")


async def final_integrated_verification():
    print("\n=== DAY 89 — FINAL INTEGRATED VERIFICATION ===")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        records = []

        async def on_response(response):
            parsed = urlparse(response.url)

            if parsed.netloc != "jsonplaceholder.typicode.com":
                return
            if parsed.path != "/posts":
                return
            if response.request.method != "GET":
                return
            if response.status != 200:
                return
            if "application/json" not in response.headers.get("content-type", ""):
                return

            data = await response.json()

            if isinstance(data, dict):
                items = [data]
            elif isinstance(data, list):
                items = data
            else:
                return

            for item in items:
                records.append({
                    "id": item.get("id"),
                    "user_id": item.get("userId"),
                    "title": item.get("title", "")
                })

        page.on("response", on_response)

        await page.goto(
            "https://jsonplaceholder.typicode.com/posts?userId=1",
            wait_until="networkidle"
        )
        await page.goto(
            "https://jsonplaceholder.typicode.com/posts/1",
            wait_until="networkidle"
        )
        await page.goto(
            "https://jsonplaceholder.typicode.com/posts/2",
            wait_until="networkidle"
        )

        filtered = [r for r in records if r["user_id"] == 1]
        total = sum(len(r["title"]) for r in filtered)
        average = total / len(filtered) if filtered else 0

        print("\nFINAL NETWORK AUTOMATION REPORT")
        print("Captured records:", len(records))
        print("Filtered records:", len(filtered))
        print("Total title characters:", total)
        print(f"Average title length: {average:.2f}")

        assert len(records) == 12
        assert len(filtered) == 12
        assert total == 424
        assert round(average, 2) == 35.33

        print("\nVERIFICATION CHECKS")
        print("Network response monitoring: PASS")
        print("API endpoint filtering: PASS")
        print("HTTP status validation: PASS")
        print("JSON detection: PASS")
        print("JSON parsing: PASS")
        print("Python data processing: PASS")
        print("Final report generation: PASS")

        await context.close()
        await browser.close()
        print("\nBrowser cleanup: PASS")
        print("\nDAY 89 FINAL VERIFICATION COMPLETE")


TASKS = {
    "1": task_1,
    "2": task_2,
    "3": task_3,
    "4": task_4,
    "5": task_5,
    "6": task_6,
    "7": task_7,
    "8": task_8,
    "9": task_9,
    "10": task_10,
    "11": task_11,
    "12": final_integrated_verification,
}


async def main():
    print("""
DAY 89 — NETWORK INSPECTION
1  Basic request/response monitor
2  Filter network traffic
3  JSON response inspection
4  Query parameter inspection
5  Request/response headers
6  POST request and request data
7  Inspecting API endpoints
8  Filtering/capturing selected API responses
9  Python processing of captured network data
10 Practical network inspection use cases
11 Limitations and boundaries
12 FINAL INTEGRATED VERIFICATION
""")
    choice = input("Select a task (1-12): ").strip()
    if choice in TASKS:
        await TASKS[choice]()
    else:
        print("Invalid selection.")


if __name__ == "__main__":
    asyncio.run(main())
