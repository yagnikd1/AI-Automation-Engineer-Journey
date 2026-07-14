"""
Day 37 - BeautifulSoup DOM Tree Navigation

Topics covered:
1. Combined Python fundamentals + BeautifulSoup revision
2. CSS selectors: select() and select_one()
3. Text extraction and cleaning with get_text(strip=True)
4. Lists, dictionaries, loops, functions, and try/except
5. DOM tree relationships: parent, child, sibling, ancestor
6. Moving upward with .parent and .parent.parent
7. Moving downward with .children and .contents
8. Moving sideways with .next_sibling and .previous_sibling
9. Whitespace text nodes such as "\n"
10. Reliable forward/backward traversal with .find_next() and .find_previous()
"""

from bs4 import BeautifulSoup
from bs4.element import Tag


# ---------------------------------------------------------------------
# PART 1: COMBINED REVISION PROGRAM
# Python fundamentals + BeautifulSoup selectors
# ---------------------------------------------------------------------

EMPLOYEE_HTML = """
<html>
<body>

<div class="employee">
    <h2 class="name">Alice Johnson</h2>
    <p class="department">IT</p>
    <span class="salary">$5500</span>
</div>

<div class="employee">
    <h2 class="name">Michael Brown</h2>
    <p class="department">HR</p>
    <span class="salary">$4200</span>
</div>

<div class="employee">
    <h2 class="name">Emma Wilson</h2>
    <p class="department">Finance</p>
    <span class="salary">$6100</span>
</div>

<div class="employee">
    <h2 class="name">Daniel Carter</h2>
    <p class="department">Support</p>
    <span class="salary">N/A</span>
</div>

</body>
</html>
"""


def clean_salary(salary_text: str) -> int:
    """Convert salary text such as '$5500' into an integer.

    Invalid values such as 'N/A' return 0 so the scraper can continue.
    """
    try:
        return int(salary_text.replace("$", "").strip())
    except (ValueError, AttributeError):
        return 0


def scrape_employees(html: str) -> list[dict]:
    """Extract employee records from HTML and return a list of dictionaries."""
    soup = BeautifulSoup(html, "html.parser")
    employees = []

    # select() returns all matching elements as a ResultSet-like collection.
    cards = soup.select(".employee")

    for card in cards:
        # Search inside the current card, not across the entire document.
        name_tag = card.select_one(".name")
        department_tag = card.select_one(".department")
        salary_tag = card.select_one(".salary")

        # Defensive extraction prevents AttributeError if a tag is missing.
        name = name_tag.get_text(strip=True) if name_tag else "Unknown"
        department = (
            department_tag.get_text(strip=True) if department_tag else "Unknown"
        )
        salary_text = salary_tag.get_text(strip=True) if salary_tag else ""

        employee = {
            "name": name,
            "department": department,
            "salary": clean_salary(salary_text),
        }

        employees.append(employee)

    return employees


def print_employee_report(employees: list[dict]) -> None:
    """Print a formatted report from a list of employee dictionaries."""
    print("\nEMPLOYEE REPORT")
    print("-" * 46)

    for employee in employees:
        print(f"Name       : {employee['name']}")
        print(f"Department : {employee['department']}")
        print(f"Salary     : ${employee['salary']}")
        print("-" * 46)


# ---------------------------------------------------------------------
# PART 2: DOM TREE NAVIGATION
# ---------------------------------------------------------------------

NAVIGATION_HTML = """
<html>
<body>
    <section class="catalog">
        <h1>Technology Products</h1>

        <div class="product">
            <h2 class="title">Laptop</h2>
            <p class="description">Portable computer</p>
            <span class="price">$1200</span>
            <button>Buy Now</button>
        </div>

        <div class="product">
            <h2 class="title">Tablet</h2>
            <p class="description">Touchscreen device</p>
            <span class="price">$650</span>
            <button>Buy Now</button>
        </div>
    </section>
</body>
</html>
"""


def print_tag(label: str, value) -> None:
    """Print a readable label and the selected BeautifulSoup value."""
    print(f"\n{label}")
    print("-" * len(label))
    print(value)


def demonstrate_parent_navigation(soup: BeautifulSoup) -> None:
    """Demonstrate moving upward through the DOM tree."""
    title = soup.select_one(".title")

    if title is None:
        print("Title tag was not found.")
        return

    # .parent moves up one level.
    product = title.parent

    # BeautifulSoup has no .grandparent property.
    # Chaining .parent.parent moves up two levels.
    catalog = title.parent.parent

    print_tag("Current tag", title)
    print_tag("Immediate parent: title.parent", product)
    print_tag("Grandparent: title.parent.parent", catalog)

    # Once we reach the correct parent container, search inside it.
    price_tag = product.select_one(".price") if isinstance(product, Tag) else None
    if price_tag:
        print(f"\nPrice found inside the parent container: {price_tag.get_text(strip=True)}")


def demonstrate_child_navigation(soup: BeautifulSoup) -> None:
    """Demonstrate moving downward with .children and .contents."""
    product = soup.select_one(".product")

    if product is None:
        print("Product tag was not found.")
        return

    print("\nIMMEDIATE CHILD TAGS USING .children")
    print("-" * 38)

    # .children returns an iterator.
    # Formatted HTML also contains whitespace text nodes, so keep only Tag objects.
    for child in product.children:
        if isinstance(child, Tag):
            print(f"{child.name}: {child.get_text(' ', strip=True)}")

    print("\nIMMEDIATE CHILD TAGS USING .contents")
    print("-" * 38)

    # .contents returns a Python list.
    tag_children = [item for item in product.contents if isinstance(item, Tag)]

    for index, child in enumerate(tag_children):
        print(f"Index {index}: {child.name} -> {child.get_text(' ', strip=True)}")

    if len(tag_children) > 1:
        print(f"\nSecond child by index: {tag_children[1]}")


def demonstrate_sibling_navigation(soup: BeautifulSoup) -> None:
    """Demonstrate sideways navigation and the whitespace-node problem."""
    title = soup.select_one(".title")
    price = soup.select_one(".price")

    if title is None or price is None:
        print("Required tags were not found.")
        return

    print_tag("title.next_sibling (may be a whitespace text node)", repr(title.next_sibling))
    print_tag(
        "price.previous_sibling (may be a whitespace text node)",
        repr(price.previous_sibling),
    )

    # find_next() and find_previous() skip whitespace and search for tags.
    print_tag("title.find_next()", title.find_next())
    print_tag("title.find_next('span')", title.find_next("span"))
    print_tag("price.find_previous()", price.find_previous())
    print_tag("price.find_previous('h2')", price.find_previous("h2"))


def demonstrate_repeated_forward_search(soup: BeautifulSoup) -> None:
    """Show how to continue moving through repeated matching tags."""
    title = soup.select_one(".title")

    if title is None:
        return

    first_next = title.find_next("p")
    second_next = first_next.find_next("p") if first_next else None

    print("\nREPEATED FORWARD SEARCH")
    print("-" * 23)
    print("First <p> after the first title:", first_next.get_text(strip=True) if first_next else None)
    print("Next <p> after that:", second_next.get_text(strip=True) if second_next else None)


def main() -> None:
    """Run all Day 37 examples."""
    employees = scrape_employees(EMPLOYEE_HTML)
    print_employee_report(employees)

    soup = BeautifulSoup(NAVIGATION_HTML, "html.parser")

    print("\n\nBEAUTIFULSOUP DOM TREE NAVIGATION")
    print("=" * 46)

    demonstrate_parent_navigation(soup)
    demonstrate_child_navigation(soup)
    demonstrate_sibling_navigation(soup)
    demonstrate_repeated_forward_search(soup)

    print("\n\nDAY 37 QUICK REFERENCE")
    print("=" * 46)
    print(".parent                  -> move up one level")
    print(".parent.parent           -> move up two levels (grandparent)")
    print(".children                -> iterator of immediate children")
    print(".contents                -> list of immediate children")
    print(".next_sibling            -> immediate next sibling/node")
    print(".previous_sibling        -> immediate previous sibling/node")
    print(".find_next()             -> next HTML element in document order")
    print(".find_next('tag')        -> next matching tag")
    print(".find_previous()         -> previous HTML element in document order")
    print(".find_previous('tag')    -> previous matching tag")
    print("\nPreferred real-world choice: find_next()/find_previous()")
    print("Reason: formatted HTML often contains whitespace text nodes such as '\\n'.")


if __name__ == "__main__":
    main()
