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
    
    # Use regular expressions to find the specific text and extract the variables
    pattern = re.compile(r"Net realised P&L ([\w\s]+) Equity:\s*([0-9,.-]+) F&O:\s*([0-9,.-]+)")
    
    # Search the entire text of the soup object for the pattern
    page_text = soup.get_text()
    
    # Extract the data using the pattern
    match = pattern.search(page_text)
    
    if match:
        date = match.group(1)
        equity = match.group(2)
        fo = match.group(3)
        
        # Print the captured data
        print(f"Net realised P&L {date}")
        print(f"Equity: {equity}")
        print(f"F&O: {fo}")
    else:
        print("Failed to find the specified data on the page.")
else:
    print(f"Failed to retrieve the web page. Status code: {response.status_code}")
