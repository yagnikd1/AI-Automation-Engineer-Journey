"""
Day 63 — Partial-Failure Recovery

Complete study program demonstrating:
1. failed-record audit logs;
2. checkpoints;
3. resumable collection;
4. deduplication after restarting;
5. safe JSON file writes; and
6. final success-and-failure summaries.

Quick use
---------
Normal complete run:
    python Day_63_Partial_Failure_Recovery.py

Simulated interruption and recovery (PowerShell):
    $env:DAY63_SIMULATE_INTERRUPTION="true"
    python Day_63_Partial_Failure_Recovery.py
    $env:DAY63_SIMULATE_INTERRUPTION="false"
    python Day_63_Partial_Failure_Recovery.py

To repeat the demonstration, delete only the generated ``day_63_output``
directory and run the two commands again.
"""

import json
import os
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup


SOURCE_NAME = "International Environmental Report Archive"

REQUIRED_FIELDS = (
    "report_id",
    "title",
    "country",
    "publication_year",
)

OUTPUT_DIRECTORY = Path("day_63_output")
CHECKPOINT_FILE = OUTPUT_DIRECTORY / "collection_checkpoint.json"
FAILED_AUDIT_FILE = OUTPUT_DIRECTORY / "failed_records_audit.json"
VALID_REPORTS_FILE = OUTPUT_DIRECTORY / "valid_reports.json"

# Set DAY63_SIMULATE_INTERRUPTION=true for the first demonstration run.
SIMULATE_INTERRUPTION = (
    os.getenv("DAY63_SIMULATE_INTERRUPTION", "false").lower() == "true"
)

HTML_PAGES = [
    """
    <section class="report-page" data-page="1">
        <article class="report-card">
            <span class="report-id">ER-101</span>
            <h2 class="title">Coastal Ecosystem Review</h2>
            <p class="country">Portugal</p>
            <span class="year">2024</span>
        </article>

        <article class="report-card">
            <span class="report-id">ER-102</span>
            <h2 class="title">Forest Restoration Assessment</h2>
            <p class="country">Canada</p>
            <span class="year">2023</span>
        </article>
    </section>
    """,
    """
    <section class="report-page" data-page="2">
        <article class="report-card">
            <span class="report-id">ER-102</span>
            <h2 class="title">Forest Restoration Assessment</h2>
            <p class="country">Canada</p>
            <span class="year">2023</span>
        </article>

        <article class="report-card">
            <span class="report-id">ER-103</span>
            <h2 class="title"></h2>
            <p class="country">Norway</p>
            <span class="year">2022</span>
        </article>

        <article class="report-card">
            <span class="report-id">ER-104</span>
            <h2 class="title">Urban Air Quality Study</h2>
            <p class="country">Germany</p>
            <span class="year">unknown</span>
        </article>
    </section>
    """,
]


def get_text_or_none(card: Any, selector: str) -> str | None:
    """Return cleaned element text, or None when absent or empty."""
    element = card.select_one(selector)

    if element is None:
        return None

    text = element.get_text(strip=True)
    return text if text else None


def clean_year(raw_year: str | None) -> int | None:
    """Convert a year string to int without crashing on invalid input."""
    if raw_year is None:
        return None

    try:
        return int(raw_year)
    except ValueError:
        return None


def parse_report(card: Any) -> dict[str, Any]:
    """Turn one HTML report card into a consistent Python dictionary."""
    return {
        "report_id": get_text_or_none(card, ".report-id"),
        "title": get_text_or_none(card, ".title"),
        "country": get_text_or_none(card, ".country"),
        "publication_year": clean_year(get_text_or_none(card, ".year")),
    }


def validate_report(report: dict[str, Any]) -> tuple[bool, str | None]:
    """Return validation status and an exact rejection reason."""
    missing_fields = []

    for field in REQUIRED_FIELDS:
        if report.get(field) is None:
            missing_fields.append(field)

    if missing_fields:
        reason = f"Missing or invalid: {', '.join(missing_fields)}"
        return False, reason

    return True, None


def safe_write_json(file_path: Path, data: Any) -> None:
    """Write JSON atomically so a partial write cannot corrupt the real file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_file = file_path.with_suffix(file_path.suffix + ".tmp")

    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    # Replacement happens only after the temporary JSON is written completely.
    temporary_file.replace(file_path)


def empty_checkpoint() -> dict[str, Any]:
    """Return the initial state used when no checkpoint exists."""
    return {
        "last_completed_page": 0,
        "valid_reports": [],
        "failed_reports": [],
        "seen_report_ids": [],
    }


def load_checkpoint() -> dict[str, Any]:
    """Recover progress from disk, or start with an empty state."""
    if not CHECKPOINT_FILE.exists():
        return empty_checkpoint()

    with CHECKPOINT_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_checkpoint(
    last_completed_page: int,
    valid_reports: list[dict[str, Any]],
    failed_reports: list[dict[str, Any]],
    seen_report_ids: set[str],
) -> None:
    """Persist every piece of state needed for an accurate restart."""
    checkpoint_data = {
        "last_completed_page": last_completed_page,
        "valid_reports": valid_reports,
        "failed_reports": failed_reports,
        "seen_report_ids": sorted(seen_report_ids),
    }

    safe_write_json(CHECKPOINT_FILE, checkpoint_data)
    safe_write_json(FAILED_AUDIT_FILE, failed_reports)
    print(f"Checkpoint saved after page {last_completed_page}.")


def collect_reports() -> None:
    """Collect, validate, checkpoint, recover, deduplicate, and export reports."""
    checkpoint = load_checkpoint()

    last_completed_page = checkpoint["last_completed_page"]
    valid_reports = checkpoint["valid_reports"]
    failed_reports = checkpoint["failed_reports"]
    seen_report_ids = set(checkpoint["seen_report_ids"])

    print(f"Starting {SOURCE_NAME} Collector...")
    print(f"Last completed page: {last_completed_page}")
    print(f"Recovered valid reports: {len(valid_reports)}")
    print(f"Recovered failed reports: {len(failed_reports)}")

    try:
        for page_number, html in enumerate(HTML_PAGES, start=1):
            if page_number <= last_completed_page:
                print(f"\nPreviously completed page skipped: {page_number}")
                continue

            soup = BeautifulSoup(html, "html.parser")
            cards = soup.select(".report-card")

            print(f"\nProcessing page {page_number}...")
            print(f"Report cards found: {len(cards)}")

            for position, card in enumerate(cards, start=1):
                report = parse_report(card)
                report_id = report.get("report_id")

                if report_id in seen_report_ids:
                    print(f"Duplicate skipped: {report_id}")
                    continue

                is_valid, failure_reason = validate_report(report)

                if not is_valid:
                    failed_reports.append(
                        {
                            "page": page_number,
                            "position": position,
                            "report_id": report_id,
                            "reason": failure_reason,
                            "raw_record": report,
                        }
                    )
                    print(
                        f"Rejected page {page_number}, record {position}: "
                        f"{failure_reason}"
                    )
                    continue

                # The ID is added only after the record passes validation.
                seen_report_ids.add(report_id)
                valid_reports.append(report)
                print(f"Accepted: {report_id} | {report['title']}")

            # A page becomes completed only after every card has been handled.
            last_completed_page = page_number
            save_checkpoint(
                last_completed_page,
                valid_reports,
                failed_reports,
                seen_report_ids,
            )

            if SIMULATE_INTERRUPTION and page_number == 1:
                raise RuntimeError("Simulated interruption after page 1")

    except RuntimeError as error:
        print(f"\nCOLLECTION INTERRUPTED: {error}")
        print("Saved progress is available for the next run.")

    else:
        safe_write_json(VALID_REPORTS_FILE, valid_reports)
        safe_write_json(FAILED_AUDIT_FILE, failed_reports)

        print("\n===== FINAL RECOVERY SUMMARY =====")
        print(f"Pages completed: {last_completed_page}")
        print(f"Valid reports: {len(valid_reports)}")
        print(f"Failed reports: {len(failed_reports)}")
        print(f"Unique accepted IDs: {len(seen_report_ids)}")
        print(f"Valid-record file: {VALID_REPORTS_FILE}")
        print(f"Failed-record audit: {FAILED_AUDIT_FILE}")
        print("Collection status: COMPLETED")


if __name__ == "__main__":
    collect_reports()
