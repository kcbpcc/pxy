from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re

# Path to the ChromeDriver executable
chromedriver_path = '/usr/local/bin/chromedriver'

# Set up Chrome options
options = Options()
options.add_argument('--headless')  # Run in headless mode (optional)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the WebDriver with Service and Options
service = Service(executable_path=chromedriver_path)
try:
    driver = webdriver.Chrome(service=service, options=options)

    # URL of the web page
    url = "https://console.zerodha.com/verified/783d6dad"

    print(f"Opening URL: {url}")
    # Open the web page
    driver.get(url)
    print("Page opened successfully.")

    # Let the page load (adjust time as necessary)
    driver.implicitly_wait(30)  # Increase wait time to 30 seconds

    # Get the page source
    page_source = driver.page_source
    print("Page source retrieved.")

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

except Exception as e:
    print(f"An error occurred: {str(e)}")
    if 'executable needs to be in PATH' in str(e):
        print("Make sure chromedriver is installed and available in PATH")
