import re
import datetime
import pytz
from oauth2client.service_account import ServiceAccountCredentials
import gspread

def remove_color_codes(text):
    # Define the color codes to be removed
    color_codes = ['[92m', '[91m', '[93m', '[90m', '[1m', '[4m', '[0m']
    
    # Remove color codes
    for code in color_codes:
        text = text.replace(code, '')
    
    return text

def update_google_sheet(cleaned_text):
    # Load Google Sheets credentials from a service account file
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('accvalue.json', scope)
    client = gspread.authorize(credentials)

    # Open the Google Sheet
    sheet = client.open("dashboard").sheet1  # Replace "dashboard" with the actual name of your Google Sheet

    # Clear existing content from the sheet
    sheet.clear()

    # Update cell A1 with the cleaned text and cell A2 with timestamp
    sheet.update(range_name='A1', values=[[cleaned_text]])

    # Get Singapore time
    singapore = pytz.timezone('Asia/Singapore')
    now_singapore = datetime.datetime.now(singapore)
    timestamp_singapore = now_singapore.strftime("%Y-%m-%d %H:%M:%S")

    # Update cell A2 with timestamp in Singapore time
    sheet.update(range_name='A2', values=[[timestamp_singapore]])

    #print("Google Sheet updated successfully")

def main():
    input_file = 'bordpxy.csv'

    with open(input_file, 'r') as file:
        text_with_color_codes = file.read()

    # Remove color codes
    cleaned_text = remove_color_codes(text_with_color_codes)

    # Update Google Sheet with the cleaned text and timestamp
    update_google_sheet(cleaned_text)

if __name__ == "__main__":
    main()

