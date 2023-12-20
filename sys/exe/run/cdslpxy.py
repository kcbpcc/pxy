import asyncio
import traceback
from pyppeteer import launch
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

TPIN = "303518"

async def main():
    try:
        # Pyppeteer part
        browser = await launch({'headless': True})
        page = await browser.newPage()
        
        await page.goto('https://kite.zerodha.com/')
        await page.click('.button-orange')
        await page.waitForNavigation()
        
        # Continue with your pyppeteer script logic...

        kite_url = page.url
        await browser.close()

        # Selenium part
        option = Options()
        option.add_argument("user-data-dir=/home/userland/.config/google-chrome")
        driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=option)

        driver.get(kite_url)
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

    except Exception as e:
        print(f"Error: {e}")
        print("Traceback:")
        print(traceback.format_exc())

# Run the main function
asyncio.get_event_loop().run_until_complete(main())


