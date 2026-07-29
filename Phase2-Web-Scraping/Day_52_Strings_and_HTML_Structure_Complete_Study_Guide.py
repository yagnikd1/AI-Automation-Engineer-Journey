"""
Day 52 - Strings and HTML Structure
Complete Study Guide

Topics:
- String creation, cleaning, indexing, and slicing
- Case conversion, searching, replacement, and validation
- Splitting, joining, f-strings, quotes, escaping, and multiline strings
- HTML structure, nesting, tags, attributes, classes, IDs, and links
- Repeated cards, tables, BeautifulSoup, and parser selection
- Combined HTML extraction and string cleaning

Dependency:
    pip install beautifulsoup4
"""

from bs4 import BeautifulSoup


# Section 1: String indexing and slicing
raw_title = "  Global Automation Conference 2026  "

print("--- ORIGINAL STRING ---")
print(f"Value: {raw_title!r}")
print(f"Type: {type(raw_title)}")
print(f"Length: {len(raw_title)}")

clean_title = raw_title.strip()

print("\n--- CLEANED STRING ---")
print(f"Value: {clean_title}")
print(f"Length: {len(clean_title)}")

print("\n--- STRING INDEXING ---")
print(f"First character: {clean_title[0]}")
print(f"Second character: {clean_title[1]}")
print(f"Last character: {clean_title[-1]}")
print(f"Second-last character: {clean_title[-2]}")

print("\n--- STRING SLICING ---")
print(f"First six characters: {clean_title[0:6]}")
print(f"Characters from index 7 onward: {clean_title[7:]}")
print(f"First ten characters: {clean_title[:10]}")
print(f"Complete copy: {clean_title[:]}")
print(f"Every second character: {clean_title[::2]}")
print(f"Reversed title: {clean_title[::-1]}")


# Section 2: String methods and validation
conference_location = "  berlin, germany  "
conference_code = "GAC2026"
ticket_price = "450"
website = "https://globalautomation.example.com"

clean_location = conference_location.strip()

print("\n--- STRING CASE METHODS ---")
print(f"Original location: {conference_location!r}")
print(f"Uppercase: {clean_location.upper()}")
print(f"Lowercase: {clean_location.lower()}")
print(f"Title case: {clean_location.title()}")
print(f"Capitalized: {clean_location.capitalize()}")

print("\n--- STRING SEARCH METHODS ---")
print(f"Starts with 'Global': {clean_title.startswith('Global')}")
print(f"Ends with '2026': {clean_title.endswith('2026')}")
print(f"Contains 'Automation': {'Automation' in clean_title}")
print(f"Index of 'Conference': {clean_title.find('Conference')}")
print(f"Number of letter 'o': {clean_title.lower().count('o')}")

print("\n--- STRING REPLACEMENT ---")
updated_title = clean_title.replace("2026", "2027")
print(f"Original title: {clean_title}")
print(f"Updated title: {updated_title}")

print("\n--- STRING VALIDATION ---")
print(f"Conference code is alphanumeric: {conference_code.isalnum()}")
print(f"Conference code contains only letters: {conference_code.isalpha()}")
print(f"Ticket price contains only digits: {ticket_price.isdigit()}")
print(f"Location contains only letters: {clean_location.isalpha()}")
print(f"Website starts with HTTPS: {website.startswith('https://')}")

print("\n--- ORIGINAL STRINGS REMAIN UNCHANGED ---")
print(f"Original title: {clean_title}")
print(f"Original location: {conference_location!r}")


# Section 3: Splitting, joining, and formatting
speaker_data = "Morgan Lee|Automation Engineer|Canada"
topic_tags = "Python, Web Scraping, APIs, Automation"
conference_year = 2026
ticket_cost = 450.0
available_seats = 125

print("\n--- SPLITTING STRINGS ---")

speaker_parts = speaker_data.split("|")

print(f"Original speaker data: {speaker_data}")
print(f"Split result: {speaker_parts}")
print(f"Speaker name: {speaker_parts[0]}")
print(f"Speaker role: {speaker_parts[1]}")
print(f"Speaker country: {speaker_parts[2]}")

tag_list = topic_tags.split(", ")

print(f"\nOriginal topic tags: {topic_tags}")
print(f"Topic list: {tag_list}")
print(f"Number of topics: {len(tag_list)}")

print("\n--- JOINING STRINGS ---")

joined_topics = " | ".join(tag_list)
url_slug = "-".join(clean_title.lower().split())

print(f"Topics joined with pipes: {joined_topics}")
print(f"Generated URL slug: {url_slug}")

print("\n--- F-STRING FORMATTING ---")

print(f"Conference: {clean_title}")
print(f"Year: {conference_year}")
print(f"Ticket cost: ${ticket_cost:.2f}")
print(f"Available seats: {available_seats:,}")
print(
    f"{speaker_parts[0]} is an {speaker_parts[1]} "
    f"from {speaker_parts[2]}."
)

print("\n--- QUOTES AND ESCAPING ---")

single_quote_text = "The speaker's session begins at 10:00."
double_quote_text = 'The organizer said, "Registration is open."'
escaped_text = "The organizer said, \"Welcome to the conference.\""
file_location = r"C:\conference\reports\day52"

print(single_quote_text)
print(double_quote_text)
print(escaped_text)
print(f"Raw Windows path: {file_location}")

print("\n--- MULTILINE STRING ---")

conference_description = """Global Automation Conference 2026
Location: Berlin, Germany
Topics: Python, Web Scraping, APIs, Automation"""

print(conference_description)


# Section 4: HTML structure and BeautifulSoup
conference_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Global Automation Conference</title>
</head>
<body>
    <header id="main-header">
        <h1 class="conference-title">
            Global Automation Conference 2026
        </h1>
        <p class="location">Berlin, Germany</p>
    </header>

    <main>
        <section id="conference-details">
            <h2>Conference Details</h2>
            <p class="date">September 15-17, 2026</p>
            <a
                class="registration-link"
                href="https://globalautomation.example.com/register"
            >
                Register Now
            </a>
        </section>

        <section id="featured-speakers">
            <h2>Featured Speakers</h2>

            <article class="speaker-card" data-speaker-id="SP101">
                <h3>Morgan Lee</h3>
                <p class="role">Automation Engineer</p>
                <p class="country">Canada</p>
            </article>

            <article class="speaker-card" data-speaker-id="SP102">
                <h3>Jordan Blake</h3>
                <p class="role">Web Data Specialist</p>
                <p class="country">Germany</p>
            </article>
        </section>

        <section id="ticket-section">
            <h2>Ticket Options</h2>

            <table id="ticket-table">
                <thead>
                    <tr>
                        <th>Ticket</th>
                        <th>Price</th>
                        <th>Available</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Standard</td>
                        <td>$450</td>
                        <td>125</td>
                    </tr>
                    <tr>
                        <td>Premium</td>
                        <td>$700</td>
                        <td>40</td>
                    </tr>
                </tbody>
            </table>
        </section>
    </main>
</body>
</html>
"""

soup = BeautifulSoup(conference_html, "html.parser")

print("\n--- HTML DOCUMENT STRUCTURE ---")
print(f"Root HTML tag: {soup.html.name}")
print(f"Document language: {soup.html.get('lang')}")
print(f"Page title: {soup.title.get_text(strip=True)}")
print(f"Body tag exists: {soup.body is not None}")
print(f"Main tag exists: {soup.main is not None}")

print("\n--- TAGS AND NESTED ELEMENTS ---")

header = soup.header
heading = header.h1
location_element = header.p

print(f"Header tag: {header.name}")
print(f"Heading tag: {heading.name}")
print(f"Conference heading: {heading.get_text(strip=True)}")
print(f"Location: {location_element.get_text(strip=True)}")

print("\n--- ATTRIBUTES, CLASSES, AND IDS ---")
print(f"Header ID: {header.get('id')}")
print(f"Heading classes: {heading.get('class')}")
print(f"Details section ID: {soup.find('section').get('id')}")

registration_link = soup.find("a")

print("\n--- LINK STRUCTURE ---")
print(f"Link text: {registration_link.get_text(strip=True)}")
print(f"Link destination: {registration_link.get('href')}")
print(f"Link classes: {registration_link.get('class')}")

speaker_cards = soup.find_all("article", class_="speaker-card")

print("\n--- REPEATED HTML CARDS ---")
print(f"Number of speaker cards: {len(speaker_cards)}")

for card in speaker_cards:
    speaker_id = card.get("data-speaker-id")
    speaker_name = card.find("h3").get_text(strip=True)
    speaker_role = card.find("p", class_="role").get_text(strip=True)
    speaker_country = card.find("p", class_="country").get_text(strip=True)

    print(
        f"{speaker_id}: {speaker_name} | "
        f"{speaker_role} | {speaker_country}"
    )

ticket_table = soup.find("table", id="ticket-table")
table_rows = ticket_table.find("tbody").find_all("tr")

print("\n--- HTML TABLE STRUCTURE ---")
print(f"Number of ticket rows: {len(table_rows)}")

for row in table_rows:
    cells = row.find_all("td")

    ticket_name = cells[0].get_text(strip=True)
    price = cells[1].get_text(strip=True)
    seats = cells[2].get_text(strip=True)

    print(f"{ticket_name}: {price} | Available seats: {seats}")

print("\n--- PARSER INFORMATION ---")
print("Parser used: html.parser")


# Section 5: Combined string cleaning and HTML extraction
print("\n--- COMBINED CONFERENCE EXTRACTION ---")

extracted_title = soup.h1.get_text(" ", strip=True)
extracted_location = soup.find("p", class_="location").get_text(strip=True)
extracted_date = soup.find("p", class_="date").get_text(strip=True)
extracted_url = registration_link.get("href")

conference_slug = "-".join(extracted_title.lower().split())

speaker_records = []

for card in speaker_cards:
    speaker_record = {
        "speaker_id": card.get("data-speaker-id"),
        "name": card.find("h3").get_text(strip=True),
        "role": card.find("p", class_="role").get_text(strip=True),
        "country": card.find("p", class_="country").get_text(strip=True),
    }

    speaker_records.append(speaker_record)

ticket_records = []

for row in table_rows:
    cells = row.find_all("td")

    ticket_record = {
        "ticket_type": cells[0].get_text(strip=True),
        "price_text": cells[1].get_text(strip=True),
        "available_seats": cells[2].get_text(strip=True),
    }

    ticket_records.append(ticket_record)

conference_record = {
    "title": extracted_title,
    "slug": conference_slug,
    "location": extracted_location,
    "date": extracted_date,
    "registration_url": extracted_url,
    "speakers": speaker_records,
    "tickets": ticket_records,
}

print(f"Title: {conference_record['title']}")
print(f"Slug: {conference_record['slug']}")
print(f"Location: {conference_record['location']}")
print(f"Date: {conference_record['date']}")
print(f"Registration URL: {conference_record['registration_url']}")
print(f"Speaker records: {len(conference_record['speakers'])}")
print(f"Ticket records: {len(conference_record['tickets'])}")

print("\n--- STRUCTURED SPEAKER RECORDS ---")

for speaker in conference_record["speakers"]:
    print(
        f"{speaker['speaker_id']} | "
        f"{speaker['name']} | "
        f"{speaker['role']} | "
        f"{speaker['country']}"
    )

print("\n--- STRUCTURED TICKET RECORDS ---")

for ticket in conference_record["tickets"]:
    clean_price = ticket["price_text"].replace("$", "")
    formatted_price = f"${float(clean_price):,.2f}"

    print(
        f"{ticket['ticket_type']} | "
        f"{formatted_price} | "
        f"{ticket['available_seats']} seats"
    )

print("\n--- FINAL DAY 52 SUMMARY ---")

summary = (
    f"{conference_record['title']} takes place in "
    f"{conference_record['location']} on {conference_record['date']}. "
    f"It has {len(speaker_records)} featured speakers and "
    f"{len(ticket_records)} ticket options."
)

print(summary)
