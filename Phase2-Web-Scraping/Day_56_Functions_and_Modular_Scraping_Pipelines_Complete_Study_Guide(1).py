"""
Day 56 - Functions and Modular Scraping Pipelines

Guided revision program: World Heritage Site Listing Auditor

Topics covered:
- Defining and calling functions
- Parameters, positional arguments, keyword arguments, and defaults
- return versus print
- Local and global scope
- Type hints and docstrings
- Returning collections
- Functions calling other functions
- Early returns
- Separate collection, parsing, cleaning, validation, deduplication,
  analysis, and reporting responsibilities
- A complete function-based scraping pipeline

This program uses simulated HTML so it can be run safely and repeatedly
without making a network request.
"""

from bs4 import BeautifulSoup


SOURCE_URL = "https://example.com/heritage-sites"
AUDIT_CATEGORY = "World Heritage Sites"


SIMULATED_HTML = """
<section id="heritage-listings">
    <article class="site-card">
        <h2 class="site-name">Petra</h2>
        <p class="country">Jordan</p>
        <span class="year">1985</span>
    </article>

    <article class="site-card">
        <h2 class="site-name">Acropolis of Athens</h2>
        <p class="country">Greece</p>
        <span class="year">1987</span>
    </article>

    <article class="site-card">
        <h2 class="site-name">Petra</h2>
        <p class="country">Jordan</p>
        <span class="year">1985</span>
    </article>

    <article class="site-card">
        <h2 class="site-name">Historic Sanctuary</h2>
        <span class="year">Unknown</span>
    </article>
</section>
"""


def show_program_name() -> None:
    """Display the program name."""

    print("World Heritage Site Listing Auditor")


def show_source(source_url: str) -> None:
    """Display the data-source URL."""

    print(f"Source: {source_url}")


def create_site_label(
    site_name: str,
    country: str = "Country unavailable"
) -> str:
    """Return a cleaned display label for one site."""

    cleaned_name = site_name.strip().title()
    cleaned_country = country.strip().title()
    return f"{cleaned_name} | {cleaned_country}"


def print_site_status(site_name: str) -> None:
    """Print a site status without returning a reusable string."""

    print(f"{site_name}: Listing checked")


def return_site_status(site_name: str) -> str:
    """Return a reusable site-status string."""

    return f"{site_name}: Listing checked"


def create_audit_message(site_name: str) -> str:
    """Demonstrate access to global and local variables."""

    local_status = "Validated"
    return f"{AUDIT_CATEGORY} | {site_name} | {local_status}"


def collect_site_records() -> list[dict[str, str]]:
    """Return simulated World Heritage Site records."""

    return [
        {"name": "  petra  ", "country": "jordan", "year": "1985"},
        {
            "name": "acropolis of athens",
            "country": "greece",
            "year": "1987"
        },
        {
            "name": "historic sanctuary",
            "country": "",
            "year": "unknown"
        }
    ]


def clean_site_record(record: dict[str, str]) -> dict[str, str]:
    """Clean the fields of one heritage-site record."""

    return {
        "name": record.get("name", "").strip().title(),
        "country": record.get("country", "").strip().title(),
        "year": record.get("year", "").strip()
    }


def validate_site_record(
    record: dict[str, str]
) -> tuple[bool, str]:
    """Validate one cleaned heritage-site record."""

    if not record["name"]:
        return False, "Missing site name"

    if not record["country"]:
        return False, "Missing country"

    if not record["year"].isdigit():
        return False, "Invalid inscription year"

    return True, "Valid record"


def prepare_site_record(
    raw_record: dict[str, str]
) -> dict[str, str] | None:
    """Clean and validate one raw record."""

    cleaned_record = clean_site_record(raw_record)
    is_valid, validation_message = validate_site_record(cleaned_record)

    if not is_valid:
        site_name = cleaned_record["name"] or "Unnamed Site"
        print(f"Rejected: {site_name} | {validation_message}")
        return None

    return cleaned_record


def get_element_text(card, selector: str) -> str:
    """Return an element's text or an empty string when missing."""

    element = card.select_one(selector)

    if element is None:
        return ""

    return element.get_text(strip=True)


def parse_site_cards(html: str) -> list[dict[str, str]]:
    """Parse heritage-site records from HTML."""

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select(".site-card")
    parsed_records = []

    for card in cards:
        record = {
            "name": get_element_text(card, ".site-name"),
            "country": get_element_text(card, ".country"),
            "year": get_element_text(card, ".year")
        }
        parsed_records.append(record)

    return parsed_records


def remove_duplicate_sites(
    records: list[dict[str, str]]
) -> list[dict[str, str]]:
    """Return records with duplicate sites removed."""

    unique_records = []
    seen_sites: set[tuple[str, str]] = set()

    for record in records:
        identity = (
            record["name"].casefold(),
            record["country"].casefold()
        )

        if identity in seen_sites:
            print(
                f"Duplicate skipped: "
                f"{record['name']} | {record['country']}"
            )
            continue

        seen_sites.add(identity)
        unique_records.append(record)

    return unique_records


def analyze_site_records(
    records: list[dict[str, str]]
) -> dict[str, int | str]:
    """Calculate summary information for valid heritage sites."""

    if not records:
        return {
            "total_sites": 0,
            "countries": 0,
            "earliest_year": "Unavailable",
            "latest_year": "Unavailable"
        }

    countries = {record["country"].casefold() for record in records}
    inscription_years = [int(record["year"]) for record in records]

    return {
        "total_sites": len(records),
        "countries": len(countries),
        "earliest_year": min(inscription_years),
        "latest_year": max(inscription_years)
    }


def display_analysis_report(analysis: dict[str, int | str]) -> None:
    """Display the heritage-site analysis report."""

    print("\n===== HERITAGE SITE ANALYSIS =====")
    print(f"Total unique valid sites: {analysis['total_sites']}")
    print(f"Countries represented: {analysis['countries']}")
    print(f"Earliest inscription year: {analysis['earliest_year']}")
    print(f"Latest inscription year: {analysis['latest_year']}")


def collect_listing_html(source_url: str) -> str:
    """Return simulated HTML collected from a listing page."""

    print(f"Collecting page: {source_url}")
    return SIMULATED_HTML


def run_heritage_site_pipeline(
    source_url: str
) -> list[dict[str, str]]:
    """Run the complete heritage-site auditing pipeline."""

    print("\n===== COMPLETE FUNCTION-BASED PIPELINE =====")

    page_html = collect_listing_html(source_url)
    parsed_records = parse_site_cards(page_html)
    valid_records = []

    for parsed_record in parsed_records:
        prepared_record = prepare_site_record(parsed_record)

        if prepared_record is not None:
            valid_records.append(prepared_record)

    unique_records = remove_duplicate_sites(valid_records)
    analysis = analyze_site_records(unique_records)

    print(f"Parsed records: {len(parsed_records)}")
    print(f"Valid records: {len(valid_records)}")
    print(f"Unique records: {len(unique_records)}")
    display_analysis_report(analysis)

    return unique_records


def demonstrate_function_fundamentals() -> None:
    """Run the guided examples from the Day 56 lesson."""

    show_program_name()
    show_source(SOURCE_URL)

    site_1_label = create_site_label("  petra  ", "jordan")
    site_2_label = create_site_label(
        site_name="acropolis of athens",
        country="greece"
    )
    site_3_label = create_site_label("historic sanctuary")

    print("\n===== FUNCTION RESULTS =====")
    print(f"Site 1: {site_1_label}")
    print(f"Site 2: {site_2_label}")
    print(f"Site 3: {site_3_label}")

    printed_result = print_site_status("Petra")
    returned_result = return_site_status("Acropolis of Athens")

    print("\n===== PRINT VERSUS RETURN =====")
    print(f"Value from print function: {printed_result}")
    print(f"Value from return function: {returned_result}")

    audit_message = create_audit_message("Petra")
    print("\n===== VARIABLE SCOPE =====")
    print(f"Global variable: {AUDIT_CATEGORY}")
    print(f"Returned message: {audit_message}")

    collected_records = collect_site_records()
    print("\n===== COLLECTION FUNCTION =====")
    print(f"Returned type: {type(collected_records)}")
    print(f"Records collected: {len(collected_records)}")
    print(f"First record: {collected_records[0]}")
    print(f"Function documentation: {collect_site_records.__doc__}")

    prepared_records = []
    print("\n===== CLEANING AND VALIDATION FUNCTIONS =====")

    for raw_record in collected_records:
        prepared_record = prepare_site_record(raw_record)

        if prepared_record is not None:
            prepared_records.append(prepared_record)
            print(f"Accepted: {prepared_record}")

    print(f"Valid prepared records: {len(prepared_records)}")


def main() -> None:
    """Run the Day 56 demonstrations and final modular pipeline."""

    demonstrate_function_fundamentals()

    final_site_records = run_heritage_site_pipeline(SOURCE_URL)

    print("\n===== PIPELINE RETURN VALUE =====")
    print(f"Returned type: {type(final_site_records)}")
    print(f"Returned records: {len(final_site_records)}")


if __name__ == "__main__":
    main()
