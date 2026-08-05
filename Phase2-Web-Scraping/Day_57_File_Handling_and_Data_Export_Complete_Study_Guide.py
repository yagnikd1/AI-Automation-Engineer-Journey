"""
Day 57 - File Handling and Data Export

Project: International Research Grant Listing Exporter

Topics revised and practised:
- tuples, lists, sets, dictionaries, loops, conditions, and functions
- duplicate detection and missing-value cleaning
- pathlib paths and output directories
- file modes: r, w, a, and x
- manual close() and automatic closing with with
- UTF-8 text files
- CSV export and round-trip validation
- JSON export and round-trip validation
- readable text reports
- consolidated export validation

The sample records are local HTML-like dictionaries so the program can focus
on file handling without depending on a live website.
"""

import csv
import json
from pathlib import Path


REQUIRED_FIELDS = (
    "grant_id",
    "title",
    "country",
    "amount_usd",
    "status",
)

RAW_GRANT_LISTINGS = [
    {
        "grant_id": " GR-201 ",
        "title": " Renewable Energy Research Fund ",
        "country": " Denmark ",
        "amount_usd": " $25,000 ",
        "status": " Open ",
    },
    {
        "grant_id": " GR-202 ",
        "title": " Marine Conservation Initiative ",
        "country": " Portugal ",
        "amount_usd": " $18,500 ",
        "status": " Closed ",
    },
    {
        "grant_id": " GR-201 ",
        "title": " Renewable Energy Research Fund ",
        "country": " Denmark ",
        "amount_usd": " $25,000 ",
        "status": " Open ",
    },
    {
        "grant_id": " GR-203 ",
        "title": " Public Health Innovation Grant ",
        "country": " ",
        "amount_usd": " $32,000 ",
        "status": " Open ",
    },
]


def clean_text(value, fallback="Unavailable"):
    """Return stripped text, or a fallback when the value is missing."""
    if value is None:
        return fallback

    cleaned_value = str(value).strip()
    return cleaned_value if cleaned_value else fallback


def clean_amount(value):
    """Convert a currency string such as '$25,000' to the integer 25000."""
    if value is None:
        return None

    cleaned_value = str(value).replace("$", "").replace(",", "").strip()
    return int(cleaned_value) if cleaned_value.isdigit() else None


def collect_unique_grants(raw_listings):
    """Clean records, exclude duplicate IDs, and return audit information."""
    grants = []
    seen_ids = set()
    duplicate_ids = []

    for raw_grant in raw_listings:
        grant_id = clean_text(raw_grant.get("grant_id"), "ID Unavailable")

        if grant_id in seen_ids:
            duplicate_ids.append(grant_id)
            continue

        seen_ids.add(grant_id)
        cleaned_grant = {
            "grant_id": grant_id,
            "title": clean_text(raw_grant.get("title"), "Title Unavailable"),
            "country": clean_text(
                raw_grant.get("country"),
                "Country Unavailable",
            ),
            "amount_usd": clean_amount(raw_grant.get("amount_usd")),
            "status": clean_text(raw_grant.get("status"), "Status Unavailable"),
        }
        grants.append(cleaned_grant)

    return grants, duplicate_ids


def write_preview(preview_path, grants, open_grant_count):
    """Demonstrate manual close(), append mode, and read mode."""
    preview_file = open(preview_path, "w", encoding="utf-8")
    preview_file.write("International Research Grant Listing Exporter\n")
    preview_file.write("=" * 46 + "\n")
    preview_file.write(f"Unique grants: {len(grants)}\n")
    preview_file.write(f"Open grants: {open_grant_count}\n")
    preview_file.close()

    print("Initial preview written successfully.")
    print("File closed:", preview_file.closed)

    with open(preview_path, "a", encoding="utf-8") as preview_file:
        preview_file.write("\nGrant records:\n")
        for grant in grants:
            preview_file.write(
                f"{grant['grant_id']} | "
                f"{grant['title']} | "
                f"{grant['country']} | "
                f"${grant['amount_usd']} | "
                f"{grant['status']}\n"
            )

    print("Grant records appended successfully.")
    print("File closed after with-block:", preview_file.closed)


def export_csv(csv_path, required_fields, grants):
    """Write dictionaries to CSV and load them back for validation."""
    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=required_fields)
        writer.writeheader()
        writer.writerows(grants)

    with open(csv_path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        loaded_records = list(reader)
        loaded_fieldnames = reader.fieldnames

    validations = {
        "csv_record_count": len(loaded_records) == len(grants),
        "csv_fields": tuple(loaded_fieldnames or []) == required_fields,
    }
    return loaded_records, loaded_fieldnames, validations


def export_json(json_path, required_fields, grants, duplicates, open_count):
    """Write structured JSON and load it back to verify type preservation."""
    export_data = {
        "export_name": "International Research Grant Listing Exporter",
        "required_fields": list(required_fields),
        "summary": {
            "unique_grants": len(grants),
            "open_grants": open_count,
            "duplicate_ids": duplicates,
        },
        "grant_records": grants,
    }

    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(export_data, json_file, indent=4, ensure_ascii=False)

    with open(json_path, "r", encoding="utf-8") as json_file:
        loaded_data = json.load(json_file)

    loaded_records = loaded_data["grant_records"]
    validations = {
        "json_record_count": len(loaded_records) == len(grants),
        "json_fields": all(
            tuple(record.keys()) == required_fields
            for record in loaded_records
        ),
        "json_data": loaded_records == grants,
    }
    return loaded_data, validations


def build_grant_report_lines(grant_records, duplicate_ids, open_count):
    """Build a list of lines ready for writelines()."""
    total_amount = sum(
        grant["amount_usd"]
        for grant in grant_records
        if grant["amount_usd"] is not None
    )

    report_lines = [
        "INTERNATIONAL RESEARCH GRANT REPORT\n",
        "=" * 43 + "\n",
        f"Unique grants: {len(grant_records)}\n",
        f"Open grants: {open_count}\n",
        f"Duplicate IDs excluded: {duplicate_ids}\n",
        f"Total listed funding: ${total_amount:,}\n",
        "\n",
        "GRANT RECORDS\n",
        "-" * 43 + "\n",
    ]

    for position, grant in enumerate(grant_records, start=1):
        report_lines.append(
            f"{position}. {grant['grant_id']} | "
            f"{grant['title']} | "
            f"{grant['country']} | "
            f"${grant['amount_usd']:,} | "
            f"{grant['status']}\n"
        )

    return report_lines


def export_text_report(report_path, grants, duplicates, open_count):
    """Write a report and validate its first line, IDs, and summary."""
    report_lines = build_grant_report_lines(grants, duplicates, open_count)

    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.writelines(report_lines)

    with open(report_path, "r", encoding="utf-8") as report_file:
        first_line = report_file.readline().strip()
        remaining_lines = report_file.readlines()

    loaded_lines = [first_line] + [line.rstrip("\n") for line in remaining_lines]
    contains_all_ids = all(
        any(grant["grant_id"] in line for line in loaded_lines)
        for grant in grants
    )
    contains_summary = (
        f"Unique grants: {len(grants)}" in loaded_lines
        and f"Open grants: {open_count}" in loaded_lines
    )

    validations = {
        "report_grant_ids": contains_all_ids,
        "report_summary": contains_summary,
    }
    return first_line, loaded_lines, validations


def print_export_audit(export_paths, validation_results):
    """Confirm that all expected files exist, contain data, and passed checks."""
    print("\n--- CONSOLIDATED EXPORT AUDIT ---")

    all_exports_exist = all(
        path.exists() and path.is_file()
        for path in export_paths.values()
    )
    all_exports_have_content = all(
        path.stat().st_size > 0
        for path in export_paths.values()
    )

    for export_name, path in export_paths.items():
        print(
            f"{export_name.title()} export | {path.name} | "
            f"Exists: {path.exists()} | Size: {path.stat().st_size} bytes"
        )

    print("All expected exports exist:", all_exports_exist)
    print("All expected exports contain data:", all_exports_have_content)

    for check_name, passed in validation_results.items():
        print(f"{check_name}: {'PASS' if passed else 'FAIL'}")

    print("All content validations passed:", all(validation_results.values()))


def demonstrate_exclusive_mode(output_directory):
    """Create a file once with x mode, then skip safely on later runs."""
    print("\n--- EXCLUSIVE CREATION MODE ---")
    exclusive_path = output_directory / "exclusive_mode_example.txt"

    if not exclusive_path.exists():
        with open(exclusive_path, "x", encoding="utf-8") as exclusive_file:
            exclusive_file.write(
                "This file was created using exclusive creation mode.\n"
            )
        print("Exclusive file created:", True)
    else:
        print("Exclusive file already exists; creation skipped.")

    print("Exclusive file exists:", exclusive_path.exists())
    print("Exclusive file size:", exclusive_path.stat().st_size, "bytes")


def main():
    print("Starting International Research Grant Listing Exporter...")

    grants, duplicates = collect_unique_grants(RAW_GRANT_LISTINGS)
    open_grant_count = sum(
        grant["status"].lower() == "open"
        for grant in grants
    )

    print("\n--- COLLECTION RESULTS ---")
    print("Required fields:", REQUIRED_FIELDS)
    print("Required-fields type:", type(REQUIRED_FIELDS))
    print("Grant records type:", type(grants))
    print("Duplicate IDs:", duplicates)
    print("Unique grant count:", len(grants))
    print("Open grant count:", open_grant_count)

    print("\n--- CLEANED GRANT RECORDS ---")
    for position, grant in enumerate(grants, start=1):
        print(
            f"{position}. {grant['grant_id']} | {grant['title']} | "
            f"{grant['country']} | ${grant['amount_usd']} | {grant['status']}"
        )

    print("\n--- PATH AND DIRECTORY SETUP ---")
    output_directory = Path("day57_grant_output")
    output_directory.mkdir(parents=True, exist_ok=True)
    preview_path = output_directory / "grant_export_preview.txt"
    csv_path = output_directory / "international_research_grants.csv"
    json_path = output_directory / "international_research_grants.json"
    report_path = output_directory / "international_research_grants_report.txt"

    print("Current working directory:", Path.cwd())
    print("Output directory:", output_directory.resolve())
    print("Output directory exists:", output_directory.exists())
    print("Output path type:", type(preview_path))

    print("\n--- BASIC FILE HANDLING ---")
    write_preview(preview_path, grants, open_grant_count)

    print("\n--- FILE VALIDATION ---")
    print("Preview file exists:", preview_path.exists())
    print("Path points to a file:", preview_path.is_file())
    print("File name:", preview_path.name)
    print("File extension:", preview_path.suffix)
    print("Parent directory:", preview_path.parent)
    print("Preview file size:", preview_path.stat().st_size, "bytes")
    with open(preview_path, "r", encoding="utf-8") as preview_file:
        print("\n--- PREVIEW FILE CONTENT ---")
        print(preview_file.read())

    print("\n--- CSV EXPORT ---")
    loaded_csv, csv_fields, csv_validations = export_csv(
        csv_path,
        REQUIRED_FIELDS,
        grants,
    )
    print("CSV export completed:", csv_path.exists())
    print("CSV filename:", csv_path.name)
    print("CSV file size:", csv_path.stat().st_size, "bytes")
    print("\n--- CSV VALIDATION ---")
    print("CSV records loaded:", len(loaded_csv))
    print("CSV field names:", csv_fields)
    print("Loaded CSV type:", type(loaded_csv))
    print("Loaded amount type:", type(loaded_csv[0]["amount_usd"]))
    print("CSV record count matches:", csv_validations["csv_record_count"])
    print("CSV fields match:", csv_validations["csv_fields"])

    print("\n--- JSON EXPORT ---")
    loaded_json, json_validations = export_json(
        json_path,
        REQUIRED_FIELDS,
        grants,
        duplicates,
        open_grant_count,
    )
    loaded_json_records = loaded_json["grant_records"]
    print("JSON export completed:", json_path.exists())
    print("JSON filename:", json_path.name)
    print("JSON file size:", json_path.stat().st_size, "bytes")
    print("\n--- JSON VALIDATION ---")
    print("Loaded JSON type:", type(loaded_json))
    print("Loaded records type:", type(loaded_json_records))
    print("JSON records loaded:", len(loaded_json_records))
    print("Loaded amount type:", type(loaded_json_records[0]["amount_usd"]))
    print("JSON record count matches:", json_validations["json_record_count"])
    print("JSON fields match:", json_validations["json_fields"])
    print("JSON data matches original:", json_validations["json_data"])

    print("\n--- FINAL TEXT REPORT EXPORT ---")
    first_line, loaded_report_lines, report_validations = export_text_report(
        report_path,
        grants,
        duplicates,
        open_grant_count,
    )
    print("Text report completed:", report_path.exists())
    print("Text report filename:", report_path.name)
    print("Text report size:", report_path.stat().st_size, "bytes")
    print("\n--- TEXT REPORT VALIDATION ---")
    print("First report line:", first_line)
    print("Loaded report-line count:", len(loaded_report_lines))
    print("Report contains every grant ID:", report_validations["report_grant_ids"])
    print("Report contains correct summary:", report_validations["report_summary"])
    print("\n--- FINAL TEXT REPORT CONTENT ---")
    with open(report_path, "r", encoding="utf-8") as report_file:
        print(report_file.read())

    export_paths = {
        "preview": preview_path,
        "csv": csv_path,
        "json": json_path,
        "report": report_path,
    }
    validation_results = {
        **csv_validations,
        **json_validations,
        **report_validations,
    }
    print_export_audit(export_paths, validation_results)
    demonstrate_exclusive_mode(output_directory)


if __name__ == "__main__":
    main()
