from bs4 import BeautifulSoup

html = '''
<html>
    <body>
        <h1>Programming Books</h1>
        <p>Python Basics</p>
        <p>Advanced Python</p>
        <p>Web Scraping with Python</p>
        <div class="book-card">
            <h2>Python Automation Guide</h2>
            <p class="price">$49</p>
        </div>
        <a href="https://example.com/books">Visit Store</a>
    </body>
</html>
'''

soup = BeautifulSoup(html, 'html.parser')

heading = soup.find('h1')
print('Heading element:', heading)
print('Heading text:', heading.get_text(strip=True))

paragraphs = soup.find_all('p')
print('Paragraph text values:')
for paragraph in paragraphs:
    print('-', paragraph.get_text(strip=True))

book_card = soup.find('div')
print('Book card text:', book_card.get_text(separator=' | ', strip=True))

link = soup.find('a')
print('Link text:', link.get_text(strip=True))
print('Link href preview:', link.get('href'))
