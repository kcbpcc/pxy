from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv

# Your login credentials
username = 'your_username'
password = 'your_password'

# URL for login
login_url = 'https://www.kammamarimonony.com/login'

# Create a webdriver instance
driver = webdriver.Chrome()

try:
    # Perform login
    driver.get(login_url)
    username_field = driver.find_element(By.NAME, 'username')
    password_field = driver.find_element(By.NAME, 'password')

    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    # Wait for login to complete (you may need to adjust the wait time)
    driver.implicitly_wait(10)

    # Get all KMC* hyperlinks
    kmc_links = driver.find_elements(By.XPATH, '//*[starts-with(text(), "KMC")]/ancestor::a')

    # Loop through each KMC* hyperlink
    for link in kmc_links:
        # Click on the link
        link.click()

        # Wait for the new page to load (you may need to adjust the wait time)
        driver.implicitly_wait(10)

        # Find and capture net worth
        net_worth_element = driver.find_element(By.XPATH, '//span[contains(text(), "Net Worth")]/following-sibling::span')
        net_worth = net_worth_element.text

        # Capture KMC* and net worth to a CSV file
        with open('kmc_net_worth.csv', 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([link.text, net_worth])

        # Go back to the previous page
        driver.back()

        # Wait for the page to navigate back (you may need to adjust the wait time)
        driver.implicitly_wait(10)

finally:
    # Close the browser window
    driver.quit()
