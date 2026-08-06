"""
Day 59 — Advanced HTTP and Request Error Handling

Guided revision project: Museum Exhibition Feed Reliability Auditor

Topics covered:
- try, except, else, finally, raise, and exception objects
- specific requests exceptions and RequestException fallback
- raise_for_status(), 4xx errors, and 5xx errors
- empty-body and Content-Type validation
- custom response and parsing exceptions
- request, HTTP, response, parsing, and validation failure separation
- requests.Session() context-manager cleanup

Retries and backoff are intentionally excluded; they belong to Day 60.
"""

import requests
from bs4 import BeautifulSoup


class InvalidResponseError(Exception):
    """Raised when a response arrives but cannot be used as HTML."""


class ParsingError(Exception):
    """Raised when valid HTML does not contain the required element."""


def validate_exhibition(record):
    """Clean and validate one exhibition record."""
    try:
        title = record["title"].strip()
        ticket_price = float(record["ticket_price"])

        if not title:
            raise ValueError("Exhibition title cannot be empty.")

        if ticket_price < 0:
            raise ValueError("Ticket price cannot be negative.")

    except KeyError as error:
        print(f"Missing required field: {error}")
        return None

    except (TypeError, ValueError) as error:
        print(f"Invalid exhibition data: {error}")
        return None

    else:
        cleaned_record = {
            "title": title.title(),
            "ticket_price": ticket_price,
        }
        print(f"Validated exhibition: {cleaned_record['title']}")
        return cleaned_record

    finally:
        print("Validation attempt finished.")


def test_request(label, url, timeout_seconds=5):
    """Demonstrate success, timeout, connection, and HTTP error paths."""
    print(f"\n--- {label.upper()} ---")
    print("Requesting:", url)

    try:
        response = requests.get(url, timeout=timeout_seconds)
        response.raise_for_status()

    except requests.exceptions.Timeout as error:
        print("Failure type: TIMEOUT")
        print("Details:", error)

    except requests.exceptions.ConnectionError as error:
        print("Failure type: CONNECTION ERROR")
        print("Details:", error)

    except requests.exceptions.HTTPError as error:
        status_code = error.response.status_code

        if 400 <= status_code < 500:
            print("Failure type: CLIENT HTTP ERROR")
        elif 500 <= status_code < 600:
            print("Failure type: SERVER HTTP ERROR")

        print("Status code:", status_code)
        print("Details:", error)

    except requests.exceptions.RequestException as error:
        # Keep the general parent exception after all specific exceptions.
        print("Failure type: OTHER REQUEST ERROR")
        print("Details:", error)

    else:
        print("Request successful.")
        print("Status code:", response.status_code)
        print("Content type:", response.headers.get("Content-Type"))
        print("Response size:", len(response.content))

    finally:
        print("Request attempt finished.")


def inspect_html_response(response, required_selector):
    """Validate an HTML response and extract text from one selector."""
    content_type = response.headers.get("Content-Type", "").lower()

    if not response.content:
        raise InvalidResponseError("Response body is empty.")

    if "text/html" not in content_type:
        raise InvalidResponseError(
            f"Expected HTML but received: {content_type or 'unknown'}"
        )

    soup = BeautifulSoup(response.text, "html.parser")
    selected_element = soup.select_one(required_selector)

    if selected_element is None:
        raise ParsingError(
            f"Required selector was not found: {required_selector}"
        )

    return selected_element.get_text(" ", strip=True)


def run_pipeline_test(label, url, required_selector):
    """Run a request-to-parsing pipeline with precise failure categories."""
    print(f"\n--- {label.upper()} ---")
    print("Requesting:", url)

    try:
        with requests.Session() as session:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            extracted_text = inspect_html_response(response, required_selector)

    except requests.exceptions.Timeout as error:
        print("Failure stage: REQUEST")
        print("Failure type: TIMEOUT")
        print("Details:", error)

    except requests.exceptions.ConnectionError as error:
        print("Failure stage: REQUEST")
        print("Failure type: CONNECTION ERROR")
        print("Details:", error)

    except requests.exceptions.HTTPError as error:
        print("Failure stage: HTTP")
        print("Status code:", error.response.status_code)
        print("Details:", error)

    except InvalidResponseError as error:
        print("Failure stage: RESPONSE")
        print("Details:", error)

    except ParsingError as error:
        print("Failure stage: PARSING")
        print("Details:", error)

    except requests.exceptions.RequestException as error:
        print("Failure stage: REQUEST")
        print("Failure type: OTHER REQUEST ERROR")
        print("Details:", error)

    else:
        print("Pipeline successful.")
        print("Extracted text:", extracted_text)

    finally:
        print("Pipeline attempt finished.")


def verify_empty_body_offline():
    """Verify empty-body classification without depending on a live server."""
    print("\n--- OFFLINE EMPTY-BODY VERIFICATION ---")

    empty_response = requests.Response()
    empty_response.status_code = 204
    empty_response._content = b""
    empty_response.headers["Content-Type"] = "text/html"

    try:
        inspect_html_response(empty_response, "body")
    except InvalidResponseError as error:
        print("Failure stage: RESPONSE")
        print("Details:", error)


def main():
    """Run the complete Day 59 guided revision program."""
    print("Starting Museum Exhibition Feed Reliability Auditor...")

    exhibitions = [
        {"title": "  ocean worlds  ", "ticket_price": "18.50"},
        {"title": "future cities"},
        {"title": "ancient navigation", "ticket_price": "free"},
        {"title": "   ", "ticket_price": "12.00"},
        {"title": "modern sculpture", "ticket_price": "-5"},
    ]

    valid_exhibitions = []

    for exhibition in exhibitions:
        print("\nChecking record:", exhibition)
        validated_record = validate_exhibition(exhibition)

        if validated_record is not None:
            valid_exhibitions.append(validated_record)

    print("\n--- VALIDATION SUMMARY ---")
    print("Records checked:", len(exhibitions))
    print("Valid records:", len(valid_exhibitions))
    print("Invalid records:", len(exhibitions) - len(valid_exhibitions))

    for record in valid_exhibitions:
        print(f"{record['title']} | ${record['ticket_price']:.2f}")

    request_tests = [
        ("Successful response", "https://books.toscrape.com/", 10),
        (
            "404 client error",
            "https://books.toscrape.com/missing-page.html",
            10,
        ),
        ("503 server error", "https://httpbin.org/status/503", 10),
        ("Connection failure", "http://127.0.0.1:1", 3),
        ("Timeout test", "https://httpbin.org/delay/3", 0.001),
    ]

    print("\n===== HTTP ERROR-HANDLING TESTS =====")
    for test_label, test_url, test_timeout in request_tests:
        test_request(test_label, test_url, test_timeout)

    pipeline_tests = [
        (
            "Valid HTML and selector",
            "https://books.toscrape.com/",
            "article.product_pod h3 a",
        ),
        ("Unexpected content type", "https://httpbin.org/json", "body"),
        ("Empty response body", "https://httpbin.org/status/204", "body"),
        (
            "Missing HTML element",
            "https://books.toscrape.com/",
            ".exhibition-card",
        ),
    ]

    print("\n===== RESPONSE AND PARSING TESTS =====")
    for pipeline_label, pipeline_url, pipeline_selector in pipeline_tests:
        run_pipeline_test(pipeline_label, pipeline_url, pipeline_selector)

    # This deterministic test still proves the empty-response branch if the
    # live 204 endpoint is slow or unavailable.
    verify_empty_body_offline()


if __name__ == "__main__":
    main()
