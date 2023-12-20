import time
import traceback
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

TPIN = "303518"

def main():
    display = Display(visible=0, size=(800, 600))
    display.start()

    try:
        # Selenium part
        options = Options()
        options.add_argument("--headless")
        options.add_argument("user-data-dir=/home/userland/.config/google-chrome")
        
        # Provide the path to chromedriver executable directly in the webdriver.Chrome() call
        driver = webdriver.Chrome(options=options, executable_path="/usr/local/bin/chromedriver")

        # Opening Kite Web app
        driver.get('https://kite.zerodha.com/')

        # Clicking the login button
        driver.find_element_by_class_name('button-orange').click()
        time.sleep(2)  # Add a delay if needed

        # Continue with your Selenium script logic...

        # Navigating to the holdings page
        driver.get("https://kite.zerodha.com/holdings")

        # Selecting "Authorisation" option
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/section/div/div/div/span[2]/a[1]").click()
        time.sleep(2)

        # Selecting "Continue" in authorization pop up
        try:
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div/div/div[3]/div/button[1]")))
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div/div/div[3]/div/button[1]").click()
        except TimeoutException:
            print("Page not loaded")

        time.sleep(2)

        # Switching to CDSL page
        cdsl_window = driver.window_handles[1]
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

    except Exception as e:
        print(f"Error: {e}")
        print("Traceback:")
        print(traceback.format_exc())
    finally:
        # Ensure the browser is closed in case of any exceptions
        if driver:
            driver.quit()
        display.stop()

# Run the main function
if __name__ == "__main__":
    main()



