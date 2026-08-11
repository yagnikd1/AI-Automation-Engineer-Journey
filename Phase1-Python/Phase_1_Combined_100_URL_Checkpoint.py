"""Phase 1 checkpoint: process 100 URLs without stopping on failures.

Usage:
    python Phase_1_Combined_100_URL_Checkpoint.py urls.txt

The input file must contain one HTTP or HTTPS URL per line. Blank lines and
lines beginning with ``#`` are ignored. The program processes at most 100
URLs and writes one result row per URL to ``phase_1_100_url_results.csv``.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


OUTPUT_FILE = Path("phase_1_100_url_results.csv")
MAX_URLS = 100
TIMEOUT_SECONDS = 15


def load_urls(file_path: Path) -> list[str]:
    """Return the first 100 non-empty, non-comment lines."""
    with file_path.open("r", encoding="utf-8") as source_file:
        urls = [
            line.strip()
            for line in source_file
            if line.strip() and not line.lstrip().startswith("#")
        ]
    return urls[:MAX_URLS]


def is_http_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def inspect_url(session: requests.Session, position: int, url: str) -> dict:
    """Inspect one URL and always return a result dictionary."""
    result = {
        "position": position,
        "requested_url": url,
        "final_url": "",
        "status_code": "",
        "content_type": "",
        "page_title": "",
        "word_count": 0,
        "result": "failed",
        "error": "",
    }

    if not is_http_url(url):
        result["error"] = "Invalid HTTP/HTTPS URL"
        return result

    try:
        response = session.get(url, timeout=TIMEOUT_SECONDS)
        result["final_url"] = response.url
        result["status_code"] = response.status_code
        result["content_type"] = response.headers.get("Content-Type", "")
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        result["page_title"] = soup.title.get_text(strip=True) if soup.title else ""
        result["word_count"] = len(soup.get_text(" ", strip=True).split())
        result["result"] = "success"
    except requests.RequestException as error:
        result["error"] = f"{type(error).__name__}: {error}"

    return result


def export_results(results: list[dict], output_path: Path) -> None:
    fieldnames = list(results[0].keys())
    with output_path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def run(input_path: Path, output_path: Path = OUTPUT_FILE) -> list[dict]:
    urls = load_urls(input_path)
    if not urls:
        raise ValueError("The input file does not contain any URLs.")

    session = requests.Session()
    session.headers.update(
        {"User-Agent": "Phase1Checkpoint/1.0 (educational URL auditor)"}
    )

    try:
        results = [
            inspect_url(session, position, url)
            for position, url in enumerate(urls, start=1)
        ]
    finally:
        session.close()

    export_results(results, output_path)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect up to 100 URLs and combine the results in one CSV file."
    )
    parser.add_argument("input_file", type=Path, help="Text file containing one URL per line")
    parser.add_argument("--output", type=Path, default=OUTPUT_FILE, help="Output CSV path")
    arguments = parser.parse_args()

    try:
        results = run(arguments.input_file, arguments.output)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Checkpoint failed: {error}\n")

    successful = sum(item["result"] == "success" for item in results)
    failed = len(results) - successful
    print(f"URLs processed: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Combined CSV: {arguments.output.resolve()}")


if __name__ == "__main__":
    main()
