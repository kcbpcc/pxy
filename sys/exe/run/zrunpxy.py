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
    table_rows = soup.select('table tr')[1:]  # Select all table rows except the header
    for row in table_rows:
        columns = row.find_all('td')
        if len(columns) > 1:
            index = columns[0].text.strip()
            change_percent = columns[3].text.strip()
            market_data.append((index, change_percent))
    return market_data

# Extract the market data
data = scrape_market_data(soup)

# Print the scraped data with color formatting
formatted_output = []
for index, change_percent in data:
    change_value = float(change_percent.replace('%', '').replace(',', ''))
    color = 'green' if change_value > 0 else 'red'
    formatted_output.append(f"\033[1;{32 if color == 'green' else 31}m{index}\033[0m")

print("|".join(formatted_output))

# Reset terminal color
print("\033[0m")

