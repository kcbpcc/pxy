from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import traceback
import sys
import re

message = ""
OTP = 0

KITE_URL = "https://kite.zerodha.com/"
HOLDINGS_URL = "https://kite.zerodha.com/holdings"

# pattern for extracting OTP
pattern_otp = "\d{6}"

option = Options()
# Loading default Chrome Profile
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

# Opening Messages Web app
driver.get('https://messages.google.com/web/')
driver.implicitly_wait(60)
messages_window = driver.window_handles[0]
driver.execute_script("window.open('https://kite.zerodha.com/');")
time.sleep(2)
driver.switch_to.window(driver.window_handles[1])

# Replace the following lines with your login mechanism
# For example, you might need to enter the credentials in the login form
# clicking login button
driver.find_element_by_class_name("button-orange").click()
driver.implicitly_wait(60)

# navigating to holding page
driver.get(HOLDINGS_URL)
driver.implicitly_wait(60)
time.sleep(2)

# selecting "Authorisation" option
driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/section/div/div/div/span[2]/a[1]").click()
time.sleep(2)
driver.implicitly_wait(60)
kite_window = driver.window_handles[1]

# Selecting "Continue" in authorization pop up
try:
    WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div/div/div[3]/div/button[1]")))
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div/div/div[3]/div/button[1]").click()
except TimeoutException:
    print("Page not loaded")
time.sleep(2)
driver.implicitly_wait(60)

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
