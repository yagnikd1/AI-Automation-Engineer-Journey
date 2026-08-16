"""
DAY 69 - CSS SELECTORS
Phase 3: Browser Automation

Program: CSS Selector Equipment Inspector

Learning goals
--------------
1. Locate elements with tag, ID, and class selectors.
2. Combine multiple classes on the same element.
3. Use attribute selectors: existence, exact, starts-with, ends-with, contains.
4. Distinguish descendants from direct children.
5. Combine conditions and use comma-separated selector lists.
6. Prefer stable, purpose-specific locators over fragile structural paths.
7. Test CSS selectors in browser DevTools.

Run this file with the Phase 3 virtual environment, for example:
& ".\\Phase 3 - Browser Automation\\myenv\\Scripts\\python.exe" \
  ".\\Phase 3 - Browser Automation\\Day_69_CSS_Selectors.py"
"""

from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By


# ---------------------------------------------------------------------------
# SECTION 1 - OFFLINE PRACTICE WEBPAGE
# ---------------------------------------------------------------------------
# A data: URL lets Selenium open our HTML without a web server or internet.
# quote() percent-encodes characters that are unsafe inside a URL.

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Equipment Management Portal</title>
</head>
<body>
    <header id="main-header">
        <h1>Equipment Management Portal</h1>
        <p class="subtitle">CSS Selector Practice</p>
    </header>

    <main id="equipment-catalogue">
        <section class="product-list">
            <article class="product available featured"
                     data-code="EQ-101" data-category="sensor">
                <h2 class="product-name">Sensor Kit</h2>
                <p class="price">$48.50</p>
                <p class="stock">In stock</p>
                <button class="action inspect" name="inspect-product"
                        data-testid="inspect-EQ-101">Inspect</button>
            </article>

            <article class="product unavailable"
                     data-code="EQ-102" data-category="controller">
                <h2 class="product-name">Control Module</h2>
                <p class="price">$72.00</p>
                <p class="stock">Out of stock</p>
                <button class="action inspect" name="inspect-product"
                        data-testid="inspect-EQ-102" disabled>Inspect</button>
            </article>

            <article class="product available"
                     data-code="EQ-103" data-category="relay">
                <h2 class="product-name">Relay Board</h2>
                <p class="price">$35.25</p>
                <p class="stock">In stock</p>
                <button class="action inspect" name="inspect-product"
                        data-testid="inspect-EQ-103">Inspect</button>
            </article>
        </section>

        <section class="controls">
            <button class="action save" data-testid="save-catalogue">
                Save Catalogue
            </button>
        </section>
    </main>

    <footer><p class="status">Portal ready</p></footer>
</body>
</html>
"""

page_url = "data:text/html;charset=utf-8," + quote(html)


# ---------------------------------------------------------------------------
# SECTION 2 - START CHROME SAFELY
# ---------------------------------------------------------------------------

driver = webdriver.Chrome()

try:
    driver.get(page_url)

    print("Page title:", driver.title)
    print("Current URL starts with data:", driver.current_url.startswith("data:"))

    # -----------------------------------------------------------------------
    # SECTION 3 - TAG, ID, AND CLASS SELECTORS
    # -----------------------------------------------------------------------

    # Tag selector: finds the first <h1> element.
    main_heading = driver.find_element(By.CSS_SELECTOR, "h1")
    print("\nTag selector:")
    print("Heading:", main_heading.text)

    # ID selector: # means id in CSS selector syntax.
    catalogue = driver.find_element(By.CSS_SELECTOR, "#equipment-catalogue")
    print("\nID selector:")
    print("Catalogue tag:", catalogue.tag_name)

    # One class: .product matches every element containing class="product".
    products = driver.find_elements(By.CSS_SELECTOR, ".product")
    print("\nSingle-class selector:")
    print("Products found:", len(products))

    # No space: all classes must belong to the same element.
    featured_available_products = driver.find_elements(
        By.CSS_SELECTOR,
        ".product.available.featured",
    )
    print("\nCombined-class selector:")
    print("Available featured products:", len(featured_available_products))
    for product in featured_available_products:
        print("Product:", product.text.splitlines()[0])

    # -----------------------------------------------------------------------
    # SECTION 4 - ATTRIBUTE SELECTORS
    # -----------------------------------------------------------------------

    # [attribute] checks only that the attribute exists.
    coded_products = driver.find_elements(By.CSS_SELECTOR, "[data-code]")
    print("\nAttribute-existence selector:")
    print("Elements with data-code:", len(coded_products))

    # [attribute="value"] requires an exact value.
    eq_102 = driver.find_element(By.CSS_SELECTOR, '[data-code="EQ-102"]')
    print("\nExact attribute selector:")
    print(
        "EQ-102 product:",
        eq_102.find_element(By.CSS_SELECTOR, ".product-name").text,
    )

    # ^= starts with.
    inspect_buttons = driver.find_elements(
        By.CSS_SELECTOR,
        'button[data-testid^="inspect-"]',
    )
    print("\nStarts-with attribute selector:")
    print("Inspect buttons:", len(inspect_buttons))

    # $= ends with.
    eq_103_button = driver.find_element(
        By.CSS_SELECTOR,
        'button[data-testid$="EQ-103"]',
    )
    print("\nEnds-with attribute selector:")
    print("EQ-103 button text:", eq_103_button.text)

    # A Boolean HTML attribute is matched by its presence.
    disabled_buttons = driver.find_elements(By.CSS_SELECTOR, "button[disabled]")
    print("\nBoolean attribute selector:")
    print("Disabled buttons:", len(disabled_buttons))

    # *= contains the specified text anywhere in the attribute value.
    controller_products = driver.find_elements(
        By.CSS_SELECTOR,
        '[data-category*="roll"]',
    )
    print("\nContains attribute selector:")
    print("Categories containing 'roll':", len(controller_products))

    # -----------------------------------------------------------------------
    # SECTION 5 - DESCENDANTS AND DIRECT CHILDREN
    # -----------------------------------------------------------------------

    # A space means a descendant at any depth inside the ancestor.
    product_names = driver.find_elements(
        By.CSS_SELECTOR,
        "#equipment-catalogue .product-name",
    )
    print("\nDescendant selector:")
    print("Product names inside catalogue:", len(product_names))
    for name in product_names:
        print("-", name.text)

    # > means a direct child only.
    direct_product_children = driver.find_elements(
        By.CSS_SELECTOR,
        ".product-list > .product",
    )
    print("\nDirect-child selector:")
    print("Direct product children:", len(direct_product_children))

    # The product names are nested inside articles, so this correctly finds 0.
    wrong_direct_relationship = driver.find_elements(
        By.CSS_SELECTOR,
        ".product-list > .product-name",
    )
    print("\nNon-matching direct-child selector:")
    print("Direct product-name children:", len(wrong_direct_relationship))

    # -----------------------------------------------------------------------
    # SECTION 6 - COMBINED CONDITIONS AND SELECTOR LISTS
    # -----------------------------------------------------------------------

    # These tag, class, and attribute conditions describe the same element.
    specific_product = driver.find_element(
        By.CSS_SELECTOR,
        'article.product.available[data-code="EQ-103"]',
    )
    specific_name = specific_product.find_element(
        By.CSS_SELECTOR,
        ".product-name",
    ).text
    print("\nCombined selector conditions:")
    print("Specific available product:", specific_name)

    # A comma means OR. This finds a save button OR a disabled button.
    special_buttons = driver.find_elements(
        By.CSS_SELECTOR,
        "button.save, button[disabled]",
    )
    print("\nSelector list using a comma:")
    print("Save or disabled buttons:", len(special_buttons))
    for button in special_buttons:
        print("-", button.text)

    # input() keeps the page visible until the learner chooses to close it.
    input("\nPress Enter after checking the Chrome page...")

finally:
    # finally runs even when an exception occurs, preventing orphaned browsers.
    driver.quit()


# DEVTOOLS QUICK REFERENCE
# ------------------------
# document.querySelector(".product")
#     Returns the first matching element, or null.
#
# document.querySelectorAll(".product")
#     Returns a NodeList containing all matching elements.
#
# document.querySelectorAll(".product").length
#     Returns the number of matching elements.
#
# STABILITY RULE
# --------------
# Prefer short purpose-specific selectors such as:
#     button[data-testid="submit-order"]
# Avoid long position-dependent selectors such as:
#     body > div:nth-child(2) > form > button:nth-child(3)
