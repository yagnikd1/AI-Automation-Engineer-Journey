"""
DAY 43 — SQLITE DATABASE STORAGE AND ADVANCED DATA MANAGEMENT
Complete GitHub-Ready Study Guide

Completion status
-----------------
Phase 1 — Python Fundamentals: Completed
Phase 2 — Web Scraping and Data Collection: In progress
Day 43 — SQLite Part 1 and Part 2: Completed

This file contains:
1. A compact historical revision program from the start of Day 43.
2. SQLite Part 1: a live USGS earthquake API-to-database monitor.
3. SQLite Part 2: a municipal infrastructure work-order lifecycle manager.
4. Detailed comments explaining every SQL concept and major failure case.

Permanent teaching rule added on Day 43
---------------------------------------
Future lessons must never reuse a previous program or explanatory example.
Every new program and example must use a genuinely different, realistic,
career-relevant problem and dataset. The revision program below is preserved
only because it was completed before that permanent rule was established.

Python requirements
-------------------
Built in: sqlite3, csv, json, datetime, random, time
External: requests, beautifulsoup4

Install external packages if necessary:
    pip install requests beautifulsoup4
"""

from __future__ import annotations

import csv
import json
import random
import sqlite3
import time
from datetime import datetime, timezone

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    # SQLite Part 2 uses only the standard library and can still run without
    # these optional web-scraping dependencies. Options 1 and 2 explain how to
    # install them when selected.
    requests = None
    BeautifulSoup = None


# ============================================================================
# SECTION 1 — COMPACT HISTORICAL REVISION PROGRAM
# ============================================================================
# Program name: Multi-Page Book Inventory and Price Analyzer
# Purpose: Collect three catalogue pages, analyze prices and availability,
# and export the records to CSV and JSON.
# Career connection: The structure resembles a basic catalogue audit or
# competitor inventory monitor.
# Important: This scenario must not be reused in future lessons.

REVISION_BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"


def collect_revision_page(session: requests.Session, page_number: int) -> list[dict]:
    """Collect and normalize all books on one catalogue page."""
    url = REVISION_BASE_URL.format(page_number)

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()

        # The lesson initially received text similar to "Â£51.77" because the
        # response was decoded incorrectly. Setting UTF-8 fixes the source
        # decoding instead of merely deleting unexpected characters later.
        response.encoding = "utf-8"

    except requests.RequestException as error:
        print(f"Page {page_number} failed: {error}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    page_books: list[dict] = []

    for card in soup.select("article.product_pod"):
        title_element = card.select_one("h3 a")
        price_element = card.select_one(".price_color")
        stock_element = card.select_one(".availability")

        if not title_element or not price_element or not stock_element:
            continue

        title = title_element.get("title", "Unknown title")
        price = float(price_element.get_text(strip=True).replace("£", ""))
        availability = stock_element.get_text(strip=True)

        page_books.append(
            {
                "title": title,
                "price": price,
                "in_stock": "In stock" in availability,
            }
        )

    # Debugging lesson: this return must remain OUTSIDE the for loop. When it
    # was accidentally inside the loop, only one book per page was collected.
    return page_books


def run_compact_revision() -> None:
    """Run the completed compact Python + web-scraping revision."""
    if requests is None or BeautifulSoup is None:
        print("Install web dependencies first: pip install requests beautifulsoup4")
        return

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    session.cookies.set("currency", "GBP")

    all_books: list[dict] = []

    for page_number in range(1, 4):
        page_books = collect_revision_page(session, page_number)
        all_books.extend(page_books)
        print(f"Page {page_number}: {len(page_books)} books collected")
        time.sleep(random.uniform(0.5, 1.0))

    available_books: list[dict] = []
    budget_books: list[dict] = []
    total_price = 0.0

    for book in all_books:
        if book["in_stock"]:
            available_books.append(book)
            total_price += book["price"]

            if book["price"] <= 20:
                budget_books.append(book)

    if available_books:
        average_price = total_price / len(available_books)
        cheapest_book = min(available_books, key=lambda item: item["price"])
        most_expensive_book = max(
            available_books,
            key=lambda item: item["price"],
        )

        print("\n--- COLLECTION SUMMARY ---")
        print(f"Total books: {len(all_books)}")
        print(f"Available books: {len(available_books)}")
        print(f"Books costing £20 or less: {len(budget_books)}")
        print(f"Average price: £{average_price:.2f}")
        print(
            f"Cheapest: {cheapest_book['title']} "
            f"— £{cheapest_book['price']:.2f}"
        )
        print(
            f"Most expensive: {most_expensive_book['title']} "
            f"— £{most_expensive_book['price']:.2f}"
        )
    else:
        print("No available books were collected.")

    with open("day43_revision_books.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["title", "price", "in_stock"],
        )
        writer.writeheader()
        writer.writerows(all_books)

    with open("day43_revision_books.json", "w", encoding="utf-8") as file:
        json.dump(all_books, file, indent=4, ensure_ascii=False)

    print("Revision data saved to CSV and JSON.")


# ============================================================================
# SECTION 2 — SQLITE PART 1: USGS EARTHQUAKE EVENT DATABASE
# ============================================================================
# SQL is the language used to communicate with databases.
# SQLite is a lightweight database engine that understands SQL.
# Python's sqlite3 module is built in; no pip installation is required.
#
# Data flow:
# USGS GeoJSON feed -> Python dictionaries -> validation -> SQLite table
# -> parameterized INSERT -> duplicate protection -> analytical SELECT report

USGS_API_URL = (
    "https://earthquake.usgs.gov/earthquakes/"
    "feed/v1.0/summary/all_hour.geojson"
)
EARTHQUAKE_DATABASE = "usgs_earthquake_monitor.db"


def fetch_earthquakes() -> list[dict]:
    """Fetch the live past-hour USGS GeoJSON summary feed."""
    if requests is None:
        print("Install the required dependency first: pip install requests")
        return []

    try:
        response = requests.get(USGS_API_URL, timeout=15)
        response.raise_for_status()
        api_data = response.json()

    except (requests.RequestException, ValueError) as error:
        print(f"USGS request failed: {error}")
        return []

    if not isinstance(api_data, dict):
        print("USGS response had an unexpected top-level structure.")
        return []

    features = api_data.get("features", [])
    return features if isinstance(features, list) else []


def initialize_earthquake_database() -> None:
    """Create the earthquake table and guarantee connection cleanup."""
    connection = sqlite3.connect(EARTHQUAKE_DATABASE)

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS earthquakes (
                event_id TEXT PRIMARY KEY,
                location TEXT NOT NULL,
                magnitude REAL,
                event_time INTEGER NOT NULL,
                event_url TEXT NOT NULL
            )
            """
        )
        connection.commit()

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


def store_earthquakes(features: list[dict]) -> tuple[int, int, int]:
    """Insert new events and ignore duplicate primary keys."""
    connection = sqlite3.connect(EARTHQUAKE_DATABASE)

    insert_query = """
        INSERT OR IGNORE INTO earthquakes (
            event_id,
            location,
            magnitude,
            event_time,
            event_url
        )
        VALUES (?, ?, ?, ?, ?)
    """

    inserted_count = 0
    duplicate_count = 0
    invalid_count = 0

    try:
        cursor = connection.cursor()

        for feature in features:
            if not isinstance(feature, dict):
                invalid_count += 1
                continue

            properties = feature.get("properties", {})
            if not isinstance(properties, dict):
                invalid_count += 1
                continue

            event_id = feature.get("id")
            location = properties.get("place") or "Unknown location"
            magnitude = properties.get("mag")
            event_time = properties.get("time")
            event_url = properties.get("url") or ""

            if not event_id or event_time is None:
                invalid_count += 1
                continue

            event_record = (
                event_id,
                location,
                magnitude,
                event_time,
                event_url,
            )

            cursor.execute(insert_query, event_record)

            if cursor.rowcount == 1:
                inserted_count += 1
            else:
                duplicate_count += 1

        connection.commit()
        return inserted_count, duplicate_count, invalid_count

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


def generate_earthquake_report() -> None:
    """Read aggregate, strongest-event, and latest-event results."""
    connection = sqlite3.connect(EARTHQUAKE_DATABASE)

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*), AVG(magnitude)
            FROM earthquakes
            """
        )
        total_records, average_magnitude = cursor.fetchone()

        cursor.execute(
            """
            SELECT location, magnitude, event_time, event_url
            FROM earthquakes
            WHERE magnitude IS NOT NULL
            ORDER BY magnitude DESC
            LIMIT 1
            """
        )
        strongest_event = cursor.fetchone()

        cursor.execute(
            """
            SELECT location, magnitude, event_time
            FROM earthquakes
            ORDER BY event_time DESC
            LIMIT 5
            """
        )
        latest_events = cursor.fetchall()

    finally:
        connection.close()

    print("\n--- EARTHQUAKE DATABASE REPORT ---")
    print(f"Total stored events: {total_records}")
    print(
        f"Average magnitude: {average_magnitude:.2f}"
        if average_magnitude is not None
        else "Average magnitude: unavailable"
    )

    if strongest_event:
        location, magnitude, event_time, event_url = strongest_event
        readable_time = datetime.fromtimestamp(
            event_time / 1000,
            tz=timezone.utc,
        ).strftime("%Y-%m-%d %H:%M:%S UTC")

        print("\nStrongest stored event:")
        print(f"Location: {location}")
        print(f"Magnitude: {magnitude}")
        print(f"Time: {readable_time}")
        print(f"Details: {event_url}")

    print("\nFive latest stored events:")

    for location, magnitude, event_time in latest_events:
        readable_time = datetime.fromtimestamp(
            event_time / 1000,
            tz=timezone.utc,
        ).strftime("%Y-%m-%d %H:%M:%S UTC")
        print(f"- {readable_time} | Magnitude {magnitude} | {location}")


def run_earthquake_monitor() -> None:
    """Run the complete SQLite Part 1 project."""
    initialize_earthquake_database()
    features = fetch_earthquakes()

    print(f"Live earthquake events received: {len(features)}")

    if not features:
        print("No current earthquake information was available.")
        return

    inserted, duplicates, invalid = store_earthquakes(features)
    print(f"New database records: {inserted}")
    print(f"Duplicate events skipped: {duplicates}")
    print(f"Invalid events skipped: {invalid}")
    generate_earthquake_report()


# ============================================================================
# SECTION 3 — SQLITE PART 2: WORK-ORDER LIFECYCLE MANAGER
# ============================================================================
# Purpose: Maintain infrastructure records through their full lifecycle.
# New SQL concepts:
# WHERE, AND, NOT IN, UPDATE, DELETE, UPSERT, ON CONFLICT, excluded.column,
# transactions, rollback, GROUP BY, aliases, CREATE INDEX, EXPLAIN QUERY PLAN.

WORK_ORDER_DATABASE = "infrastructure_work_orders.db"

INITIAL_WORK_ORDERS = [
    ("WO-1041", "Water pipeline", "North District", 5, "Open", 18500.00),
    ("WO-1042", "Traffic signal", "Central District", 4, "In Progress", 7200.00),
    ("WO-1043", "Public footbridge", "West District", 3, "Inspection", 42000.00),
    ("WO-1044", "Drainage system", "South District", 5, "Open", 12800.00),
    ("WO-1045", "Street lighting", "East District", 2, "Closed", 3100.00),
]

REVISED_WORK_ORDERS = [
    ("WO-1042", "Traffic signal", "Central District", 5, "Completed", 7800.00),
    ("WO-1046", "Retaining wall", "West District", 4, "Open", 25500.00),
]

UPSERT_WORK_ORDER = """
    INSERT INTO work_orders (
        work_order_id,
        asset_type,
        district,
        priority,
        status,
        estimated_cost
    )
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(work_order_id)
    DO UPDATE SET
        asset_type = excluded.asset_type,
        district = excluded.district,
        priority = excluded.priority,
        status = excluded.status,
        estimated_cost = excluded.estimated_cost
"""


def create_work_order_schema(cursor: sqlite3.Cursor) -> None:
    """Create the table and the composite search index."""
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS work_orders (
            work_order_id TEXT PRIMARY KEY,
            asset_type TEXT NOT NULL,
            district TEXT NOT NULL,
            priority INTEGER NOT NULL,
            status TEXT NOT NULL,
            estimated_cost REAL NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_work_orders_status_priority
        ON work_orders(status, priority)
        """
    )


def insert_initial_work_orders(
    cursor: sqlite3.Cursor,
    records: list[tuple],
) -> None:
    """Insert first-seen records while preserving already stored values."""
    insert_query = """
        INSERT OR IGNORE INTO work_orders (
            work_order_id,
            asset_type,
            district,
            priority,
            status,
            estimated_cost
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """

    for record in records:
        cursor.execute(insert_query, record)


def update_work_order(
    cursor: sqlite3.Cursor,
    status: str,
    estimated_cost: float,
    work_order_id: str,
) -> int:
    """Update exactly one selected work order with parameterized SQL."""
    cursor.execute(
        """
        UPDATE work_orders
        SET status = ?, estimated_cost = ?
        WHERE work_order_id = ?
        """,
        (status, estimated_cost, work_order_id),
    )
    return cursor.rowcount


def delete_closed_low_priority_orders(
    cursor: sqlite3.Cursor,
    maximum_priority: int,
) -> tuple[list[tuple], int]:
    """Preview and then delete only the approved cleanup candidates."""
    conditions = ("Closed", maximum_priority)

    cursor.execute(
        """
        SELECT work_order_id, asset_type, priority, status
        FROM work_orders
        WHERE status = ? AND priority <= ?
        """,
        conditions,
    )
    candidates = cursor.fetchall()

    if not candidates:
        return [], 0

    cursor.execute(
        """
        DELETE FROM work_orders
        WHERE status = ? AND priority <= ?
        """,
        conditions,
    )
    return candidates, cursor.rowcount


def upsert_work_orders(
    cursor: sqlite3.Cursor,
    records: list[tuple],
) -> tuple[int, int]:
    """Insert new IDs and update existing IDs in one incoming batch."""
    inserted_count = 0
    updated_count = 0

    for record in records:
        work_order_id = record[0]

        cursor.execute(
            "SELECT 1 FROM work_orders WHERE work_order_id = ?",
            (work_order_id,),
        )
        existed = cursor.fetchone() is not None

        cursor.execute(UPSERT_WORK_ORDER, record)

        if existed:
            updated_count += 1
        else:
            inserted_count += 1

    return inserted_count, updated_count


def print_urgent_work_orders(cursor: sqlite3.Cursor) -> None:
    """Show active priority-four-or-higher work after all mutations finish."""
    cursor.execute(
        """
        SELECT
            work_order_id,
            asset_type,
            district,
            priority,
            status,
            estimated_cost
        FROM work_orders
        WHERE priority >= ? AND status NOT IN (?, ?)
        ORDER BY priority DESC
        """,
        (4, "Closed", "Completed"),
    )

    print("\n--- URGENT ACTIVE WORK ORDERS ---")

    for order_id, asset, district, priority, status, cost in cursor.fetchall():
        print(
            f"{order_id} | {asset} | {district} | "
            f"Priority {priority} | {status} | ${cost:,.2f}"
        )


def print_status_summary(cursor: sqlite3.Cursor) -> None:
    """Group work orders by status and calculate operational totals."""
    cursor.execute(
        """
        SELECT
            status,
            COUNT(*) AS order_count,
            SUM(estimated_cost) AS total_cost,
            AVG(priority) AS average_priority
        FROM work_orders
        GROUP BY status
        ORDER BY total_cost DESC
        """
    )

    print("\n--- WORK-ORDER STATUS SUMMARY ---")

    for status, order_count, total_cost, average_priority in cursor.fetchall():
        print(f"Status: {status}")
        print(f"Orders: {order_count}")
        print(f"Total estimated cost: ${total_cost:,.2f}")
        print(f"Average priority: {average_priority:.2f}")
        print("-" * 40)


def print_index_query_plan(cursor: sqlite3.Cursor) -> None:
    """Prove that SQLite uses the composite status/priority index."""
    cursor.execute(
        """
        EXPLAIN QUERY PLAN
        SELECT work_order_id, asset_type, status, priority
        FROM work_orders
        WHERE status = ? AND priority >= ?
        """,
        ("Open", 4),
    )

    print("\n--- INDEX QUERY PLAN ---")
    for plan_row in cursor.fetchall():
        print(plan_row)


def run_work_order_manager() -> None:
    """Run the final SQLite Part 2 lifecycle-management project."""
    connection: sqlite3.Connection | None = None

    try:
        connection = sqlite3.connect(WORK_ORDER_DATABASE)
        cursor = connection.cursor()

        create_work_order_schema(cursor)
        insert_initial_work_orders(cursor, INITIAL_WORK_ORDERS)
        connection.commit()

        updated_rows = update_work_order(
            cursor,
            status="In Progress",
            estimated_cost=19750.00,
            work_order_id="WO-1041",
        )
        connection.commit()
        print(
            "\nWork order WO-1041 updated successfully."
            if updated_rows == 1
            else "\nWork order WO-1041 was not found."
        )

        candidates, deleted_rows = delete_closed_low_priority_orders(
            cursor,
            maximum_priority=2,
        )
        connection.commit()

        print("\n--- RECORDS SELECTED FOR DELETION ---")
        for candidate in candidates:
            print(candidate)
        print(f"Records permanently deleted: {deleted_rows}")

        # One logical batch: either every revised record is saved or rollback
        # removes the batch's uncommitted changes.
        inserted_count, updated_count = upsert_work_orders(
            cursor,
            REVISED_WORK_ORDERS,
        )
        connection.commit()

        print("\n--- UPSERT RESULTS ---")
        print(f"New records inserted: {inserted_count}")
        print(f"Existing records updated: {updated_count}")

        # Reports intentionally run after all state changes, preventing stale
        # results. Completed and closed rows are not classified as active.
        print_urgent_work_orders(cursor)
        print_status_summary(cursor)
        print_index_query_plan(cursor)

    except sqlite3.Error as error:
        if connection is not None:
            connection.rollback()
        print(f"\nDatabase operation failed: {error}")

    finally:
        if connection is not None:
            connection.close()
            print("\nDatabase connection closed.")


# ============================================================================
# SECTION 4 — FAILURE CHECKLIST AND ROADMAP HANDOFF
# ============================================================================
FAILURE_CHECKLIST = """
Key failures studied on Day 43
------------------------------
1. Wrong response encoding can create characters such as Â before a price.
2. return inside a loop stops collection after the first item.
3. Duplicate primary keys raise sqlite3.IntegrityError with plain INSERT.
4. A cursor cannot operate after connection.close().
5. Missing WHERE can update or delete every database row.
6. Placeholder order must match the SQL column/value order.
7. INSERT OR IGNORE can preserve stale data; UPSERT can update it.
8. A failed batch needs rollback to avoid partial results.
9. Inconsistent labels create separate GROUP BY groups.
10. Too many or poorly ordered indexes can slow writes without helping reads.
11. Reports must run after mutations or they may display stale values.
12. Completed records must not be classified as urgent active work.
13. Code under try must be indented before except/finally.
14. finally guarantees connection cleanup even after failure.

"""


def main() -> None:
    """Provide one GitHub-ready launcher for the three Day 43 programs."""
    print("DAY 43 — SQLITE COMPLETE STUDY GUIDE")
    print("1. Compact historical revision")
    print("2. SQLite Part 1 — USGS Earthquake Monitor")
    print("3. SQLite Part 2 — Work-Order Lifecycle Manager")
    print("4. Print failure checklist")

    choice = input("Choose 1, 2, 3, or 4: ").strip()

    if choice == "1":
        run_compact_revision()
    elif choice == "2":
        run_earthquake_monitor()
    elif choice == "3":
        run_work_order_manager()
    elif choice == "4":
        print(FAILURE_CHECKLIST)
    else:
        print("Invalid choice. Run the program again and choose 1–4.")


if __name__ == "__main__":
    main()
