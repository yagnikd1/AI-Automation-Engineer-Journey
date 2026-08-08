"""
Day 62 - Systematic Debugging
International Science Conference Listing Debugger

This study guide demonstrates a complete debugging workflow:
1. Reproduce a bug consistently.
2. Isolate the failing pipeline stage.
3. Inspect runtime values and types.
4. Trace program flow.
5. Test a component independently.
6. Correct and verify the defect.
7. Run regression checks.

Dependency:
    pip install beautifulsoup4
"""

import logging
import traceback

from bs4 import BeautifulSoup


logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s | %(message)s",
)


CONFERENCE_HTML = """
<section id="conference-listings">
    <article class="conference" data-id="SC-101">
        <h2 class="title">Global Robotics Forum</h2>
        <span class="country">Germany</span>
        <span class="ticket-price">$1,120.00</span>
    </article>

    <article class="conference" data-id="SC-102">
        <h2 class="title">Ocean Science Summit</h2>
        <span class="country">Portugal</span>
    </article>
</section>
"""


def buggy_clean_price(raw_price):
    """Original faulty cleaner: it forgets to remove commas."""

    if raw_price is None:
        return None

    cleaned_price = raw_price.replace("$", "").strip()
    return float(cleaned_price)


def reproduce_bug():
    """Run the same input twice and confirm the same exception occurs."""

    print("\n--- 1. REPRODUCE THE BUG CONSISTENTLY ---")

    for attempt in range(1, 3):
        try:
            buggy_clean_price("$1,120.00")
        except ValueError as error:
            print(f"Attempt {attempt}: REPRODUCED -> {error}")


def isolate_and_trace_bug():
    """Expose the failing value, type, function, and traceback path."""

    print("\n--- 2-4. ISOLATE, INSPECT, AND TRACE ---")

    raw_price = "$1,120.00"
    cleaned_price = raw_price.replace("$", "").strip()

    print(f"Raw value: {raw_price!r}")
    print(f"Raw type: {type(raw_price).__name__}")
    print(f"Cleaned value before conversion: {cleaned_price!r}")
    print(f"Cleaned type: {type(cleaned_price).__name__}")
    print("Failing pipeline stage: cleaning/conversion")

    try:
        buggy_clean_price(raw_price)
    except ValueError:
        print("Traceback path:")
        traceback.print_exc(limit=2)


def clean_price(raw_price):
    """Convert a price string into a float after removing $ and commas."""

    logging.debug(
        "clean_price input: value=%r | type=%s",
        raw_price,
        type(raw_price).__name__,
    )

    if raw_price is None:
        logging.debug("clean_price returning None")
        return None

    cleaned_price = (
        raw_price
        .replace("$", "")
        .replace(",", "")
        .strip()
    )

    logging.debug(
        "Before float conversion: value=%r | type=%s",
        cleaned_price,
        type(cleaned_price).__name__,
    )

    ticket_price = float(cleaned_price)

    logging.debug(
        "clean_price output: value=%r | type=%s",
        ticket_price,
        type(ticket_price).__name__,
    )

    return ticket_price


def test_clean_price():
    """Test the corrected component and its earlier working behaviours."""

    test_cases = [
        ("$120.00", 120.0, "ordinary price regression check"),
        ("$1,120.00", 1120.0, "corrected comma-formatted price"),
        (None, None, "missing-price regression check"),
    ]

    print("\n--- 5-7. COMPONENT AND REGRESSION TESTS ---")

    for raw_value, expected_result, purpose in test_cases:
        actual_result = clean_price(raw_value)

        assert actual_result == expected_result, (
            f"Expected {expected_result!r}, "
            f"but received {actual_result!r}"
        )

        print(
            "PASS:",
            repr(raw_value),
            "->",
            actual_result,
            f"({purpose})",
        )


def parse_conferences(html):
    """Extract conference records from controlled HTML."""

    soup = BeautifulSoup(html, "html.parser")
    conference_cards = soup.select("article.conference")

    logging.info("Conference cards found: %d", len(conference_cards))

    records = []

    for card in conference_cards:
        conference_id = card.get("data-id")

        title_element = card.select_one(".title")
        country_element = card.select_one(".country")
        price_element = card.select_one(".ticket-price")

        title = (
            title_element.get_text(strip=True)
            if title_element
            else None
        )
        country = (
            country_element.get_text(strip=True)
            if country_element
            else None
        )
        raw_price = (
            price_element.get_text(strip=True)
            if price_element
            else None
        )

        ticket_price = clean_price(raw_price)

        record = {
            "conference_id": conference_id,
            "title": title,
            "country": country,
            "ticket_price": ticket_price,
        }

        logging.debug("Parsed record: %s", record)
        records.append(record)

    return records


def validate_conference(record):
    """Return True only when all required values are valid."""

    required_fields = (
        "conference_id",
        "title",
        "country",
        "ticket_price",
    )

    for field in required_fields:
        if record.get(field) is None:
            logging.warning(
                "Rejected %s: missing %s",
                record.get("conference_id"),
                field,
            )
            return False

    if record["ticket_price"] < 0:
        logging.warning(
            "Rejected %s: ticket price cannot be negative",
            record["conference_id"],
        )
        return False

    return True


def run_corrected_pipeline():
    """Run parsing, cleaning, validation, and output after the correction."""

    print("\n--- CORRECTED FULL PIPELINE ---")

    parsed_records = parse_conferences(CONFERENCE_HTML)
    valid_records = []

    for conference in parsed_records:
        if validate_conference(conference):
            valid_records.append(conference)

    print("\n--- RESULTS ---")
    print("Parsed records:", len(parsed_records))
    print("Valid records:", len(valid_records))

    for conference in valid_records:
        print(
            conference["conference_id"],
            "|",
            conference["title"],
            "|",
            conference["country"],
            "|",
            conference["ticket_price"],
        )

    assert len(parsed_records) == 2
    assert len(valid_records) == 1
    assert valid_records[0]["ticket_price"] == 1120.0

    print("Full-pipeline verification: PASS")


def main():
    """Execute the complete Day 62 systematic debugging demonstration."""

    print("Day 62 - Systematic Debugging")
    print("International Science Conference Listing Debugger")

    reproduce_bug()
    isolate_and_trace_bug()
    test_clean_price()
    run_corrected_pipeline()

    print("\nAll Day 62 debugging checks passed.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, AttributeError, AssertionError) as error:
        logging.exception("Day 62 program failed: %s", error)
