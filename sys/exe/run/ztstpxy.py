import requests
from bs4 import BeautifulSoup

# URL of the web page
url = "https://console.zerodha.com/verified/783d6dad"

# Send a GET request to the web page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content of the page
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the elements containing the desired data
    equity_data = soup.find(text="Net realised P&L Jul 9, 2024 Equity:").find_next().text
    fo_data = soup.find(text="Net realised P&L Jul 9, 2024 F&O:").find_next().text
    
    # Print the captured data
    print("Net realised P&L Jul 9, 2024")
    print(f"Equity: {equity_data}")
    print(f"F&O: {fo_data}")
else:
    print(f"Failed to retrieve the web page. Status code: {response.status_code}")




