import re
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

    # Convert the cleaned text to a list of rows
    rows = cleaned_text.split('\n')

    # Write the cleaned text to the sheet
    for i, row in enumerate(rows):
        # Split the row into cells based on comma or semicolon (adjust as needed)
        cells = re.split(r'[;,]', row.strip())
        sheet.insert_row(cells, i+1)

    print("Google Sheet updated successfully")

def main():
    input_file = 'bordpxy.csv'

    with open(input_file, 'r') as file:
        text_with_color_codes = file.read()

    # Remove color codes
    cleaned_text = remove_color_codes(text_with_color_codes)

    # Update Google Sheet with the cleaned text
    update_google_sheet(cleaned_text)

if __name__ == "__main__":
    main()

