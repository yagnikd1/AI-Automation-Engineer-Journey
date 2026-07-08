"""
=========================================================
Day 30 - HTML Fundamentals for Web Scraping
AI Automation Engineer Journey | Phase 2
=========================================================
"""

print("="*60)
print("Day 30 - HTML Fundamentals for Web Scraping")
print("="*60)

html_tags = {
    "Heading": "<h1>",
    "Paragraph": "<p>",
    "Container": "<div>",
    "Inline": "<span>",
    "Link": "<a>",
    "Image": "<img>",
    "List": "<ul>",
    "List Item": "<li>",
    "Table": "<table>"
}

print("\nCommon HTML Tags")
for k, v in html_tags.items():
    print(f"{k:<15}: {v}")

attributes = {
    "class": "Repeated elements",
    "id": "Unique element",
    "href": "Link URL",
    "src": "Image source",
    "alt": "Image description",
    "title": "Extra information"
}

print("\nHTML Attributes")
for k, v in attributes.items():
    print(f"{k:<8}: {v}")

book_html = '''
<article class="product_pod">
    <h3>
        <a href="catalogue/book.html">Book Title</a>
    </h3>

    <p class="price_color">£51.77</p>
    <p class="instock availability">In Stock</p>
</article>
'''

print("\nBooksToScrape Example")
print(book_html)

print("\nDeveloper Tools")
print("- F12")
print("- Ctrl + Shift + I")
print("- Right Click -> Inspect")
print("- Ctrl + U (View Source)")

print("\nGolden Rule")
print("Find the repeated container first.")
print("Then extract all related data inside it.")

print("\nDay 30 Completed Successfully!")
