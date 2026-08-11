# Phase 2 — Web Scraping

Phase 2 of the AI Automation Engineer Journey is complete through Day 65. It develops a responsible, production-minded workflow for collecting public web/API data, validating it, storing it, exporting it, and recovering safely from failures.

## Completed scope

| Days | Topics and outcomes |
|---|---|
| 29–34 | HTTP downloads, HTML structure, Beautiful Soup, DOM navigation, CSS selectors, `select()` and `select_one()` |
| 35–37 | CSV and JSON output, structured records, and deeper DOM traversal |
| 38–41 | Pagination, headers, rate limiting, request error handling, sessions, and cookies |
| 42–45 | REST APIs, SQLite, robots.txt and ethical scraping, and a remote job-market project |
| 46–50 | Integrated API/scraping pipelines, country statistics, validation, audit projects, and accessibility data |
| 51–57 | Guided Python + scraping revision: HTTP, strings, selectors, loops, collections, functions, files, CSV, and JSON |
| 58–65 | Environments, sessions, advanced HTTP failures, retries/backoff, logging, debugging, partial-failure recovery, professional integration, and final recovery project |

## Checkpoint deliverables

- `Phase_2_Historical_Price_Change_Tracker.py` stores the latest observation between runs, compares old and new prices, and appends change alerts to JSON Lines.
- `Day_42_Web_Scraping_and_REST_API_Complete_Study_Guide.py` includes the earlier competitor price-comparison work and REST API study.
- `Day_45_Remote_Technology_Job_Market_Analyzer_Complete_Study_Guide(1).py` is the first larger real-world market-analysis project.
- `Day_65_Final_Guided_Recovery_Project.py` closes the phase with an integrated recovery-oriented project.

## Installation

Python 3.14 was used during the roadmap. From an activated virtual environment:

```bash
python -m pip install requests beautifulsoup4 urllib3
```

Individual projects may use only part of this dependency set. SQLite, CSV, JSON, logging, and file handling are provided by Python's standard library.

## Running a study file

Run a file from the repository root, quoting paths that contain spaces:

```bash
python "Phase2-Web-Scraping/Day_65_Final_Guided_Recovery_Project.py"
```

Live websites and APIs can change after a lesson is committed. A changed selector, rate limit, response schema, network failure, or service outage does not automatically mean the Python concept is wrong; inspect the current response and logs before changing code.

## Historical price-change checkpoint

The tracker includes a deterministic demonstration so historical detection can be tested without repeatedly requesting a commercial website:

```bash
cd Phase2-Web-Scraping
python Phase_2_Historical_Price_Change_Tracker.py --demo
python Phase_2_Historical_Price_Change_Tracker.py --demo-change
```

The first run stores USD 99.00. The second run stores USD 89.00, detects the decrease, prints an alert, and appends it to `price_change_alerts.jsonl`. Generated state and alert files are runtime output and should not be committed.

For a permitted public practice page, provide its URL and the two CSS selectors explicitly:

```bash
python Phase_2_Historical_Price_Change_Tracker.py \
  --url "https://example.com/permitted-product" \
  --name-selector "h1.product-name" \
  --price-selector "span.price" \
  --currency USD
```

Before using live mode, confirm the site's terms, robots policy, and allowed request frequency. The project does not bypass authentication, CAPTCHA, access controls, or anti-bot protections.

## Output patterns covered

- CSV tables for spreadsheet-compatible results.
- JSON and JSON Lines for structured records and alerts.
- SQLite for persistent queries, uniqueness constraints, and updates.
- Text reports and logging files for human-readable summaries and diagnostics.
- Atomic state replacement in the historical price tracker to reduce partial-write risk.

## Reliability and ethics rules

- Use timeouts on network requests.
- Handle expected request, parsing, validation, and file errors.
- Retry only appropriate temporary failures and use backoff.
- Preserve partial progress when one record or request fails.
- Use sessions when shared headers, cookies, or connection reuse are required.
- Validate and deduplicate records before saving them.
- Identify the educational client with a reasonable `User-Agent`.
- Respect terms of service, robots.txt, privacy, rate limits, and authorization boundaries.
- Never store secrets or private session data in the repository.

## Phase status

- Phase 1 — Python Fundamentals: complete.
- Phase 2 — Web Scraping: complete through Day 65, including the original checkpoint deliverables.
- Phase 3 — Browser Automation: next; Selenium first, followed by Playwright.
