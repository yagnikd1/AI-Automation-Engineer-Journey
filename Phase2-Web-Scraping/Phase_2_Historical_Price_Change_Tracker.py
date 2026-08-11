"""Phase 2 checkpoint: store prices, detect changes, and create alerts.

Safe deterministic demonstration:
    python Phase_2_Historical_Price_Change_Tracker.py --demo
    python Phase_2_Historical_Price_Change_Tracker.py --demo-change

The first command stores the baseline. The second simulates a later permitted
observation and writes a price-change alert. State is kept in JSON so the
historical comparison survives separate program runs.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

import requests
from bs4 import BeautifulSoup


STATE_FILE = Path("price_tracker_state.json")
ALERT_FILE = Path("price_change_alerts.jsonl")
TIMEOUT_SECONDS = 15


@dataclass(frozen=True)
class ProductObservation:
    product_id: str
    name: str
    url: str
    currency: str
    price: str
    checked_at: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_price(raw_price: str) -> Decimal:
    cleaned = "".join(character for character in raw_price if character.isdigit() or character in ".-")
    try:
        price = Decimal(cleaned)
    except InvalidOperation as error:
        raise ValueError(f"Could not parse price: {raw_price!r}") from error
    if price < 0:
        raise ValueError("Price cannot be negative.")
    return price.quantize(Decimal("0.01"))


def load_state(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as state_file:
        data = json.load(state_file)
    if not isinstance(data, dict):
        raise ValueError("The state file must contain a JSON object.")
    return data


def save_state(state: dict[str, dict], path: Path) -> None:
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    with temporary_path.open("w", encoding="utf-8") as state_file:
        json.dump(state, state_file, indent=2, ensure_ascii=False)
    temporary_path.replace(path)


def write_alert(alert: dict, path: Path) -> None:
    with path.open("a", encoding="utf-8") as alert_file:
        alert_file.write(json.dumps(alert, ensure_ascii=False) + "\n")


def compare_and_store(observation: ProductObservation, state_path: Path, alert_path: Path) -> dict | None:
    state = load_state(state_path)
    previous = state.get(observation.product_id)
    alert = None

    if previous is not None:
        previous_price = Decimal(previous["price"])
        current_price = Decimal(observation.price)
        if current_price != previous_price:
            difference = current_price - previous_price
            alert = {
                "type": "price_change",
                "product_id": observation.product_id,
                "name": observation.name,
                "url": observation.url,
                "currency": observation.currency,
                "old_price": f"{previous_price:.2f}",
                "new_price": f"{current_price:.2f}",
                "difference": f"{difference:+.2f}",
                "direction": "increased" if difference > 0 else "decreased",
                "detected_at": observation.checked_at,
            }
            write_alert(alert, alert_path)

    state[observation.product_id] = asdict(observation)
    save_state(state, state_path)
    return alert


def scrape_permitted_page(url: str, name_selector: str, price_selector: str, currency: str) -> ProductObservation:
    """Fetch a permitted public page using user-supplied CSS selectors."""
    headers = {"User-Agent": "Phase2PriceTracker/1.0 (educational project)"}
    response = requests.get(url, headers=headers, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    name_element = soup.select_one(name_selector)
    price_element = soup.select_one(price_selector)
    if name_element is None or price_element is None:
        raise ValueError("The supplied CSS selector did not match the required element.")
    price = normalize_price(price_element.get_text(" ", strip=True))
    return ProductObservation(
        product_id=url,
        name=name_element.get_text(" ", strip=True),
        url=url,
        currency=currency.upper(),
        price=f"{price:.2f}",
        checked_at=utc_now(),
    )


def demo_observation(changed: bool) -> ProductObservation:
    return ProductObservation(
        product_id="demo-headphones-001",
        name="Studio Reference Headphones",
        url="https://example.com/permitted-demo-product",
        currency="USD",
        price="89.00" if changed else "99.00",
        checked_at=utc_now(),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Historical price-change tracker")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--demo", action="store_true", help="Store the demo baseline price")
    mode.add_argument("--demo-change", action="store_true", help="Store a changed demo price")
    mode.add_argument("--url", help="Permitted product-page URL")
    parser.add_argument("--name-selector", help="CSS selector for the product name")
    parser.add_argument("--price-selector", help="CSS selector for the product price")
    parser.add_argument("--currency", default="USD", help="ISO-style currency code")
    parser.add_argument("--state", type=Path, default=STATE_FILE)
    parser.add_argument("--alerts", type=Path, default=ALERT_FILE)
    arguments = parser.parse_args()

    try:
        if arguments.demo or arguments.demo_change:
            observation = demo_observation(changed=arguments.demo_change)
        else:
            if not arguments.name_selector or not arguments.price_selector:
                parser.error("--url requires --name-selector and --price-selector")
            observation = scrape_permitted_page(
                arguments.url,
                arguments.name_selector,
                arguments.price_selector,
                arguments.currency,
            )
        alert = compare_and_store(observation, arguments.state, arguments.alerts)
    except (OSError, ValueError, json.JSONDecodeError, requests.RequestException) as error:
        parser.exit(1, f"Tracker failed: {error}\n")

    print(f"Stored {observation.name}: {observation.currency} {observation.price}")
    if alert:
        print(
            f"ALERT: price {alert['direction']} from {alert['old_price']} "
            f"to {alert['new_price']} ({alert['difference']})."
        )
        print(f"Alert log: {arguments.alerts.resolve()}")
    else:
        print("No price change detected; baseline/current state saved.")


if __name__ == "__main__":
    main()
