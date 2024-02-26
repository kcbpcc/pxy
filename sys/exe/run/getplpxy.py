import requests
from bs4 import BeautifulSoup

# URL of the webpage you want to scrape
url = "https://console.zerodha.com/verified/09142c22"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the elements containing "Equity" and "F&O" along with their corresponding numbers
    equity_element = soup.find(text="Equity")
    equity_number = equity_element.find_next_sibling().text.strip()
    
    fo_element = soup.find(text="F&O")
    fo_number = fo_element.find_next_sibling().text.strip()
    
    # Print the extracted information
    print("Equity:", equity_number)
    print("F&O:", fo_number)
    
    # Write the extracted information to a text file
    with open('extracted_info.txt', 'w', encoding='utf-8') as file:
        file.write("Equity: " + equity_number + "\n")
        file.write("F&O: " + fo_number + "\n")
    
    print("Information extracted successfully and saved to 'extracted_info.txt'")
else:
    print("Failed to fetch the webpage")
