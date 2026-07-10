"""
DAY 33 - BEAUTIFULSOUP CSS SELECTORS
====================================
Project: AI Automation Engineer Journey
Phase: Phase 2 - Web Scraping

INTERVIEW-READY DEFINITIONS
---------------------------
CSS Selector:
    A CSS Selector is a pattern used to locate HTML elements based on their
    tag name, class, ID, attributes, or position inside the HTML structure.
    In BeautifulSoup, CSS selectors are used with select() to retrieve all
    matching elements.

select() Method:
    select() is a BeautifulSoup method that searches HTML using CSS selector
    syntax and returns all matching Tag objects as a ResultSet (a list-like
    collection), even when only one element matches.

Tag Selector:
    A tag selector selects HTML elements by tag name.
    Examples: "p", "h1", "a", "img", "div"

Class Selector:
    A class selector selects elements using their class attribute.
    Syntax: ".class_name"
    Example: ".price"

ID Selector:
    An ID selector selects an element using its unique id attribute.
    Syntax: "#id_name"
    Example: "#main-title"

Descendant Selector:
    A descendant selector selects elements located inside another element.
    Syntax: "parent child"
    Example: ".book .title"

Attribute Selector:
    An attribute selector selects elements based on the presence or value of
    an HTML attribute.
    Examples: 'a[href]' and 'a[href="python.html"]'

IMPORTANT SELECTOR PATTERNS
---------------------------
    soup.select("p")                       -> all <p> tags
    soup.select(".price")                  -> all elements with class="price"
    soup.select("#main-title")             -> element with id="main-title"
    soup.select(".book .title")            -> title elements inside books
    soup.select('a[href]')                  -> links that contain href
    soup.select('a[href="python.html"]')    -> exact href match

KEY DIFFERENCE
--------------
    get_text()          -> extracts visible text from a tag
    get("attribute")   -> extracts an HTML attribute value

METHOD COMPARISON
-----------------
    find()      -> returns the first matching Tag or None
    find_all()  -> returns all matches using tag/attribute arguments
    select()    -> returns all matches using CSS selector syntax

PROGRAM ARCHITECTURE
--------------------
    Input HTML
        -> Parse HTML
        -> Select repeating book containers
        -> Loop through each book
        -> Extract title, price, and link
        -> Store each book in a dictionary
        -> Append dictionaries to a list
        -> Display a formatted report

PYTHON FUNDAMENTALS REVISED
---------------------------
    Imports, variables, strings, lists, dictionaries, indexing, for loops,
    methods, key-value access, append(), input/output thinking, and separation
    of responsibilities.
"""

from bs4 import BeautifulSoup


# =============================================================================
# PART 1: SELECTOR DEMONSTRATION HTML
# =============================================================================
html = """
<html>
    <body>
        <h1 id="main-title">Book Catalog</h1>

        <div class="book featured">
            <h2 class="title">Python Automation</h2>
            <p class="price">$25</p>
            <p class="description">A practical Python automation guide.</p>
            <a href="python.html" title="Python book page">View Book</a>
        </div>

        <div class="book">
            <h2 class="title">Web Scraping Basics</h2>
            <p class="price">$30</p>
            <p class="description">Learn structured data extraction.</p>
            <a href="scraping.html" title="Scraping book page">View Book</a>
        </div>

        <footer>
            <h2 class="title">Store Information</h2>
        </footer>
    </body>
</html>
"""


# =============================================================================
# PART 2: CREATE THE BEAUTIFULSOUP OBJECT
# =============================================================================
# BeautifulSoup converts raw HTML into a searchable object.
soup = BeautifulSoup(html, "html.parser")


# =============================================================================
# PART 3: CSS SELECTOR EXAMPLES
# =============================================================================
# 1. TAG SELECTOR
# Select every <p> element.
paragraph_tags = soup.select("p")

# 2. CLASS SELECTOR
# The dot means: search by class.
price_tags = soup.select(".price")

# 3. ID SELECTOR
# The hash symbol means: search by ID.
main_title_tags = soup.select("#main-title")

# 4. DESCENDANT SELECTOR
# Select only titles inside .book containers.
# The footer title is excluded because it is not inside a .book.
book_title_tags = soup.select(".book .title")

# 5. ATTRIBUTE SELECTORS
# Select all links that contain an href attribute.
links_with_href = soup.select('a[href]')

# Select the exact link whose href value is python.html.
python_link_tags = soup.select('a[href="python.html"]')


# =============================================================================
# PART 4: OPTIONAL LEARNING OUTPUT
# =============================================================================
print("========== CSS SELECTOR DEMONSTRATION ==========")
print("Paragraph count       :", len(paragraph_tags))
print("Price count           :", len(price_tags))
print("Main title            :", main_title_tags[0].get_text(strip=True))
print("Book titles found     :", len(book_title_tags))
print("Links with href       :", len(links_with_href))
print("Exact python link     :", python_link_tags[0].get("href"))
print()


# =============================================================================
# PART 5: INTEGRATED REVISION PROJECT - BOOK CATALOG SCRAPER
# =============================================================================
# Step 1: Select all repeating book containers.
books = soup.select(".book")

# Step 2: Create one list to store all extracted book dictionaries.
book_catalog = []

# Step 3: Process one book at a time.
for book in books:
    # Search only inside the current book container.
    title_tags = book.select(".title")
    price_tags = book.select(".price")
    link_tags = book.select("a")

    # select() returns a collection, so [0] accesses the first match.
    # get_text(strip=True) extracts clean visible text.
    title = title_tags[0].get_text(strip=True)
    price = price_tags[0].get_text(strip=True)

    # The URL is stored in href, so get("href") is used instead of get_text().
    link = link_tags[0].get("href")

    # One dictionary represents one complete book record.
    book_data = {
        "title": title,
        "price": price,
        "link": link,
    }

    # Add the current dictionary to the complete catalog.
    book_catalog.append(book_data)


# =============================================================================
# PART 6: DISPLAY THE FINAL REPORT
# =============================================================================
print("========== BOOK CATALOG ==========")
print()

for book_data in book_catalog:
    print("Title :", book_data["title"])
    print("Price :", book_data["price"])
    print("Link  :", book_data["link"])
    print("----------------------------------")


# =============================================================================
# COMMON MISTAKES TO REMEMBER
# =============================================================================
# 1. Wrong: soup.select("<p>")
#    Right: soup.select("p")
#
# 2. Wrong: soup.select("price")
#    Right: soup.select(".price")
#
# 3. Wrong: soup.select("main-title")
#    Right: soup.select("#main-title")
#
# 4. select() returns Tag objects, not plain text.
#    Use get_text() after selecting.
#
# 5. To extract href, src, title, or another attribute, use get().
#
# 6. Keep the storage list outside the loop, otherwise it resets each cycle.
#
# 7. Extract and store inside the first loop; display later in a separate loop.
