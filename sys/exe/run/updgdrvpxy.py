import csv
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from utcpxy import peak_time

# Global variables
GOOGLE_SHEET_TITLE = 'pxy/accvalue'
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

def gsheet_acvalue(acvalue):

    current_date = datetime.utcnow().strftime('%Y-%m-%d')

    # Authenticate with Google Sheets API
    creds = ServiceAccountCredentials.from_json_keyfile_name('accvalue.json', SCOPES)
    client = gspread.authorize(creds)

    try:
        # Open the Google Sheet
        sheet = client.open(GOOGLE_SHEET_TITLE).sheet1

        # Get existing data
        existing_data = sheet.get_all_records()

        # Check if the record exists and update or append accordingly
        record_exists = False
        for index, row in enumerate(existing_data, start=2):  # Start from row 2 (assuming headers are in row 1)
            if row['date'] == current_date:
                sheet.update_cell(index, 2, acvalue)  # Update the 'acvalue' column in the matching row
                record_exists = True
                break

        # If the record does not exist, append a new row
        if not record_exists:
            sheet.append_row([current_date, acvalue])

    except Exception as e:
        # Handle the exception (e.g., log an error message)
        print(f"Error updating Google Sheet: {e}")

# Example usage:
# process_acvalue(100)  # Call this function with the AC value you want to process
