import requests
from bs4 import BeautifulSoup

# URL of the target webpage
url = "https://giftcitynifty.com/global-market/"

# Send a GET request to the webpage
response = requests.get(url)
response.raise_for_status()  # Ensure the request was successful

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Function to scrape the market data
def scrape_market_data(soup):
    market_data = []
    index_to_country = {
        'Dow 30': 'DUS',
        'S&P 500': 'SUS',
        'Nasdaq Composite': 'NUS',
        'FTSE 100': 'UK',
        'CAC 40': 'FR',
        'DAX': 'DE',
        'Nikkei 225': 'JP',
        'Hang Seng': 'HK',
        'Shanghai Composite': 'CN',
        'STI': 'SG',
        'Kospi': 'KR'
    }
    table_rows = soup.select('table tr')[1:]  # Select all table rows except the header
    for row in table_rows:
        columns = row.find_all('td')
        if len(columns) > 1:
            index_name = columns[0].text.strip()
            country_code = index_to_country.get(index_name, 'Unknown')
            market_data.append(country_code)
    return market_data

# Extract the market data
data = scrape_market_data(soup)

# Print the scraped data with color formatting
formatted_output = []
for country_code in data:
    formatted_output.append(f"\033[1;{32 if country_code == 'US' else 31}m{country_code}\033[0m")

print("|".join(formatted_output))

# Reset terminal color
print("\033[0m")


