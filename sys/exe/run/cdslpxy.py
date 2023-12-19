import asyncio
from pyppeteer import launch
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

TPIN = "303518"

async def main():
    browser = await launch({'headless': False})  # Set 'headless' to True for headless mode
    page = await browser.newPage()

    # Opening Kite Web app
    await page.goto('https://kite.zerodha.com/')
    
    # Clicking the login button
    await page.click('.button-orange')
    await page.waitForNavigation()

    # Continue with your pyppeteer script logic...

    # Get the URL after the initial interactions
    kite_url = page.url

    # Close the browser
    await browser.close()

    # Switch to Selenium for the remaining interactions
    option = Options()
    option.add_argument("user-data-dir=/home/userland/.config/google-chrome")  # Replace 'userland' with your Linux username
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=option)

    try:
        sys.stdout = open('output.txt', 'w')
        # Incorporate your login mechanism here
        # Assuming get_kite is a function that logs in and returns a broker object
        # Update this part with your actual login mechanism
        broker = get_kite(api="bypass", sec_dir=dir_path)

    except Exception as e:
        print(traceback.format_exc())
        sys.exit(1)

    # Continue with your Selenium script logic using the kite_url
    driver.get(kite_url)
    
    # Navigating to the holdings page
    driver.get("https://kite.zerodha.com/holdings")

    # Selecting "Authorisation" option
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/section/div/div/div/span[2]/a[1]").click()
    time.sleep(2)
    kite_window = driver.window_handles[1]

    # Selecting "Continue" in authorization pop up
    try:
        WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div/div/div[3]/div/button[1]")))
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div/div/div[3]/div/button[1]").click()
    except TimeoutException:
        print("Page not loaded")
    time.sleep(2)

    # Switching to CDSL page
    cdsl_window = driver.window_handles[2]
    driver.switch_to.window(cdsl_window)
    driver.implicitly_wait(120)
    time.sleep(3)

    try:
        WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/button")))
        # Selecting "Continue to CDSL"
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/button").click()
    except TimeoutException:
        print("CDSL Page Not Loaded")

    time.sleep(3)

    # Entering the hardcoded TPIN
    driver.find_element_by_id("txtPIN").send_keys(TPIN)
    driver.find_element_by_id("btnCommit").click()
    driver.implicitly_wait(60)

    # Manually input the OTP
    manual_otp = input("Please enter the OTP manually: ")

    # Entering the manually input OTP
    if manual_otp:
        driver.find_element_by_id("OTP").send_keys(manual_otp)
        driver.find_element_by_id("VerifyOTP").click()
        print("Entered OTP on the CDSL page.")
    else:
        print("No OTP provided. Exiting script.")
        driver.quit()

# Run the main function
asyncio.get_event_loop().run_until_complete(main())

