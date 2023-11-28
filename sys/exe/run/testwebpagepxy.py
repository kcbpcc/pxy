from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

class Trendlyne:

    base_url = "https://trendlyne.com/"
    entry_url = base_url + "fundamentals/stock-screener/425413/pluspxy/"

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
        self.driver = webdriver.Chrome(options=chrome_options)

    def entry(self):
        try:
            self.driver.get(self.entry_url)
            time.sleep(5)  # Allow time for dynamic content to load (adjust as needed)

            # Get the page source after JavaScript has executed
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Print the prettified HTML content for inspection
            print(soup.prettify())

            maintag = soup.find(name='main')
            if maintag is not None:
                tbody = maintag.find(name='tbody')
                if tbody is not None:
                    # ... (rest of your code)
                    pass
                else:
                    print("No 'tbody' element found on the page.")
            else:
                print("No 'main' element found on the page.")
        except Exception as e:
            print(e)
        finally:
            self.driver.quit()

if __name__ == '__main__':
    t = Trendlyne()
    t.entry()

