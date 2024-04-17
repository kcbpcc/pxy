import csv
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Global variables
GOOGLE_SHEET_TITLE = 'accvalue'  # Adjusted Google Sheet title
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

def gsheet_acvalue(acvalue):
    # Get current date
    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    print(f"Processing AC value {acvalue} for date {current_date}")

    # Authenticate with Google Sheets API
    print("Authenticating with Google Sheets API...")
    creds = ServiceAccountCredentials.from_json_keyfile_name('accvalue.json', SCOPES)
    client = gspread.authorize(creds)

    try:
        # Open the Google Sheet
        print("Opening Google Sheet...")
        sheet = client.open(GOOGLE_SHEET_TITLE).sheet1

        # Get existing data
        print("Getting existing data from Google Sheet...")
        existing_data = sheet.get_all_records()

        # Check if the record exists and update or append accordingly
        record_exists = False
        for index, row in enumerate(existing_data, start=2):  # Start from row 2 (assuming headers are in row 1)
            if row['date'] == current_date:
                print("Updating existing record in Google Sheet...")
                sheet.update_cell(index, 2, acvalue)  # Update the 'acvalue' column in the matching row
                record_exists = True
                break

        # If the record does not exist, append a new row
        if not record_exists:
            print("Appending new record to Google Sheet...")
            sheet.append_row([current_date, acvalue])

        print("Update complete.")

    except Exception as e:
        # Handle the exception
        print(f"Error updating Google Sheet: {e}")

# Example usage:
# gsheet_acvalue(100)  # Call this function with the AC value you want to process

