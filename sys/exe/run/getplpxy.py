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
    
    # Extract all text from the webpage
    all_text = soup.get_text()
    
    # Write the extracted text to a text file
    with open('extracted_text.txt', 'w', encoding='utf-8') as file:
        file.write(all_text)
    
    print("Text extracted successfully and saved to 'extracted_text.txt'")
else:
    print("Failed to fetch the webpage")
