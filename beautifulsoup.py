import requests
from bs4 import BeautifulSoup

# Target URL
url = "https://quotes.toscrape.com/"

# Send HTTP request
response = requests.get(url)

# Parse HTML content
soup = BeautifulSoup(response.text, 'lxml')

# Extract data
quotes = soup.find_all('span', class_='text')

for quote in quotes:
    print(quote.text)
