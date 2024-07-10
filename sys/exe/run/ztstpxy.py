from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re

# Path to the ChromeDriver executable
chromedriver_path = '/usr/local/bin/chromedriver'

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (optional)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(executable_path=chromedriver_path), options=options)

# URL of the web page
url = "https://console.zerodha.com/verified/783d6dad"

# Open the web page
driver.get(url)

# Let the page load (adjust time as necessary)
driver.implicitly_wait(10)

# Get the page source
page_source = driver.page_source

# Use regular expressions to find the specific text and extract the variables
pattern = re.compile(r"Net realised P&L ([\w\s]+) Equity:\s*([0-9,.-]+) F&O:\s*([0-9,.-]+)")

# Extract the data using the pattern
match = pattern.search(page_source)

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

# Close the WebDriver
driver.quit()
