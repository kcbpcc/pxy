import requests
from bs4 import BeautifulSoup
import re

# URL of the web page
url = "https://console.zerodha.com/verified/783d6dad"

# Send a GET request to the web page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content of the page
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Use regular expressions to find the text and extract the numbers
    text_to_search = "Net realised P&L Jul 9, 2024"
    equity_pattern = re.compile(rf"{text_to_search} Equity:\s*([0-9,.-]+)")
    fo_pattern = re.compile(rf"{text_to_search} F&O:\s*([0-9,.-]+)")
    
    # Search the entire text of the soup object for the patterns
    page_text = soup.get_text()
    
    # Extract the data using the patterns
    equity_data = equity_pattern.search(page_text)
    fo_data = fo_pattern.search(page_text)
    
    if equity_data and fo_data:
        # Print the captured data
        print("Net realised P&L Jul 9, 2024")
        print(f"Equity: {equity_data.group(1)}")
        print(f"F&O: {fo_data.group(1)}")
    else:
        print("Failed to find the specified data on the page.")
else:
    print(f"Failed to retrieve the web page. Status code: {response.status_code}")
