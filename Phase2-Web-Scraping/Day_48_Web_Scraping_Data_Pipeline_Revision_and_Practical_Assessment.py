"""
Day 48 - Web Scraping Data Pipeline Revision and Practical Assessment
=====================================================================

Topics covered
--------------
1. Parse static HTML with BeautifulSoup.
2. Select repeated cards with CSS selectors.
3. Extract text and data-* attributes safely.
4. Clean integer, decimal, free, missing, and unusable values.
5. Validate records and retain precise rejection reasons.
6. Detect duplicates with a set.
7. Analyse only the records appropriate for each calculation.
8. Store data in CSV, JSON, and SQLite.
9. Reopen or query every output to verify actual persistence.
10. Prevent duplicate database rows when the program is rerun.

Install dependency if needed:
    pip install beautifulsoup4

Run:
    python Day_48_Web_Scraping_Data_Pipeline_Revision_and_Practical_Assessment.py

This file uses embedded training HTML. It does not contact or scrape a live
website. For live scraping, check the site's Terms of Service and robots.txt
before sending requests; do not continue when scraping is prohibited.
"""

import csv
import json
import sqlite3
from pathlib import Path

from bs4 import BeautifulSoup


BASE_OUTPUT_DIRECTORY = Path("day48_complete_output")


def clean_integer(text):
    """Return the digits in text as an integer, or None when no digits exist."""
    digits = ""

    for character in text:
        if character.isdigit():
            digits += character

    return int(digits) if digits else None


def clean_hourly_rate(text):
    """Convert 'Free' to 0.0, a dollar rate to float, or bad input to None."""
    cleaned_text = text.strip()

    if cleaned_text.lower() == "free":
        return 0.0

    if cleaned_text.startswith("$"):
        price_text = (
            cleaned_text
            .replace("$", "")
            .replace(" per hour", "")
            .strip()
        )

        try:
            return float(price_text)
        except ValueError:
            return None

    return None


def read_csv_records(csv_path):
    """Reopen a CSV file and return all stored rows."""
    with csv_path.open("r", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def read_json_data(json_path):
    """Reopen a JSON file and return the decoded data."""
    with json_path.open("r", encoding="utf-8") as json_file:
        return json.load(json_file)


def run_guided_revision():
    """Run the guided Public Transport Service Notice Analyzer."""
    print("=" * 72)
    print("PART 1 - GUIDED REVISION: PUBLIC TRANSPORT SERVICE NOTICES")
    print("=" * 72)

    html_document = """
    <html>
        <body>
            <article class="service-notice" data-status="active">
                <h2>Central Line Maintenance</h2>
                <span class="category">Rail</span>
                <span class="affected-stops">6 stops</span>
                <span class="delay">20 minutes</span>
            </article>

            <article class="service-notice" data-status="resolved">
                <h2>Riverside Bus Diversion</h2>
                <span class="category">Bus</span>
                <span class="affected-stops">4 stops</span>
                <span class="delay">15 minutes</span>
            </article>

            <article class="service-notice" data-status="active">
                <h2>Airport Express Delay</h2>
                <span class="category">Rail</span>
                <span class="affected-stops">3 stops</span>
                <span class="delay">35 minutes</span>
            </article>

            <article class="service-notice" data-status="active">
                <h2>Incomplete Service Notice</h2>
                <span class="category"></span>
            </article>
        </body>
    </html>
    """

    # EXTRACT AND CLEAN
    soup = BeautifulSoup(html_document, "html.parser")
    notice_cards = soup.select("article.service-notice")
    notices = []

    for card in notice_cards:
        title_element = card.select_one("h2")
        category_element = card.select_one(".category")
        affected_stops_element = card.select_one(".affected-stops")
        delay_element = card.select_one(".delay")

        title = title_element.get_text(strip=True) if title_element else ""
        category = (
            category_element.get_text(strip=True)
            if category_element
            else ""
        )
        status = card.get("data-status", "").strip().lower()
        affected_stops_text = (
            affected_stops_element.get_text(strip=True)
            if affected_stops_element
            else ""
        )
        delay_text = (
            delay_element.get_text(strip=True)
            if delay_element
            else ""
        )

        notice = {
            "title": title,
            "category": category,
            "status": status,
            "affected_stops": clean_integer(affected_stops_text),
            "delay_minutes": clean_integer(delay_text),
        }
        notices.append(notice)

    print("\nNotice cards found:", len(notice_cards))
    print("\nExtracted notices:")
    for notice in notices:
        print(notice)

    # VALIDATE WITHOUT SILENTLY DISCARDING BAD DATA
    valid_notices = []
    rejected_notices = []

    for notice in notices:
        problems = []

        if notice["title"] == "":
            problems.append("missing title")

        if notice["category"] == "":
            problems.append("missing category")

        if notice["status"] not in ["active", "resolved"]:
            problems.append("invalid status")

        if notice["affected_stops"] is None:
            problems.append("missing affected-stops value")
        elif notice["affected_stops"] < 0:
            problems.append("affected-stops value cannot be negative")

        if notice["delay_minutes"] is None:
            problems.append("missing delay value")
        elif notice["delay_minutes"] < 0:
            problems.append("delay value cannot be negative")

        if problems:
            rejected_notices.append({
                "notice": notice,
                "problems": problems,
            })
        else:
            valid_notices.append(notice)

    print("\nValidation results:")
    print("Valid notices:", len(valid_notices))
    print("Rejected notices:", len(rejected_notices))

    print("\nRejected-record details:")
    for rejected_record in rejected_notices:
        print("Title:", rejected_record["notice"]["title"])
        print("Problems:", ", ".join(rejected_record["problems"]))

    # ANALYSE VALID RECORDS
    active_notices = [
        notice
        for notice in valid_notices
        if notice["status"] == "active"
    ]

    total_affected_stops = sum(
        notice["affected_stops"]
        for notice in active_notices
    )
    total_delay_minutes = sum(
        notice["delay_minutes"]
        for notice in active_notices
    )

    if active_notices:
        average_delay = total_delay_minutes / len(active_notices)
        longest_delay_notice = max(
            active_notices,
            key=lambda notice: notice["delay_minutes"],
        )
    else:
        average_delay = 0
        longest_delay_notice = None

    category_counts = {}

    for notice in valid_notices:
        category = notice["category"]
        category_counts[category] = category_counts.get(category, 0) + 1

    print("\nAnalysis results:")
    print("Active notices:", len(active_notices))
    print(
        "Total affected stops from active notices:",
        total_affected_stops,
    )
    print(f"Average active delay: {average_delay:.2f} minutes")

    if longest_delay_notice:
        print(
            "Longest active delay:",
            longest_delay_notice["title"],
            f"({longest_delay_notice['delay_minutes']} minutes)",
        )
    else:
        print("Longest active delay: None")

    print("Valid notices by category:")
    for category, count in category_counts.items():
        print(f"- {category}: {count}")

    # STORE RESULTS
    output_directory = BASE_OUTPUT_DIRECTORY / "guided_revision"
    output_directory.mkdir(parents=True, exist_ok=True)

    csv_path = output_directory / "valid_service_notices.csv"
    json_path = output_directory / "service_notice_audit.json"
    database_path = output_directory / "service_notices.db"

    fieldnames = [
        "title",
        "category",
        "status",
        "affected_stops",
        "delay_minutes",
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(valid_notices)

    audit_data = {
        "valid_notices": valid_notices,
        "rejected_notices": rejected_notices,
    }

    with json_path.open("w", encoding="utf-8") as json_file:
        json.dump(audit_data, json_file, indent=4, ensure_ascii=False)

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS service_notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL,
            affected_stops INTEGER NOT NULL,
            delay_minutes INTEGER NOT NULL
        )
        """
    )

    # The training dataset is a complete snapshot. Clearing the table prevents
    # duplicate rows when this demonstration is run repeatedly.
    cursor.execute("DELETE FROM service_notices")

    for notice in valid_notices:
        cursor.execute(
            """
            INSERT INTO service_notices (
                title,
                category,
                status,
                affected_stops,
                delay_minutes
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                notice["title"],
                notice["category"],
                notice["status"],
                notice["affected_stops"],
                notice["delay_minutes"],
            ),
        )

    connection.commit()

    # VERIFY THE STORED OUTPUTS
    stored_csv_records = read_csv_records(csv_path)
    stored_audit_data = read_json_data(json_path)

    cursor.execute("SELECT COUNT(*) FROM service_notices")
    stored_database_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT title, delay_minutes
        FROM service_notices
        ORDER BY delay_minutes DESC
        LIMIT 1
        """
    )
    database_longest_delay = cursor.fetchone()
    connection.close()

    print("\nStorage verification:")
    print("CSV records stored:", len(stored_csv_records))
    print(
        "JSON valid records stored:",
        len(stored_audit_data["valid_notices"]),
    )
    print(
        "JSON rejected records stored:",
        len(stored_audit_data["rejected_notices"]),
    )
    print("SQLite records stored:", stored_database_count)

    if database_longest_delay:
        print(
            "SQLite longest delay:",
            database_longest_delay[0],
            f"({database_longest_delay[1]} minutes)",
        )

    print("\nCreated guided-revision files:")
    print("-", csv_path)
    print("-", json_path)
    print("-", database_path)


def run_practical_assessment():
    """Run the accelerated Public Study-Room Availability Analyzer."""
    print("\n" + "=" * 72)
    print("PART 2 - PRACTICAL ASSESSMENT: PUBLIC STUDY-ROOM AVAILABILITY")
    print("=" * 72)

    html_document = """
    <html>
        <body>
            <div class="room-card" data-room-id="R-201" data-status="available">
                <h2>Atlas Room</h2>
                <span class="floor">Second Floor</span>
                <span class="capacity">8 people</span>
                <span class="hourly-rate">$12.50 per hour</span>
            </div>

            <div class="room-card" data-room-id="R-202" data-status="available">
                <h2>Harbor Room</h2>
                <span class="floor">First Floor</span>
                <span class="capacity">4 people</span>
                <span class="hourly-rate">Free</span>
            </div>

            <div class="room-card"
                 data-room-id="R-203"
                 data-status="unavailable">
                <h2>Summit Room</h2>
                <span class="floor">Third Floor</span>
                <span class="capacity">12 people</span>
                <span class="hourly-rate">$18.00 per hour</span>
            </div>

            <div class="room-card" data-room-id="R-201" data-status="available">
                <h2>Atlas Room</h2>
                <span class="floor">Second Floor</span>
                <span class="capacity">8 people</span>
                <span class="hourly-rate">$12.50 per hour</span>
            </div>

            <div class="room-card" data-room-id="R-204" data-status="available">
                <h2>Incomplete Room</h2>
                <span class="floor"></span>
                <span class="capacity">unknown</span>
            </div>
        </body>
    </html>
    """

    # EXTRACT AND CLEAN
    soup = BeautifulSoup(html_document, "html.parser")
    room_cards = soup.select("div.room-card")
    rooms = []

    for room_card in room_cards:
        room_id = room_card.get("data-room-id", "").strip()
        name_element = room_card.select_one("h2")
        floor_element = room_card.select_one(".floor")
        capacity_element = room_card.select_one(".capacity")
        hourly_rate_element = room_card.select_one(".hourly-rate")

        name = name_element.get_text(strip=True) if name_element else ""
        floor = floor_element.get_text(strip=True) if floor_element else ""
        status = room_card.get("data-status", "").strip().lower()
        capacity_text = (
            capacity_element.get_text(strip=True)
            if capacity_element
            else ""
        )
        hourly_rate_text = (
            hourly_rate_element.get_text(strip=True)
            if hourly_rate_element
            else ""
        )

        room = {
            "room_id": room_id,
            "name": name,
            "floor": floor,
            "status": status,
            "capacity": clean_integer(capacity_text),
            "hourly_rate": clean_hourly_rate(hourly_rate_text),
        }
        rooms.append(room)

    print("\nRoom cards found:", len(room_cards))
    print("\nExtracted rooms:")
    for room in rooms:
        print(room)

    # VALIDATE FIRST, THEN DETECT DUPLICATES AMONG VALID RECORDS
    valid_rooms = []
    invalid_rooms = []
    duplicate_rooms = []
    seen_room_ids = set()

    for room in rooms:
        problems = []

        if room["room_id"] == "":
            problems.append("missing room ID")

        if room["name"] == "":
            problems.append("missing name")

        if room["floor"] == "":
            problems.append("missing floor")

        if room["status"] not in ["available", "unavailable"]:
            problems.append("invalid status")

        if room["capacity"] is None:
            problems.append("missing capacity")
        elif room["capacity"] <= 0:
            problems.append("capacity must be greater than zero")

        if room["hourly_rate"] is None:
            problems.append("missing hourly rate")
        elif room["hourly_rate"] < 0:
            problems.append("hourly rate cannot be negative")

        if problems:
            invalid_rooms.append({
                "room": room,
                "problems": problems,
            })
        elif room["room_id"] in seen_room_ids:
            duplicate_rooms.append(room)
        else:
            seen_room_ids.add(room["room_id"])
            valid_rooms.append(room)

    print("\nValidation and duplicate results:")
    print("Valid unique rooms:", len(valid_rooms))
    print("Invalid rooms:", len(invalid_rooms))
    print("Duplicate rooms:", len(duplicate_rooms))

    print("\nInvalid-room details:")
    for invalid_record in invalid_rooms:
        print("Room ID:", invalid_record["room"]["room_id"])
        print("Problems:", ", ".join(invalid_record["problems"]))

    print("\nDuplicate-room details:")
    for duplicate_room in duplicate_rooms:
        print("Room ID:", duplicate_room["room_id"])
        print("Name:", duplicate_room["name"])

    # ANALYSE VALID UNIQUE ROOMS
    available_rooms = [
        room
        for room in valid_rooms
        if room["status"] == "available"
    ]

    total_available_capacity = sum(
        room["capacity"]
        for room in available_rooms
    )
    total_available_rate = sum(
        room["hourly_rate"]
        for room in available_rooms
    )

    if available_rooms:
        average_available_rate = (
            total_available_rate / len(available_rooms)
        )
        cheapest_available_room = min(
            available_rooms,
            key=lambda room: room["hourly_rate"],
        )
    else:
        average_available_rate = 0.0
        cheapest_available_room = None

    largest_room = (
        max(valid_rooms, key=lambda room: room["capacity"])
        if valid_rooms
        else None
    )

    print("\nAnalysis results:")
    print("Available rooms:", len(available_rooms))
    print("Total available capacity:", total_available_capacity)
    print(f"Average available hourly rate: ${average_available_rate:.2f}")

    if cheapest_available_room:
        print(
            "Cheapest available room:",
            cheapest_available_room["name"],
            f"(${cheapest_available_room['hourly_rate']:.2f})",
        )
    else:
        print("Cheapest available room: None")

    if largest_room:
        print(
            "Largest valid room:",
            largest_room["name"],
            f"({largest_room['capacity']} people)",
        )
    else:
        print("Largest valid room: None")

    # STORE RESULTS
    output_directory = BASE_OUTPUT_DIRECTORY / "practical_assessment"
    output_directory.mkdir(parents=True, exist_ok=True)

    csv_path = output_directory / "valid_unique_rooms.csv"
    json_path = output_directory / "room_audit.json"
    database_path = output_directory / "study_rooms.db"

    fieldnames = [
        "room_id",
        "name",
        "floor",
        "status",
        "capacity",
        "hourly_rate",
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(valid_rooms)

    audit_data = {
        "valid_rooms": valid_rooms,
        "invalid_rooms": invalid_rooms,
        "duplicate_rooms": duplicate_rooms,
    }

    with json_path.open("w", encoding="utf-8") as json_file:
        json.dump(audit_data, json_file, indent=4, ensure_ascii=False)

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS study_rooms (
            room_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            floor TEXT NOT NULL,
            status TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            hourly_rate REAL NOT NULL
        )
        """
    )

    cursor.execute("DELETE FROM study_rooms")

    for room in valid_rooms:
        cursor.execute(
            """
            INSERT INTO study_rooms (
                room_id,
                name,
                floor,
                status,
                capacity,
                hourly_rate
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                room["room_id"],
                room["name"],
                room["floor"],
                room["status"],
                room["capacity"],
                room["hourly_rate"],
            ),
        )

    connection.commit()

    # VERIFY EVERY STORAGE FORMAT
    stored_csv_rooms = read_csv_records(csv_path)
    stored_audit = read_json_data(json_path)

    cursor.execute("SELECT COUNT(*) FROM study_rooms")
    stored_database_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT name, capacity
        FROM study_rooms
        ORDER BY capacity DESC
        LIMIT 1
        """
    )
    database_largest_room = cursor.fetchone()
    connection.close()

    print("\nStorage verification:")
    print("CSV valid rooms:", len(stored_csv_rooms))
    print("JSON valid rooms:", len(stored_audit["valid_rooms"]))
    print("JSON invalid rooms:", len(stored_audit["invalid_rooms"]))
    print("JSON duplicate rooms:", len(stored_audit["duplicate_rooms"]))
    print("SQLite valid rooms:", stored_database_count)

    if database_largest_room:
        print(
            "SQLite largest room:",
            database_largest_room[0],
            f"({database_largest_room[1]} people)",
        )

    print("\nCreated practical-assessment files:")
    print("-", csv_path)
    print("-", json_path)
    print("-", database_path)


def main():
    """Run both complete Day 48 demonstrations."""
    BASE_OUTPUT_DIRECTORY.mkdir(exist_ok=True)
    run_guided_revision()
    run_practical_assessment()

    print("\n" + "=" * 72)
    print("DAY 48 COMPLETE")
    print("=" * 72)
    print("Both pipelines extracted, cleaned, validated, analysed, stored,")
    print("and verified their data successfully.")


if __name__ == "__main__":
    main()
