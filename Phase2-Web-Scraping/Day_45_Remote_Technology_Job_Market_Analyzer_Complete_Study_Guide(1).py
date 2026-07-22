"""
DAY 45 — REMOTE TECHNOLOGY JOB MARKET ANALYZER
================================================

Purpose
-------
Build a realistic end-to-end data pipeline that:

1. checks whether API access is ethically permitted;
2. collects a live Remote OK API snapshot;
3. cleans incomplete and duplicate records;
4. conservatively classifies technology and AI/automation jobs;
5. analyzes tags, locations, salaries, and AI/automation share;
6. saves results to CSV and JSON;
7. stores records in SQLite with safe upserts;
8. creates a human-readable text report; and
9. verifies every generated output.

Day 45 roadmap position
-----------------------
This project combines Python fundamentals with Phase 2 topics already learned:
functions, lists, dictionaries, loops, conditions, APIs, ethical access,
robots.txt, text cleaning, CSV, JSON, SQLite, and file handling.

Not treated as completed in Day 45
----------------------------------
Logging, retry mechanisms, and a full request-error-handling strategy remain
scheduled for the post-Day-50 recovery program. This file does not claim that
those topics are complete.

Installation
------------
    pip install requests

Run
---
    python Day_45_Remote_Technology_Job_Market_Analyzer_Complete_Study_Guide.py

Expected output folder
----------------------
    day45_job_market_output/
        remote_technology_jobs.csv
        remote_technology_jobs.json
        remote_job_market.db
        remote_technology_job_market_report.txt

Important scope warning
-----------------------
Remote OK is a live source. Record counts and results will change. The report
represents one limited API snapshot, not the entire global remote job market.
"""

from collections import Counter
import csv
from datetime import datetime, timezone
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sqlite3
from urllib import robotparser

import requests


# ---------------------------------------------------------------------------
# SECTION 1 — CONFIGURATION
# ---------------------------------------------------------------------------

PROJECT_NAME = "Remote Technology Job Market Analyzer"
SOURCE_NAME = "Remote OK"
API_URL = "https://remoteok.com/api"
ROBOTS_URL = "https://remoteok.com/robots.txt"
SOURCE_URL = "https://remoteok.com"
USER_AGENT = "Day45-Educational-Job-Market-Analyzer/1.0"
REQUEST_TIMEOUT = 30
OUTPUT_DIRECTORY = Path("day45_job_market_output")

# Recognized multi-word technology titles. Exact phrases are stronger evidence
# than generic words such as "lead", "manager", or "specialist".
TECHNOLOGY_JOB_PHRASES = [
    "ai engineer",
    "automation engineer",
    "backend developer",
    "cloud engineer",
    "computer vision engineer",
    "data analyst",
    "data engineer",
    "data scientist",
    "database administrator",
    "devops engineer",
    "frontend developer",
    "full stack developer",
    "full stack engineer",
    "machine learning engineer",
    "mobile developer",
    "mobile engineer",
    "network engineer",
    "nlp engineer",
    "platform engineer",
    "qa engineer",
    "react native engineer",
    "security engineer",
    "site reliability engineer",
    "software developer",
    "software engineer",
    "solutions architect",
    "systems administrator",
    "web developer",
]

# A generic role word is not enough on its own. It must be supported by a
# strong technology term in the title or tags.
TECHNOLOGY_ROLE_KEYWORDS = [
    "administrator",
    "analyst",
    "architect",
    "developer",
    "engineer",
    "programmer",
    "scientist",
]

STRONG_TECHNOLOGY_KEYWORDS = [
    "android",
    "api",
    "aws",
    "azure",
    "backend",
    "cloud",
    "cybersecurity",
    "data",
    "database",
    "devops",
    "django",
    "docker",
    "frontend",
    "full stack",
    "golang",
    "ios",
    "javascript",
    "kubernetes",
    "linux",
    "mobile",
    "node.js",
    "python",
    "react",
    "react native",
    "ruby",
    "security",
    "sql",
    "sys admin",
]

AI_AUTOMATION_KEYWORDS = [
    "ai",
    "artificial intelligence",
    "automation",
    "computer vision",
    "deep learning",
    "generative ai",
    "intelligent automation",
    "large language model",
    "llm",
    "machine learning",
    "ml",
    "natural language processing",
    "nlp",
    "openai",
    "rpa",
    "workflow automation",
    "workflow",
]

CSV_FIELDNAMES = [
    "job_id",
    "company",
    "position",
    "location",
    "date_posted",
    "tags",
    "salary_min",
    "salary_max",
    "url",
    "technology_matches",
    "ai_automation_matches",
    "is_ai_automation",
]


# ---------------------------------------------------------------------------
# SECTION 2 — SMALL CONCEPT EXAMPLES
# These demonstrations do not repeat the final project. They isolate the most
# important techniques so each one can be understood independently.
# ---------------------------------------------------------------------------

def demonstrate_core_concepts():
    """Show focused examples of the Python ideas used by the main project."""

    print("\nDay 45 focused examples:")

    # Example 1: clean whitespace in inconsistent text.
    messy_title = "  Senior\n  Data   Analyst  "
    cleaned_title = " ".join(messy_title.split())
    print(f"1. Cleaned text: {cleaned_title}")

    # Example 2: remove duplicates while preserving the original order.
    original_tags = ["python", "api", "python", "sql"]
    unique_tags = list(dict.fromkeys(original_tags))
    print(f"2. Unique tags: {unique_tags}")

    # Example 3: calculate a percentage safely.
    total_jobs = 8
    ai_jobs = 2
    ai_share = (ai_jobs / total_jobs * 100) if total_jobs else 0.0
    print(f"3. AI share: {ai_share:.2f}%")

    # Example 4: count repeated categorical values.
    locations = ["Remote", "Berlin", "Remote", "Toronto"]
    location_counts = Counter(locations)
    print(f"4. Location counts: {dict(location_counts)}")

    # Example 5: parameterized SQL keeps values separate from SQL syntax.
    safe_query = "SELECT * FROM jobs WHERE company = ?"
    safe_parameters = ("Example Company",)
    print(f"5. Safe SQL: {safe_query} | Values: {safe_parameters}")


# ---------------------------------------------------------------------------
# SECTION 3 — TEXT CLEANING AND KEYWORD MATCHING
# ---------------------------------------------------------------------------

def clean_text(value):
    """Convert a value to normalized single-line text.

    None becomes an empty string. HTML entities such as &amp; are decoded,
    repeated whitespace is collapsed, and leading/trailing space is removed.
    """

    if value is None:
        return ""

    decoded_text = html.unescape(str(value))
    return " ".join(decoded_text.split())


class PlainTextHTMLParser(HTMLParser):
    """Collect visible text from HTML using only Python's standard library."""

    def __init__(self):
        super().__init__()
        self.text_parts = []

    def handle_data(self, data):
        cleaned_data = clean_text(data)

        if cleaned_data:
            self.text_parts.append(cleaned_data)


def remove_html(value):
    """Remove HTML tags and return readable normalized plain text."""

    if not value:
        return ""

    parser = PlainTextHTMLParser()
    parser.feed(str(value))
    parser.close()
    return clean_text(" ".join(parser.text_parts))


def build_keyword_pattern(keyword):
    """Create a boundary-aware regular expression for one keyword.

    re.escape protects punctuation such as the dot in "node.js". The custom
    boundaries prevent short terms such as "ai" from matching inside unrelated
    words such as "training".
    """

    escaped_keyword = re.escape(keyword.lower())
    escaped_keyword = escaped_keyword.replace(r"\ ", r"\s+")
    return rf"(?<![a-z0-9]){escaped_keyword}(?![a-z0-9])"


def find_matching_keywords(text, keywords):
    """Return sorted unique keywords that occur as complete terms."""

    normalized_text = clean_text(text).lower()
    matches = []

    for keyword in keywords:
        pattern = build_keyword_pattern(keyword)

        if re.search(pattern, normalized_text, flags=re.IGNORECASE):
            matches.append(keyword.lower())

    return sorted(set(matches))


# ---------------------------------------------------------------------------
# SECTION 4 — ETHICAL ACCESS CHECK
# ---------------------------------------------------------------------------

def check_api_access():
    """Check robots.txt before requesting the API endpoint.

    robots.txt is not the only source of permission. API terms, site terms,
    applicable law, rate limits, privacy, and data-use restrictions must also
    be respected. The API response's terms record is retained later.
    """

    robots_parser = robotparser.RobotFileParser()
    robots_parser.set_url(ROBOTS_URL)
    robots_parser.read()

    api_allowed = robots_parser.can_fetch(USER_AGENT, API_URL)
    crawl_delay = robots_parser.crawl_delay(USER_AGENT)

    print("\nEthical access check:")
    print(f"API access allowed: {api_allowed}")
    print(f"Crawl delay: {crawl_delay}")

    return api_allowed, crawl_delay


# ---------------------------------------------------------------------------
# SECTION 5 — LIVE API COLLECTION
# ---------------------------------------------------------------------------

def collect_remote_jobs():
    """Request the Remote OK API and separate its terms record from jobs.

    Remote OK commonly returns a list whose first item contains API/legal
    metadata. Only dictionary records after that item are possible jobs.

    Note: a full request-error-handling and retry strategy is intentionally
    outside Day 45. raise_for_status() still prevents a failed HTTP response
    from being silently processed as valid data.
    """

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }

    response = requests.get(
        API_URL,
        headers=headers,
        timeout=REQUEST_TIMEOUT,
    )

    print(f"API status code: {response.status_code}")
    response.raise_for_status()

    api_data = response.json()

    if not isinstance(api_data, list):
        raise ValueError("Expected the Remote OK API to return a list.")

    api_terms = {}
    raw_jobs = api_data

    if api_data and isinstance(api_data[0], dict):
        possible_terms = api_data[0]

        if "legal" in possible_terms:
            api_terms = possible_terms
            raw_jobs = api_data[1:]

    print(f"Records received: {len(api_data)}")
    print(f"Possible job records: {len(raw_jobs)}")
    print(f"API terms record found: {bool(api_terms)}")

    return raw_jobs, api_terms


# ---------------------------------------------------------------------------
# SECTION 6 — CLEANING AND CONSERVATIVE CLASSIFICATION
# ---------------------------------------------------------------------------

def normalize_salary(value):
    """Return a non-negative numeric salary or 0 for unusable input."""

    if isinstance(value, bool):
        return 0

    if isinstance(value, (int, float)) and value > 0:
        return value

    return 0


def clean_and_classify_jobs(job_records):
    """Validate, deduplicate, clean, and classify raw job dictionaries.

    Conservative technology rule
    ----------------------------
    A record must have at least one of these signals:

    * a recognized technology title phrase;
    * an AI/automation term in the title; or
    * both a technology role word and a strong technology title/tag term.

    AI/automation classification is controlled by title matches. Description
    matches are examined separately as diagnostic evidence because a company
    description can mention AI even when the vacancy is not an AI job.
    """

    cleaned_jobs = []
    seen_job_ids = set()
    skipped_incomplete = 0
    skipped_duplicates = 0
    non_technology_jobs = 0

    for raw_job in job_records:
        if not isinstance(raw_job, dict):
            skipped_incomplete += 1
            continue

        job_id = clean_text(raw_job.get("id"))
        company = clean_text(raw_job.get("company"))
        position = clean_text(raw_job.get("position"))
        job_url = clean_text(raw_job.get("url") or raw_job.get("apply_url"))

        if not job_id or not company or not position or not job_url:
            skipped_incomplete += 1
            continue

        if job_id in seen_job_ids:
            skipped_duplicates += 1
            continue

        seen_job_ids.add(job_id)

        raw_tags = raw_job.get("tags", [])

        if not isinstance(raw_tags, list):
            raw_tags = []

        tags = [
            clean_text(tag).lower()
            for tag in raw_tags
            if clean_text(tag)
        ]
        tags = list(dict.fromkeys(tags))

        description = remove_html(raw_job.get("description", ""))
        location = clean_text(raw_job.get("location")) or "Not specified"
        date_posted = clean_text(raw_job.get("date"))

        title_matches = find_matching_keywords(
            position,
            TECHNOLOGY_JOB_PHRASES,
        )
        role_matches = find_matching_keywords(
            position,
            TECHNOLOGY_ROLE_KEYWORDS,
        )
        strong_technology_matches = find_matching_keywords(
            " ".join([position] + tags),
            STRONG_TECHNOLOGY_KEYWORDS,
        )
        ai_title_matches = find_matching_keywords(
            position,
            AI_AUTOMATION_KEYWORDS,
        )

        technology_matches = sorted(
            set(
                title_matches
                + ai_title_matches
                + (
                    strong_technology_matches
                    if role_matches
                    else []
                )
            )
        )

        if not technology_matches:
            non_technology_jobs += 1
            continue

        ai_automation_matches = ai_title_matches

        cleaned_job = {
            "job_id": job_id,
            "company": company,
            "position": position,
            "location": location,
            "date_posted": date_posted,
            "tags": tags,
            "description": description,
            "salary_min": normalize_salary(raw_job.get("salary_min")),
            "salary_max": normalize_salary(raw_job.get("salary_max")),
            "url": job_url,
            "technology_matches": technology_matches,
            "ai_automation_matches": ai_automation_matches,
            "is_ai_automation": bool(ai_automation_matches),
        }

        cleaned_jobs.append(cleaned_job)

    ai_job_count = sum(
        1 for job in cleaned_jobs if job["is_ai_automation"]
    )

    print("\nCleaning and classification results:")
    print(f"Raw possible jobs: {len(job_records)}")
    print(f"Technology jobs retained: {len(cleaned_jobs)}")
    print(f"Non-technology jobs excluded: {non_technology_jobs}")
    print(f"Incomplete records skipped: {skipped_incomplete}")
    print(f"Duplicate records skipped: {skipped_duplicates}")
    print(f"AI/automation jobs identified: {ai_job_count}")

    return cleaned_jobs


def preview_classification(jobs):
    """Print retained jobs and diagnostic AI terms found in descriptions."""

    print("\nTechnology job preview:")

    if not jobs:
        print("- No technology jobs matched the rules")

    for job in jobs:
        print(
            f"- {job['position']} | "
            f"Tags: {', '.join(job['tags']) or 'None'} | "
            f"Technology matches: "
            f"{', '.join(job['technology_matches'])}"
        )

    description_mentions = []

    for job in jobs:
        matches = find_matching_keywords(
            job["description"],
            AI_AUTOMATION_KEYWORDS,
        )

        if matches:
            description_mentions.append((job, matches))

    print("\nPossible AI/automation mentions in descriptions:")
    print(
        "Technology jobs with AI/automation terms in descriptions: "
        f"{len(description_mentions)}"
    )

    for job, matches in description_mentions:
        print(
            f"- {job['position']} at {job['company']} | "
            f"Matches: {', '.join(matches)}"
        )


# ---------------------------------------------------------------------------
# SECTION 7 — ANALYSIS
# ---------------------------------------------------------------------------

def analyze_job_market(jobs):
    """Calculate a summary of the retained technology-job snapshot."""

    total_technology_jobs = len(jobs)
    ai_automation_jobs = [
        job for job in jobs if job["is_ai_automation"]
    ]
    non_ai_technology_jobs = [
        job for job in jobs if not job["is_ai_automation"]
    ]

    tag_counts = Counter(tag for job in jobs for tag in job["tags"])
    location_counts = Counter(job["location"] for job in jobs)
    jobs_with_salary = [
        job
        for job in jobs
        if job["salary_min"] > 0 or job["salary_max"] > 0
    ]

    ai_percentage = (
        len(ai_automation_jobs) / total_technology_jobs * 100
        if total_technology_jobs
        else 0.0
    )

    # JSON does not preserve tuples. Converting Counter results to lists here
    # ensures that analysis == json.load(saved_file)["analysis"] later.
    analysis = {
        "total_technology_jobs": total_technology_jobs,
        "ai_automation_jobs": len(ai_automation_jobs),
        "non_ai_technology_jobs": len(non_ai_technology_jobs),
        "ai_percentage": ai_percentage,
        "jobs_with_salary": len(jobs_with_salary),
        "common_tags": [
            list(item) for item in tag_counts.most_common(10)
        ],
        "common_locations": [
            list(item) for item in location_counts.most_common(10)
        ],
    }

    print("\nRemote technology job-market analysis:")
    print(f"Technology jobs analyzed: {total_technology_jobs}")
    print(f"AI/automation jobs: {len(ai_automation_jobs)}")
    print(f"Other technology jobs: {len(non_ai_technology_jobs)}")
    print(f"AI/automation share: {ai_percentage:.2f}%")
    print(f"Jobs providing salary information: {len(jobs_with_salary)}")

    print("\nMost common tags:")
    if analysis["common_tags"]:
        for tag, count in analysis["common_tags"]:
            print(f"- {tag}: {count}")
    else:
        print("- No tags available")

    print("\nMost common locations:")
    if analysis["common_locations"]:
        for location, count in analysis["common_locations"]:
            print(f"- {location}: {count}")
    else:
        print("- No locations available")

    return analysis


# ---------------------------------------------------------------------------
# SECTION 8 — CSV AND JSON OUTPUT
# ---------------------------------------------------------------------------

def save_jobs_to_csv(jobs, output_directory):
    """Save compact, spreadsheet-friendly job records."""

    output_directory.mkdir(parents=True, exist_ok=True)
    csv_path = output_directory / "remote_technology_jobs.csv"

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()

        for job in jobs:
            csv_record = {
                field: job[field] for field in CSV_FIELDNAMES
            }
            csv_record["tags"] = ", ".join(job["tags"])
            csv_record["technology_matches"] = ", ".join(
                job["technology_matches"]
            )
            csv_record["ai_automation_matches"] = ", ".join(
                job["ai_automation_matches"]
            )
            writer.writerow(csv_record)

    print(f"CSV records saved: {len(jobs)}")
    print(f"CSV file: {csv_path}")
    return csv_path


def save_jobs_to_json(jobs, analysis, output_directory):
    """Save full structured records, including descriptions and analysis."""

    output_directory.mkdir(parents=True, exist_ok=True)
    json_path = output_directory / "remote_technology_jobs.json"

    json_data = {
        "project": PROJECT_NAME,
        "source": SOURCE_NAME,
        "source_api": API_URL,
        "collected_at_utc": datetime.now(timezone.utc).isoformat(),
        "snapshot_warning": (
            "This analysis represents a limited current Remote OK API "
            "snapshot, not the complete remote technology job market."
        ),
        "analysis": analysis,
        "jobs": jobs,
    }

    with json_path.open("w", encoding="utf-8") as json_file:
        json.dump(
            json_data,
            json_file,
            indent=4,
            ensure_ascii=False,
        )

    print(f"JSON records saved: {len(jobs)}")
    print(f"JSON file: {json_path}")
    return json_path


# ---------------------------------------------------------------------------
# SECTION 9 — SQLITE STORAGE
# ---------------------------------------------------------------------------

def save_jobs_to_sqlite(jobs, output_directory):
    """Create the database and insert or update jobs by unique job_id."""

    output_directory.mkdir(parents=True, exist_ok=True)
    database_path = output_directory / "remote_job_market.db"

    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS technology_jobs (
                job_id TEXT PRIMARY KEY,
                company TEXT NOT NULL,
                position TEXT NOT NULL,
                location TEXT NOT NULL,
                date_posted TEXT,
                tags TEXT,
                description TEXT,
                salary_min REAL,
                salary_max REAL,
                url TEXT NOT NULL,
                technology_matches TEXT,
                ai_automation_matches TEXT,
                is_ai_automation INTEGER NOT NULL
            )
            """
        )

        for job in jobs:
            cursor.execute(
                """
                INSERT INTO technology_jobs (
                    job_id,
                    company,
                    position,
                    location,
                    date_posted,
                    tags,
                    description,
                    salary_min,
                    salary_max,
                    url,
                    technology_matches,
                    ai_automation_matches,
                    is_ai_automation
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(job_id) DO UPDATE SET
                    company = excluded.company,
                    position = excluded.position,
                    location = excluded.location,
                    date_posted = excluded.date_posted,
                    tags = excluded.tags,
                    description = excluded.description,
                    salary_min = excluded.salary_min,
                    salary_max = excluded.salary_max,
                    url = excluded.url,
                    technology_matches = excluded.technology_matches,
                    ai_automation_matches = excluded.ai_automation_matches,
                    is_ai_automation = excluded.is_ai_automation
                """,
                (
                    job["job_id"],
                    job["company"],
                    job["position"],
                    job["location"],
                    job["date_posted"],
                    json.dumps(job["tags"], ensure_ascii=False),
                    job["description"],
                    job["salary_min"],
                    job["salary_max"],
                    job["url"],
                    json.dumps(
                        job["technology_matches"],
                        ensure_ascii=False,
                    ),
                    json.dumps(
                        job["ai_automation_matches"],
                        ensure_ascii=False,
                    ),
                    int(job["is_ai_automation"]),
                ),
            )

        cursor.execute("SELECT COUNT(*) FROM technology_jobs")
        total_database_jobs = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM technology_jobs
            WHERE is_ai_automation = 1
            """
        )
        total_database_ai_jobs = cursor.fetchone()[0]

    print("\nSQLite storage results:")
    print(f"Records processed: {len(jobs)}")
    print(f"Total jobs stored: {total_database_jobs}")
    print(f"AI/automation jobs stored: {total_database_ai_jobs}")
    print(f"SQLite database: {database_path}")
    return database_path


# ---------------------------------------------------------------------------
# SECTION 10 — HUMAN-READABLE TEXT REPORT
# ---------------------------------------------------------------------------

def format_salary(job):
    """Create a readable salary label without inventing missing values."""

    salary_min = job["salary_min"]
    salary_max = job["salary_max"]

    if salary_min > 0 and salary_max > 0:
        return f"${salary_min:,.0f}–${salary_max:,.0f}"
    if salary_min > 0:
        return f"From ${salary_min:,.0f}"
    if salary_max > 0:
        return f"Up to ${salary_max:,.0f}"
    return "Not provided"


def create_text_report(jobs, analysis, api_terms, output_directory):
    """Generate a readable report with scope note and source attribution."""

    output_directory.mkdir(parents=True, exist_ok=True)
    report_path = (
        output_directory / "remote_technology_job_market_report.txt"
    )
    collected_at = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    report_lines = [
        "REMOTE TECHNOLOGY JOB MARKET ANALYZER",
        "=" * 45,
        "",
        f"Source: {SOURCE_NAME}",
        f"Source API: {API_URL}",
        f"Collected at: {collected_at}",
        "",
        "IMPORTANT SCOPE NOTE",
        "-" * 45,
        (
            "This report represents a limited live snapshot from the "
            "Remote OK API."
        ),
        (
            "It does not represent the complete global remote technology "
            "job market."
        ),
        (
            "Technology and AI/automation classifications use conservative "
            "title-and-tag rules."
        ),
        "",
        "MARKET SUMMARY",
        "-" * 45,
        (
            "Technology jobs analyzed: "
            f"{analysis['total_technology_jobs']}"
        ),
        f"AI/automation jobs: {analysis['ai_automation_jobs']}",
        (
            "Other technology jobs: "
            f"{analysis['non_ai_technology_jobs']}"
        ),
        f"AI/automation share: {analysis['ai_percentage']:.2f}%",
        (
            "Jobs providing salary information: "
            f"{analysis['jobs_with_salary']}"
        ),
        "",
        "MOST COMMON TAGS",
        "-" * 45,
    ]

    if analysis["common_tags"]:
        for tag, count in analysis["common_tags"]:
            report_lines.append(f"- {tag}: {count}")
    else:
        report_lines.append("- No tags available")

    report_lines.extend(["", "MOST COMMON LOCATIONS", "-" * 45])

    if analysis["common_locations"]:
        for location, count in analysis["common_locations"]:
            report_lines.append(f"- {location}: {count}")
    else:
        report_lines.append("- No locations available")

    report_lines.extend(["", "CLEANED TECHNOLOGY JOBS", "-" * 45])

    if jobs:
        for number, job in enumerate(jobs, start=1):
            report_lines.extend(
                [
                    f"{number}. {job['position']}",
                    f"   Company: {job['company']}",
                    f"   Location: {job['location']}",
                    (
                        "   Date posted: "
                        f"{job['date_posted'] or 'Not provided'}"
                    ),
                    f"   Tags: {', '.join(job['tags']) or 'None'}",
                    (
                        "   Technology matches: "
                        f"{', '.join(job['technology_matches'])}"
                    ),
                    (
                        "   AI/automation: "
                        f"{'Yes' if job['is_ai_automation'] else 'No'}"
                    ),
                    (
                        "   AI/automation matches: "
                        f"{', '.join(job['ai_automation_matches']) or 'None'}"
                    ),
                    f"   Salary: {format_salary(job)}",
                    f"   Job URL: {job['url']}",
                    "",
                ]
            )
    else:
        report_lines.append(
            "No technology jobs matched the classification rules."
        )

    legal_terms = ""
    if isinstance(api_terms, dict):
        legal_terms = clean_text(api_terms.get("legal"))

    report_lines.extend(
        [
            "SOURCE CREDIT AND API TERMS",
            "-" * 45,
            f"Job data sourced from Remote OK: {SOURCE_URL}",
            legal_terms or "No API terms text was returned.",
            "",
            "END OF REPORT",
        ]
    )

    with report_path.open("w", encoding="utf-8") as report_file:
        report_file.write("\n".join(report_lines))

    print("\nFinal report results:")
    print(f"Jobs included in report: {len(jobs)}")
    print(f"Text report: {report_path}")
    print(f"Remote OK API terms included: {bool(legal_terms)}")
    return report_path


# ---------------------------------------------------------------------------
# SECTION 11 — END-TO-END VERIFICATION
# ---------------------------------------------------------------------------

def verify_output_files(
    jobs,
    analysis,
    csv_path,
    json_path,
    database_path,
    report_path,
):
    """Verify files, record counts, analysis, database, and report sections."""

    verification_results = []
    expected_paths = [csv_path, json_path, database_path, report_path]

    for file_path in expected_paths:
        file_exists = file_path.exists()
        file_not_empty = file_exists and file_path.stat().st_size > 0
        verification_results.append(
            (
                f"{file_path.name} exists and is not empty",
                file_not_empty,
            )
        )

    with csv_path.open("r", newline="", encoding="utf-8") as csv_file:
        csv_rows = list(csv.DictReader(csv_file))

    verification_results.append(
        (
            "CSV job count matches cleaned job count",
            len(csv_rows) == len(jobs),
        )
    )

    with json_path.open("r", encoding="utf-8") as json_file:
        saved_json_data = json.load(json_file)

    json_jobs = saved_json_data.get("jobs", [])
    json_analysis = saved_json_data.get("analysis", {})
    verification_results.append(
        (
            "JSON job count matches cleaned job count",
            len(json_jobs) == len(jobs),
        )
    )
    verification_results.append(
        (
            "JSON analysis matches current analysis",
            json_analysis == analysis,
        )
    )

    current_job_ids = [job["job_id"] for job in jobs]
    database_current_jobs = 0
    database_current_ai_jobs = 0

    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()

        if current_job_ids:
            placeholders = ", ".join("?" for _ in current_job_ids)
            cursor.execute(
                f"""
                SELECT COUNT(*)
                FROM technology_jobs
                WHERE job_id IN ({placeholders})
                """,
                current_job_ids,
            )
            database_current_jobs = cursor.fetchone()[0]

            cursor.execute(
                f"""
                SELECT COUNT(*)
                FROM technology_jobs
                WHERE job_id IN ({placeholders})
                  AND is_ai_automation = 1
                """,
                current_job_ids,
            )
            database_current_ai_jobs = cursor.fetchone()[0]

    verification_results.append(
        (
            "Current cleaned jobs exist in SQLite",
            database_current_jobs == len(jobs),
        )
    )
    verification_results.append(
        (
            "SQLite AI count matches current analysis",
            database_current_ai_jobs == analysis["ai_automation_jobs"],
        )
    )

    with report_path.open("r", encoding="utf-8") as report_file:
        report_text = report_file.read()

    required_report_sections = [
        "REMOTE TECHNOLOGY JOB MARKET ANALYZER",
        "IMPORTANT SCOPE NOTE",
        "MARKET SUMMARY",
        "MOST COMMON TAGS",
        "MOST COMMON LOCATIONS",
        "CLEANED TECHNOLOGY JOBS",
        "SOURCE CREDIT AND API TERMS",
        "END OF REPORT",
    ]
    report_sections_present = all(
        section in report_text for section in required_report_sections
    )
    verification_results.append(
        (
            "Text report contains all required sections",
            report_sections_present,
        )
    )
    verification_results.append(
        (
            "Text report contains Remote OK source credit",
            SOURCE_URL in report_text,
        )
    )

    print("\nEnd-to-end output verification:")
    for check_name, passed in verification_results:
        result = "PASS" if passed else "FAIL"
        print(f"[{result}] {check_name}")

    passed_checks = sum(
        1 for _, passed in verification_results if passed
    )
    total_checks = len(verification_results)
    all_checks_passed = passed_checks == total_checks

    print(f"\nVerification checks passed: {passed_checks}/{total_checks}")
    print(f"Overall verification: {'PASS' if all_checks_passed else 'FAIL'}")
    return all_checks_passed


# ---------------------------------------------------------------------------
# SECTION 12 — POSSIBLE ISSUES AND LIMITATIONS
# ---------------------------------------------------------------------------

POSSIBLE_ISSUES = [
    "Live API results, tags, salaries, and record counts can change.",
    "Conservative classification can exclude genuine technology jobs.",
    "Broad or inaccurate source tags can still produce false positives.",
    "AI in a title may describe a strategy role rather than engineering.",
    "Description keywords can describe the company instead of the vacancy.",
    "Required or optional API fields may be missing or malformed.",
    "Salary currency, period, accuracy, or recency may be unclear.",
    "A changed API response structure can break cleaning or reporting.",
    "SQLite retains older IDs, so it may become a historical collection.",
    "Different IDs can represent the same vacancy, limiting deduplication.",
    "HTML removal can merge words or discard meaningful formatting.",
    "Permissions, locked files, disk space, or corruption can block output.",
    "API permissions and terms may change and must be checked again.",
    "Verification proves internal consistency, not objective correctness.",
]


def print_possible_issues():
    """Print the main real-world limitations of this project."""

    print("\nPossible issues that could arise:")
    for number, issue in enumerate(POSSIBLE_ISSUES, start=1):
        print(f"{number}. {issue}")


# ---------------------------------------------------------------------------
# SECTION 13 — MAIN PROGRAM
# ---------------------------------------------------------------------------

def main():
    """Run the complete Day 45 workflow in the correct order."""

    print(PROJECT_NAME)
    print(f"Source: {SOURCE_NAME}")
    print(f"API: {API_URL}")
    print(f"Technology title phrases: {len(TECHNOLOGY_JOB_PHRASES)}")
    print(f"AI/automation keywords: {len(AI_AUTOMATION_KEYWORDS)}")

    demonstrate_core_concepts()

    api_allowed, _crawl_delay = check_api_access()

    if not api_allowed:
        print("Collection stopped because robots.txt disallows API access.")
        return

    raw_jobs, api_terms = collect_remote_jobs()
    technology_jobs = clean_and_classify_jobs(raw_jobs)
    preview_classification(technology_jobs)
    market_analysis = analyze_job_market(technology_jobs)

    print("\nSaving cleaned job data:")
    csv_file_path = save_jobs_to_csv(
        technology_jobs,
        OUTPUT_DIRECTORY,
    )
    json_file_path = save_jobs_to_json(
        technology_jobs,
        market_analysis,
        OUTPUT_DIRECTORY,
    )
    database_file_path = save_jobs_to_sqlite(
        technology_jobs,
        OUTPUT_DIRECTORY,
    )
    report_file_path = create_text_report(
        technology_jobs,
        market_analysis,
        api_terms,
        OUTPUT_DIRECTORY,
    )

    outputs_verified = verify_output_files(
        technology_jobs,
        market_analysis,
        csv_file_path,
        json_file_path,
        database_file_path,
        report_file_path,
    )

    print_possible_issues()

    print("\nDay 45 final result:")
    if outputs_verified:
        print("The complete output pipeline passed all 11 checks.")
    else:
        print("At least one output check failed. Review the results above.")


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# DAY 45 SUMMARY
# ---------------------------------------------------------------------------
#
# Key lessons:
# - Check access rules and source terms before collection.
# - Treat live API data as a limited snapshot.
# - Validate required fields before using a record.
# - Deduplicate by a stable identifier when one is available.
# - Prefer conservative classification rules over easy false positives.
# - Keep description keyword mentions diagnostic when they are weak evidence.
# - Counter efficiently measures categorical frequencies.
# - CSV is compact and spreadsheet-friendly; JSON preserves nested structure.
# - SQLite primary keys and upserts support persistent, repeatable storage.
# - Parameterized SQL separates data from SQL syntax.
# - Reports should include scope limitations and source attribution.
# - Automated verification catches inconsistent or incomplete outputs.
# - Python tuples become JSON lists; normalize them before equality checks.
# - Passing tests proves internal consistency, not real-world truth.
#
# Useful professional phrases:
# - "The results represent a limited live snapshot."
# - "The classification uses conservative title-based rules."
# - "Description matches are diagnostic evidence."
# - "The database updates records using unique job IDs."
# - "All generated outputs passed end-to-end verification."
# - "Internal consistency does not guarantee objective accuracy."
#
# Pending after Day 50 (not completed here):
# - complete request-error handling;
# - retry mechanisms; and
# - logging.
