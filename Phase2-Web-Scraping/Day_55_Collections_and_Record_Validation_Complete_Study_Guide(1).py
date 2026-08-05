"""
Day 55 - Collections and Record Validation

Guided revision project:
International Film Festival Listing Auditor

Topics:
- lists, tuples, dictionaries, sets, and nested collections
- HTML extraction with Beautiful Soup
- normalization and type conversion
- missing-value validation
- set-based duplicate detection
- rejection auditing
- searching, updating, copying, and removing collection values
- collection analysis and final integrity checks

Install Beautiful Soup if needed:
    pip install beautifulsoup4
"""

from bs4 import BeautifulSoup


print("Starting International Film Festival Listing Auditor...")


# A tuple is ordered and is useful for values that should remain fixed.
required_fields = (
    "film_id",
    "title",
    "country",
    "runtime_minutes",
    "ticket_price",
)


# Lists preserve insertion order and can contain duplicate values.
valid_films = []
invalid_films = []
duplicate_films = []


# A set stores unique values and supports fast membership checks.
seen_film_ids = set()


# A dictionary connects descriptive keys to values.
audit_counts = {
    "raw_records": 0,
    "valid_records": 0,
    "invalid_records": 0,
    "duplicate_records": 0,
}


print("\n--- COLLECTION SETUP ---")
print("Required fields:", required_fields)
print("Required-field type:", type(required_fields))
print("Valid-film collection:", valid_films)
print("Valid-film collection type:", type(valid_films))
print("Seen film IDs:", seen_film_ids)
print("Seen-ID collection type:", type(seen_film_ids))
print("Audit counts:", audit_counts)
print("Audit-count type:", type(audit_counts))


# Embedded training HTML keeps the lesson focused on collection processing.
training_html = """
<section id="festival-listings">

    <article class="film-card" data-film-id="F101">
        <h2 class="title">  Silent Horizon  </h2>
        <p class="country">Canada</p>
        <span class="runtime">118 minutes</span>
        <span class="ticket-price">$14.50</span>
    </article>

    <article class="film-card" data-film-id="F102">
        <h2 class="title">Midnight Archive</h2>
        <p class="country">France</p>
        <span class="runtime"> 95 minutes </span>
        <span class="ticket-price">$12.00</span>
    </article>

    <article class="film-card" data-film-id="F103">
        <h2 class="title">Northern Signal</h2>
        <p class="country">Norway</p>
        <span class="runtime">104 minutes</span>
        <span class="ticket-price">$11.75</span>
    </article>

    <article class="film-card" data-film-id="F102">
        <h2 class="title">Midnight Archive</h2>
        <p class="country">France</p>
        <span class="runtime">95 minutes</span>
        <span class="ticket-price">$12.00</span>
    </article>

    <article class="film-card" data-film-id="F104">
        <h2 class="title"></h2>
        <p class="country">Japan</p>
        <span class="runtime">110 minutes</span>
        <span class="ticket-price">$13.25</span>
    </article>

    <article class="film-card" data-film-id="F105">
        <h2 class="title">Coastal Memory</h2>
        <p class="country">Portugal</p>
        <span class="runtime">unknown</span>
        <span class="ticket-price">$10.50</span>
    </article>

</section>
"""


# Extract each HTML card into one dictionary inside a list.
soup = BeautifulSoup(training_html, "html.parser")
film_cards = soup.select(".film-card")
audit_counts["raw_records"] = len(film_cards)
raw_films = []

for card in film_cards:
    raw_film = {
        "film_id": card.get("data-film-id"),
        "title": card.select_one(".title").get_text(strip=True),
        "country": card.select_one(".country").get_text(strip=True),
        "runtime_minutes": card.select_one(".runtime").get_text(strip=True),
        "ticket_price": card.select_one(".ticket-price").get_text(strip=True),
    }
    raw_films.append(raw_film)


print("\n--- RAW HTML EXTRACTION ---")
print("Film cards found:", len(film_cards))
print("Raw films collected:", len(raw_films))
print("Raw-record audit count:", audit_counts["raw_records"])
print("\nFirst raw-film dictionary:")
print(raw_films[0])
print("\nFirst film title:", raw_films[0]["title"])
print("First film country:", raw_films[0].get("country"))
print("Missing director:", raw_films[0].get("director", "Not provided"))
print("\nAll extracted films:")

for position, film in enumerate(raw_films, start=1):
    print(
        f"{position}. "
        f"{film['film_id']} | "
        f"{film['title']} | "
        f"{film['country']} | "
        f"{film['runtime_minutes']} | "
        f"{film['ticket_price']}"
    )


# Normalize text and convert runtime/price into useful numeric types.
normalized_films = []

for raw_film in raw_films:
    film_id = raw_film["film_id"].strip().upper()
    title = raw_film["title"].strip()
    country = raw_film["country"].strip().title()

    runtime_text = raw_film["runtime_minutes"].strip().lower()
    runtime_number_text = runtime_text.replace("minutes", "").strip()

    if runtime_number_text.isdigit():
        runtime_minutes = int(runtime_number_text)
    else:
        runtime_minutes = None

    price_text = raw_film["ticket_price"].strip().replace("$", "")

    try:
        ticket_price = float(price_text)
    except ValueError:
        ticket_price = None

    normalized_film = {
        "film_id": film_id,
        "title": title if title else None,
        "country": country,
        "runtime_minutes": runtime_minutes,
        "ticket_price": ticket_price,
    }
    normalized_films.append(normalized_film)


print("\n--- NORMALIZED FILMS ---")
print("Normalized films collected:", len(normalized_films))

for position, film in enumerate(normalized_films, start=1):
    print(
        f"{position}. "
        f"{film['film_id']} | "
        f"{film['title']} | "
        f"{film['country']} | "
        f"{film['runtime_minutes']} | "
        f"{film['ticket_price']}"
    )


print("\n--- TYPE VERIFICATION ---")
first_normalized_film = normalized_films[0]
print("Film ID type:", type(first_normalized_film["film_id"]))
print("Title type:", type(first_normalized_film["title"]))
print("Runtime type:", type(first_normalized_film["runtime_minutes"]))
print("Ticket-price type:", type(first_normalized_film["ticket_price"]))
print("Invalid runtime value:", normalized_films[5]["runtime_minutes"])
print("Missing title value:", normalized_films[4]["title"])


# Classify every normalized record as valid, invalid, or duplicate.
rejection_records = []

for film in normalized_films:
    missing_fields = []

    for field in required_fields:
        if film.get(field) is None or film.get(field) == "":
            missing_fields.append(field)

    if missing_fields:
        invalid_films.append(film)
        rejection_records.append(
            {
                "film_id": film.get("film_id"),
                "status": "invalid",
                "reasons": [
                    f"Missing or invalid field: {field}"
                    for field in missing_fields
                ],
            }
        )
        audit_counts["invalid_records"] += 1
        continue

    film_id = film["film_id"]

    if film_id in seen_film_ids:
        duplicate_films.append(film)
        rejection_records.append(
            {
                "film_id": film_id,
                "status": "duplicate",
                "reasons": ["Film ID already processed"],
            }
        )
        audit_counts["duplicate_records"] += 1
        continue

    seen_film_ids.add(film_id)
    valid_films.append(film)
    audit_counts["valid_records"] += 1


print("\n--- VALIDATION AND DEDUPLICATION ---")
print("Valid films:", len(valid_films))
print("Invalid films:", len(invalid_films))
print("Duplicate films:", len(duplicate_films))
print("Seen valid-film IDs:", seen_film_ids)
print("\nValid-film records:")

for film in valid_films:
    print(
        f"{film['film_id']} | "
        f"{film['title']} | "
        f"{film['country']} | "
        f"{film['runtime_minutes']} minutes | "
        f"${film['ticket_price']:.2f}"
    )

print("\nInvalid-film records:")

for film in invalid_films:
    print(
        f"{film['film_id']} | "
        f"title={film['title']} | "
        f"runtime={film['runtime_minutes']}"
    )

print("\nDuplicate-film records:")

for film in duplicate_films:
    print(f"{film['film_id']} | {film['title']}")

print("\nRejection audit:")

for rejection in rejection_records:
    print(
        f"{rejection['film_id']} | "
        f"{rejection['status']} | "
        f"{', '.join(rejection['reasons'])}"
    )

print("\nUpdated audit counts:")
print(audit_counts)

accounted_records = (
    audit_counts["valid_records"]
    + audit_counts["invalid_records"]
    + audit_counts["duplicate_records"]
)

print(
    "All raw records accounted for:",
    accounted_records == audit_counts["raw_records"],
)


# Copy the list and each nested dictionary before experimenting with changes.
working_films = [film.copy() for film in valid_films]


print("\n--- COLLECTION OPERATIONS ---")
print("Working-film count:", len(working_films))
print("First required field:", required_fields[0])
print("Last required field:", required_fields[-1])
print("F102 already processed:", "F102" in seen_film_ids)


# Search for a dictionary inside the working list.
searched_film = None

for film in working_films:
    if film["film_id"] == "F102":
        searched_film = film
        break

if searched_film is not None:
    print("\nSearch result:")
    print(
        f"{searched_film['film_id']} | "
        f"{searched_film['title']} | "
        f"${searched_film['ticket_price']:.2f}"
    )

    # Add a new key and update an existing value.
    searched_film["screening_status"] = "Evening screening"
    searched_film["ticket_price"] = 12.50
    print("\nUpdated record:")
    print(searched_film)

    # Remove a dictionary key safely and preserve the removed value.
    removed_status = searched_film.pop(
        "screening_status",
        "Status not available",
    )
    print("Removed screening status:", removed_status)
    print("Status still present:", "screening_status" in searched_film)


# Remove a record only from the temporary working list.
removed_film = None

for film in working_films:
    if film["film_id"] == "F103":
        removed_film = film
        working_films.remove(film)
        break

print("\nRemoved working record:")

if removed_film is not None:
    print(removed_film["film_id"], "|", removed_film["title"])

print("Working-film count after removal:", len(working_films))
print("Original valid-film count:", len(valid_films))


# Analyze the protected, verified valid-film collection.
total_runtime = sum(film["runtime_minutes"] for film in valid_films)
average_runtime = total_runtime / len(valid_films)
total_ticket_price = sum(film["ticket_price"] for film in valid_films)
average_ticket_price = total_ticket_price / len(valid_films)

cheapest_film = min(valid_films, key=lambda film: film["ticket_price"])
longest_film = max(valid_films, key=lambda film: film["runtime_minutes"])
countries = {film["country"] for film in valid_films}


print("\n--- FINAL COLLECTION ANALYSIS ---")
print("Valid films analyzed:", len(valid_films))
print("Total runtime:", total_runtime, "minutes")
print(f"Average runtime: {average_runtime:.2f} minutes")
print(f"Average ticket price: ${average_ticket_price:.2f}")
print(
    "Cheapest film:",
    f"{cheapest_film['title']} (${cheapest_film['ticket_price']:.2f})",
)
print(
    "Longest film:",
    f"{longest_film['title']} ({longest_film['runtime_minutes']} minutes)",
)
print("Unique countries:", len(countries))
print("Country collection:", sorted(countries))


print("\n--- FINAL INTEGRITY CHECKS ---")
print("Audit totals match raw records:", accounted_records == len(raw_films))
print("Valid IDs are unique:", len(seen_film_ids) == len(valid_films))
print(
    "All valid records contain required values:",
    all(
        all(film.get(field) is not None for field in required_fields)
        for film in valid_films
    ),
)
print(
    "Working-copy changes preserved original count:",
    len(valid_films) == 3,
)

