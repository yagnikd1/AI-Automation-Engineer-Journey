"""
Day 49 - Public Facility Inspection Data Auditor
================================================

Topics covered
--------------
1. Ethical collection from an official public JSON API.
2. Reusable requests.Session configuration.
3. Pagination, limits, delays, timeouts, and safe stop statuses.
4. HTTP and JSON response validation.
5. Record cleaning, required-field validation, type conversion, and deduplication.
6. Analysis with totals, averages, counters, filtering, and max().
7. CSV, JSON, and SQLite storage.
8. Plain-text and escaped HTML report generation.
9. README documentation generation.
10. Automated cross-format verification.
11. A main() workflow and explicit failure reporting.

Install third-party dependencies:
    pip install requests beautifulsoup4

Run:
    python Day_49_Public_Facility_Inspection_Data_Auditor_Complete_Study_Guide.py

Important:
    This program collects a maximum of 30 records for training. Review the
    source's current terms and policies before every real collection run.
"""

from __future__ import annotations

import csv
import html
import json
import sqlite3
import time
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup


# ---------------------------------------------------------------------------
# SECTION 1: Configuration and responsible collection boundaries
# ---------------------------------------------------------------------------

API_URL = "https://data.cityofchicago.org/resource/4ijn-s7e5.json"
SOURCE_PAGE_URL = (
    "https://data.cityofchicago.org/Health-Human-Services/"
    "Food-Inspections/4ijn-s7e5"
)
TERMS_URL = "https://www.chicago.gov/city/en/general/terms.html"

OUTPUT_DIRECTORY = Path("day49_facility_audit_output")
SOURCE_PERMISSION_CHECK_DATE = date.today().isoformat()

MAX_PAGES = 3
PAGE_SIZE = 10
REQUEST_DELAY = 1.0
REQUEST_TIMEOUT = 20
STOP_STATUSES = {403, 404, 503}

USER_AGENT = (
    "TrainingResearchBot/1.0 "
    "(limited educational API audit; contact: local-training)"
)

CSV_FIELDS = [
    "inspection_id",
    "business_name",
    "facility_type",
    "risk",
    "address",
    "inspection_date",
    "inspection_type",
    "result",
    "violation_count",
]


# ---------------------------------------------------------------------------
# SECTION 2: Output directory and HTTP session
# ---------------------------------------------------------------------------

def prepare_output_directory() -> Path:
    """Create the output directory if it does not already exist."""
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIRECTORY


def create_session() -> requests.Session:
    """Create one reusable HTTP session with clear request headers."""
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        }
    )
    return session


# ---------------------------------------------------------------------------
# SECTION 3: Paginated API collection and response validation
# ---------------------------------------------------------------------------

def validate_api_response(response: requests.Response) -> list[dict[str, Any]]:
    """Validate status, content type, JSON structure, and record types."""
    if response.status_code in STOP_STATUSES:
        raise RuntimeError(
            f"Collection stopped safely: HTTP {response.status_code}."
        )

    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "").lower()
    if "json" not in content_type:
        raise ValueError(
            f"Expected JSON but received Content-Type: {content_type or 'missing'}"
        )

    try:
        payload = response.json()
    except requests.exceptions.JSONDecodeError as error:
        raise ValueError("The API response was not valid JSON.") from error

    if not isinstance(payload, list):
        raise TypeError("Expected the API payload to be a list of records.")

    if not all(isinstance(record, dict) for record in payload):
        raise TypeError("Every API record must be a dictionary/object.")

    return payload


def collect_inspection_records(
    session: requests.Session,
) -> list[dict[str, Any]]:
    """Collect a small, ordered sample using limit-and-offset pagination."""
    collected_records: list[dict[str, Any]] = []

    for page_number in range(MAX_PAGES):
        offset = page_number * PAGE_SIZE

        print(
            f"Requesting page {page_number + 1}/{MAX_PAGES} "
            f"with offset {offset}..."
        )

        response = session.get(
            API_URL,
            params={
                "$limit": PAGE_SIZE,
                "$offset": offset,
                "$order": "inspection_id ASC",
            },
            timeout=REQUEST_TIMEOUT,
        )

        page_records = validate_api_response(response)
        collected_records.extend(page_records)

        print(
            f"Page records: {len(page_records)} | "
            f"Total collected: {len(collected_records)}"
        )

        if len(page_records) < PAGE_SIZE:
            break

        if page_number < MAX_PAGES - 1:
            time.sleep(REQUEST_DELAY)

    return collected_records


# ---------------------------------------------------------------------------
# SECTION 4: Cleaning, validation, conversion, and deduplication
# ---------------------------------------------------------------------------

def clean_text(value: Any, default: str = "Not available") -> str:
    """Normalize whitespace and return a safe default for empty values."""
    if value is None:
        return default

    cleaned_value = " ".join(str(value).split())
    return cleaned_value if cleaned_value else default


def count_violations(value: Any) -> int:
    """Count separate violations in the source's pipe-delimited text."""
    if not value:
        return 0

    return len(
        [
            violation
            for violation in str(value).split("|")
            if violation.strip()
        ]
    )


def clean_inspection_records(
    raw_records: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Clean records, reject missing required values, and remove duplicates."""
    cleaned_records: list[dict[str, Any]] = []
    seen_inspection_ids: set[str] = set()
    rejected_records = 0
    duplicate_records = 0

    for raw_record in raw_records:
        inspection_id = clean_text(raw_record.get("inspection_id"), "")
        business_name = clean_text(raw_record.get("dba_name"), "")
        inspection_date = clean_text(raw_record.get("inspection_date"), "")
        result = clean_text(raw_record.get("results"), "")

        if not all(
            [inspection_id, business_name, inspection_date, result]
        ):
            rejected_records += 1
            continue

        if inspection_id in seen_inspection_ids:
            duplicate_records += 1
            continue

        seen_inspection_ids.add(inspection_id)

        cleaned_records.append(
            {
                "inspection_id": inspection_id,
                "business_name": business_name,
                "facility_type": clean_text(
                    raw_record.get("facility_type")
                ),
                "risk": clean_text(raw_record.get("risk")),
                "address": clean_text(raw_record.get("address")),
                "inspection_date": inspection_date[:10],
                "inspection_type": clean_text(
                    raw_record.get("inspection_type")
                ),
                "result": result,
                "violation_count": count_violations(
                    raw_record.get("violations")
                ),
            }
        )

    cleaning_summary = {
        "raw_records": len(raw_records),
        "cleaned_records": len(cleaned_records),
        "rejected_records": rejected_records,
        "duplicate_records": duplicate_records,
    }

    return cleaned_records, cleaning_summary


# ---------------------------------------------------------------------------
# SECTION 5: Analysis
# ---------------------------------------------------------------------------

def analyze_inspection_records(
    records: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Calculate statistics and return the failed-inspection subset."""
    result_counts = Counter(record["result"] for record in records)
    risk_counts = Counter(record["risk"] for record in records)
    facility_type_counts = Counter(
        record["facility_type"] for record in records
    )

    total_violations = sum(
        record["violation_count"] for record in records
    )

    failed_inspections = [
        record
        for record in records
        if record["result"].casefold() == "fail"
    ]

    highest_violation_record = (
        max(records, key=lambda record: record["violation_count"])
        if records
        else None
    )

    analysis = {
        "total_inspections": len(records),
        "total_violations": total_violations,
        "average_violations": (
            total_violations / len(records) if records else 0.0
        ),
        "failed_inspections": len(failed_inspections),
        "most_common_facility_type": (
            facility_type_counts.most_common(1)[0][0]
            if facility_type_counts
            else None
        ),
        "highest_violation_record": highest_violation_record,
        "result_counts": dict(result_counts),
        "risk_counts": dict(risk_counts),
    }

    return analysis, failed_inspections


# ---------------------------------------------------------------------------
# SECTION 6: CSV, JSON, and SQLite persistence
# ---------------------------------------------------------------------------

def save_records_to_csv(records: list[dict[str, Any]]) -> Path:
    """Save cleaned records to CSV."""
    csv_path = OUTPUT_DIRECTORY / "inspection_records.csv"

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(records)

    return csv_path


def save_records_to_json(
    records: list[dict[str, Any]],
    cleaning_summary: dict[str, int],
    analysis: dict[str, Any],
) -> Path:
    """Save source evidence, summaries, analysis, and records to JSON."""
    json_path = OUTPUT_DIRECTORY / "inspection_audit.json"

    content = {
        "source": {
            "api_url": API_URL,
            "dataset_page": SOURCE_PAGE_URL,
            "terms_url": TERMS_URL,
            "permission_check_date": SOURCE_PERMISSION_CHECK_DATE,
            "collection_limit": MAX_PAGES * PAGE_SIZE,
        },
        "cleaning_summary": cleaning_summary,
        "analysis": analysis,
        "records": records,
    }

    json_path.write_text(
        json.dumps(content, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )

    return json_path


def save_records_to_sqlite(records: list[dict[str, Any]]) -> Path:
    """Create the table, clear older rows, and insert current records."""
    database_path = OUTPUT_DIRECTORY / "inspection_audit.db"

    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()

        # Correct order: create -> delete -> insert -> commit.
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS inspections (
                inspection_id TEXT PRIMARY KEY,
                business_name TEXT NOT NULL,
                facility_type TEXT NOT NULL,
                risk TEXT NOT NULL,
                address TEXT NOT NULL,
                inspection_date TEXT NOT NULL,
                inspection_type TEXT NOT NULL,
                result TEXT NOT NULL,
                violation_count INTEGER NOT NULL
            )
            """
        )

        cursor.execute("DELETE FROM inspections")

        cursor.executemany(
            """
            INSERT OR REPLACE INTO inspections (
                inspection_id,
                business_name,
                facility_type,
                risk,
                address,
                inspection_date,
                inspection_type,
                result,
                violation_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                tuple(record[field] for field in CSV_FIELDS)
                for record in records
            ],
        )

        connection.commit()

    return database_path


# ---------------------------------------------------------------------------
# SECTION 7: Text and HTML reporting
# ---------------------------------------------------------------------------

def generate_text_report(
    cleaning_summary: dict[str, int],
    analysis: dict[str, Any],
) -> Path:
    """Generate a readable plain-text inspection report."""
    report_path = OUTPUT_DIRECTORY / "inspection_audit_report.txt"
    highest_record = analysis["highest_violation_record"]

    highest_summary = (
        f'{highest_record["business_name"]} '
        f'({highest_record["violation_count"]} violations)'
        if highest_record
        else "Not available"
    )

    report_lines = [
        "PUBLIC FACILITY INSPECTION DATA AUDIT",
        "=" * 44,
        "",
        "SOURCE INFORMATION",
        f"API endpoint: {API_URL}",
        f"Dataset page: {SOURCE_PAGE_URL}",
        f"Terms reviewed: {TERMS_URL}",
        f"Permission check date: {SOURCE_PERMISSION_CHECK_DATE}",
        "",
        "CLEANING SUMMARY",
        f'Raw records: {cleaning_summary["raw_records"]}',
        f'Accepted records: {cleaning_summary["cleaned_records"]}',
        f'Rejected records: {cleaning_summary["rejected_records"]}',
        f'Duplicate records: {cleaning_summary["duplicate_records"]}',
        "",
        "ANALYSIS SUMMARY",
        f'Total inspections: {analysis["total_inspections"]}',
        f'Total violations: {analysis["total_violations"]}',
        f'Average violations: {analysis["average_violations"]:.2f}',
        f'Failed inspections: {analysis["failed_inspections"]}',
        (
            "Most common facility type: "
            f'{analysis["most_common_facility_type"] or "Not available"}'
        ),
        f"Highest violation record: {highest_summary}",
        "",
        "RESULT DISTRIBUTION",
    ]

    for result, count in sorted(analysis["result_counts"].items()):
        report_lines.append(f"- {result}: {count}")

    report_lines.extend(["", "RISK DISTRIBUTION"])

    for risk, count in sorted(analysis["risk_counts"].items()):
        report_lines.append(f"- {risk}: {count}")

    report_lines.extend(
        [
            "",
            "VERIFICATION NOTE",
            (
                "This report summarizes a limited training sample and must "
                "not be treated as a complete assessment of the full dataset."
            ),
        ]
    )

    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    return report_path


def generate_html_report(
    records: list[dict[str, Any]],
    cleaning_summary: dict[str, int],
    analysis: dict[str, Any],
) -> Path:
    """Generate a browser-readable report with HTML-escaped record values."""
    report_path = OUTPUT_DIRECTORY / "inspection_audit_report.html"

    result_items = "".join(
        f"<li>{html.escape(result)}: {count}</li>"
        for result, count in sorted(analysis["result_counts"].items())
    )

    table_rows = "\n".join(
        (
            "<tr>"
            f'<td>{html.escape(record["inspection_id"])}</td>'
            f'<td>{html.escape(record["business_name"])}</td>'
            f'<td>{html.escape(record["facility_type"])}</td>'
            f'<td>{html.escape(record["inspection_date"])}</td>'
            f'<td>{html.escape(record["result"])}</td>'
            f'<td>{record["violation_count"]}</td>'
            "</tr>"
        )
        for record in records
    )

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Public Facility Inspection Data Audit</title>
    <style>
        body {{ max-width: 1100px; margin: 40px auto; padding: 0 20px;
                color: #243447; background: #f4f7fa; font-family: Arial, sans-serif; }}
        h1, h2 {{ color: #17324d; }}
        .summary-grid {{ display: grid;
                         grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                         gap: 16px; }}
        .summary-card {{ padding: 16px; background: white;
                         border-left: 5px solid #2673b8; border-radius: 6px; }}
        table {{ width: 100%; margin-top: 20px; background: white;
                 border-collapse: collapse; }}
        th, td {{ padding: 10px; border: 1px solid #ccd6df; text-align: left; }}
        th {{ color: white; background: #2673b8; }}
        .note {{ margin-top: 24px; padding: 15px; background: #fff3cd;
                 border-left: 5px solid #d39e00; }}
    </style>
</head>
<body>
    <h1>Public Facility Inspection Data Audit</h1>
    <p>Source permission reviewed on
       {html.escape(SOURCE_PERMISSION_CHECK_DATE)}.</p>
    <h2>Audit Summary</h2>
    <div class="summary-grid">
        <div class="summary-card"><strong>Raw records</strong>
            <p>{cleaning_summary["raw_records"]}</p></div>
        <div class="summary-card"><strong>Accepted records</strong>
            <p>{cleaning_summary["cleaned_records"]}</p></div>
        <div class="summary-card"><strong>Failed inspections</strong>
            <p>{analysis["failed_inspections"]}</p></div>
        <div class="summary-card"><strong>Average violations</strong>
            <p>{analysis["average_violations"]:.2f}</p></div>
    </div>
    <h2>Result Distribution</h2>
    <ul>{result_items}</ul>
    <h2>Inspection Records</h2>
    <table id="inspection-table">
        <thead><tr><th>Inspection ID</th><th>Business</th>
        <th>Facility Type</th><th>Date</th><th>Result</th>
        <th>Violations</th></tr></thead>
        <tbody>{table_rows}</tbody>
    </table>
    <div class="note">This report contains a limited training sample.
    It does not represent every record available in the source dataset.</div>
</body>
</html>
"""

    report_path.write_text(html_content, encoding="utf-8")
    return report_path


# ---------------------------------------------------------------------------
# SECTION 8: Project documentation
# ---------------------------------------------------------------------------

def generate_project_documentation() -> Path:
    """Create a README without unsafe nested Python triple-quote copying."""
    documentation_path = OUTPUT_DIRECTORY / "README.md"

    documentation_lines = [
        "# Public Facility Inspection Data Auditor",
        "",
        "## Project purpose",
        "",
        (
            "This Day 49 project collects a limited public API sample, cleans "
            "and validates it, analyzes accepted records, saves multiple "
            "formats, generates reports, and verifies the outputs."
        ),
        "",
        "## Data source",
        "",
        f"- API endpoint: {API_URL}",
        f"- Dataset page: {SOURCE_PAGE_URL}",
        f"- Terms reviewed: {TERMS_URL}",
        f"- Permission check date: {SOURCE_PERMISSION_CHECK_DATE}",
        "",
        "## Ethical collection limits",
        "",
        f"- Maximum pages: {MAX_PAGES}",
        f"- Records per page: {PAGE_SIZE}",
        f"- Maximum possible records: {MAX_PAGES * PAGE_SIZE}",
        f"- Delay between requests: {REQUEST_DELAY} seconds",
        f"- Request timeout: {REQUEST_TIMEOUT} seconds",
        "- Stop statuses: 403, 404, and 503",
        "",
        "## Processing workflow",
        "",
        "1. Create a reusable HTTP session.",
        "2. Request a maximum of three API pages.",
        "3. Validate HTTP status and response format.",
        "4. Clean required and optional fields.",
        "5. Reject incomplete records and remove duplicates.",
        "6. Calculate inspection statistics.",
        "7. Save CSV, JSON, and SQLite outputs.",
        "8. Generate text and HTML reports.",
        "9. Run automated verification checks.",
        "",
        "## Generated files",
        "",
        "- `inspection_records.csv`",
        "- `inspection_audit.json`",
        "- `inspection_audit.db`",
        "- `inspection_audit_report.txt`",
        "- `inspection_audit_report.html`",
        "- `verification_report.txt`",
        "",
        "## Important limitation",
        "",
        (
            "The program processes only a small training sample and is not a "
            "complete assessment of the full dataset."
        ),
        "",
        "## Requirements",
        "",
        "```text",
        "requests",
        "beautifulsoup4",
        "```",
        "",
        "## Run command",
        "",
        "```bash",
        (
            "python "
            "Day_49_Public_Facility_Inspection_Data_Auditor_Complete_Study_Guide.py"
        ),
        "```",
    ]

    documentation_path.write_text(
        "\n".join(documentation_lines),
        encoding="utf-8",
    )
    return documentation_path


# ---------------------------------------------------------------------------
# SECTION 9: Automated verification (21 checks)
# ---------------------------------------------------------------------------

def verify_project_outputs(
    records: list[dict[str, Any]],
    cleaning_summary: dict[str, int],
    analysis: dict[str, Any],
    output_paths: dict[str, Path],
) -> tuple[Path, dict[str, bool], bool]:
    """Verify generated files and write a verification report."""
    checks: dict[str, bool] = {}
    expected_count = len(records)
    expected_violation_total = sum(
        record["violation_count"] for record in records
    )
    required_fields = set(CSV_FIELDS)

    checks["All expected output files exist"] = all(
        path.exists() for path in output_paths.values()
    )
    checks["All output files contain data"] = all(
        path.stat().st_size > 0 for path in output_paths.values()
    )
    checks["Cleaning totals are consistent"] = (
        cleaning_summary["raw_records"]
        == cleaning_summary["cleaned_records"]
        + cleaning_summary["rejected_records"]
        + cleaning_summary["duplicate_records"]
    )
    checks["Analysis record count is correct"] = (
        analysis["total_inspections"] == expected_count
    )
    checks["Analysis violation total is correct"] = (
        analysis["total_violations"] == expected_violation_total
    )
    checks["Inspection IDs are unique"] = (
        len({record["inspection_id"] for record in records})
        == expected_count
    )

    with output_paths["csv"].open(
        "r", newline="", encoding="utf-8"
    ) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        csv_rows = list(csv_reader)
        csv_fields = set(csv_reader.fieldnames or [])

    checks["CSV contains the required columns"] = (
        required_fields == csv_fields
    )
    checks["CSV row count matches cleaned records"] = (
        len(csv_rows) == expected_count
    )

    with output_paths["json"].open("r", encoding="utf-8") as json_file:
        json_content = json.load(json_file)

    checks["JSON record count matches cleaned records"] = (
        len(json_content.get("records", [])) == expected_count
    )
    checks["JSON analysis count is correct"] = (
        json_content.get("analysis", {}).get("total_inspections")
        == expected_count
    )
    checks["JSON contains source evidence"] = (
        json_content.get("source", {}).get("api_url") == API_URL
        and json_content.get("source", {}).get("terms_url") == TERMS_URL
        and json_content.get("source", {}).get("permission_check_date")
        == SOURCE_PERMISSION_CHECK_DATE
    )

    with sqlite3.connect(output_paths["database"]) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
                COUNT(*),
                COUNT(DISTINCT inspection_id),
                COALESCE(SUM(violation_count), 0)
            FROM inspections
            """
        )
        database_count, unique_id_count, database_violation_total = (
            cursor.fetchone()
        )

    checks["SQLite row count matches cleaned records"] = (
        database_count == expected_count
    )
    checks["SQLite inspection IDs are unique"] = (
        unique_id_count == expected_count
    )
    checks["SQLite violation total is correct"] = (
        database_violation_total == expected_violation_total
    )

    text_report = output_paths["text_report"].read_text(encoding="utf-8")
    checks["Text report contains required sections"] = all(
        heading in text_report
        for heading in [
            "SOURCE INFORMATION",
            "CLEANING SUMMARY",
            "ANALYSIS SUMMARY",
            "RESULT DISTRIBUTION",
            "RISK DISTRIBUTION",
            "VERIFICATION NOTE",
        ]
    )
    checks["Text report states the sample limitation"] = (
        "limited training sample" in text_report
    )

    html_report = output_paths["html_report"].read_text(encoding="utf-8")
    soup = BeautifulSoup(html_report, "html.parser")
    checks["HTML report contains the inspection table"] = (
        soup.select_one("#inspection-table") is not None
    )
    checks["HTML table row count matches cleaned records"] = (
        len(soup.select("#inspection-table tbody tr")) == expected_count
    )
    checks["HTML report has the correct title"] = (
        soup.title is not None
        and soup.title.get_text(strip=True)
        == "Public Facility Inspection Data Audit"
    )

    documentation = output_paths["documentation"].read_text(
        encoding="utf-8"
    )
    checks["Documentation contains required sections"] = all(
        heading in documentation
        for heading in [
            "## Project purpose",
            "## Data source",
            "## Ethical collection limits",
            "## Processing workflow",
            "## Generated files",
            "## Important limitation",
            "## Requirements",
            "## Run command",
        ]
    )
    checks["Documentation includes the API endpoint"] = (
        API_URL in documentation
    )

    passed_checks = sum(checks.values())
    total_checks = len(checks)
    failed_checks = total_checks - passed_checks
    verification_passed = failed_checks == 0

    verification_lines = [
        "PUBLIC FACILITY INSPECTION PROJECT VERIFICATION",
        "=" * 48,
        "",
        f"Expected cleaned records: {expected_count}",
        f"Total checks: {total_checks}",
        f"Passed checks: {passed_checks}",
        f"Failed checks: {failed_checks}",
        f'Overall result: {"PASS" if verification_passed else "FAIL"}',
        "",
        "CHECK RESULTS",
    ]

    for check_name, check_passed in checks.items():
        status = "PASS" if check_passed else "FAIL"
        verification_lines.append(f"[{status}] {check_name}")

    verification_path = OUTPUT_DIRECTORY / "verification_report.txt"
    verification_path.write_text(
        "\n".join(verification_lines),
        encoding="utf-8",
    )

    return verification_path, checks, verification_passed


# ---------------------------------------------------------------------------
# SECTION 10: Complete workflow
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the complete public facility inspection data audit."""
    print("Starting Public Facility Inspection Data Audit...")
    print(f"Source: {API_URL}")
    print(
        f"Maximum collection limit: {MAX_PAGES * PAGE_SIZE} records"
    )

    prepare_output_directory()
    session = create_session()

    try:
        raw_records = collect_inspection_records(session)
    finally:
        session.close()

    cleaned_records, cleaning_summary = clean_inspection_records(
        raw_records
    )
    analysis, failed_inspections = analyze_inspection_records(
        cleaned_records
    )

    output_paths = {
        "csv": save_records_to_csv(cleaned_records),
        "json": save_records_to_json(
            cleaned_records, cleaning_summary, analysis
        ),
        "database": save_records_to_sqlite(cleaned_records),
        "text_report": generate_text_report(cleaning_summary, analysis),
        "html_report": generate_html_report(
            cleaned_records, cleaning_summary, analysis
        ),
        "documentation": generate_project_documentation(),
    }

    verification_path, checks, verification_passed = (
        verify_project_outputs(
            cleaned_records,
            cleaning_summary,
            analysis,
            output_paths,
        )
    )

    print("\nCOLLECTION AND CLEANING RESULTS")
    print("-" * 40)
    print(f'Raw records: {cleaning_summary["raw_records"]}')
    print(f'Accepted records: {cleaning_summary["cleaned_records"]}')
    print(f'Rejected records: {cleaning_summary["rejected_records"]}')
    print(f'Duplicate records: {cleaning_summary["duplicate_records"]}')

    print("\nANALYSIS RESULTS")
    print("-" * 40)
    print(f'Total inspections: {analysis["total_inspections"]}')
    print(f'Total violations: {analysis["total_violations"]}')
    print(f'Average violations: {analysis["average_violations"]:.2f}')
    print(f"Failed inspections: {len(failed_inspections)}")
    print(
        "Most common facility type: "
        f'{analysis["most_common_facility_type"] or "Not available"}'
    )

    highest_record = analysis["highest_violation_record"]
    if highest_record:
        print(
            "Highest violation record: "
            f'{highest_record["business_name"]} '
            f'({highest_record["violation_count"]} violations)'
        )
    else:
        print("Highest violation record: Not available")

    print("\nGENERATED OUTPUTS")
    print("-" * 40)
    for output_name, output_path in output_paths.items():
        print(f"{output_name}: {output_path}")
    print(f"verification: {verification_path}")

    passed_checks = sum(checks.values())
    total_checks = len(checks)
    print("\nAUTOMATED VERIFICATION")
    print("-" * 40)
    print(f"Passed checks: {passed_checks}/{total_checks}")
    print(f'Overall result: {"PASS" if verification_passed else "FAIL"}')

    if not verification_passed:
        print("\nFAILED CHECKS")
        for check_name, check_passed in checks.items():
            if not check_passed:
                print(f"- {check_name}")

        raise SystemExit(
            "Project verification failed. Review verification_report.txt."
        )

    print("\nDay 49 project completed successfully.")


if __name__ == "__main__":
    main()
