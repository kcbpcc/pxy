import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import os

# Path to the JSON file containing credentials
CREDENTIALS_FILE = 'acvalpxy.json'
LOCAL_CSV_FILE = 'acvalpxy.csv'

# Debugging: #print the path of the credentials file
#print(f"Loading credentials from: {CREDENTIALS_FILE}")

try:
    # Load the credentials from the JSON file
    with open(CREDENTIALS_FILE, 'r') as file:
        credentials_dict = json.load(file)
    #print("Credentials loaded successfully.")
except Exception as e:
    #print(f"Error loading credentials: {e}")
    raise

try:
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        credentials_dict,
        ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    )
    #print("Credentials for Google Sheets API created successfully.")
except Exception as e:
    #print(f"Error creating credentials: {e}")
    raise

# Create a client instance
try:
    client = gspread.authorize(creds)
    #print("Authenticated with Google Sheets API successfully.")
except Exception as e:
    #print(f"Error authenticating with Google Sheets API: {e}")
    raise

SPREADSHEET_ID = '15WOo4nE8kK-ZjQKdeRpbtHnqwYExFX4w36IiXyLzVyA'
SHEET_NAME = 'Sheet1'  # Adjust if necessary

try:
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    #print(f"Connected to spreadsheet: {SPREADSHEET_ID}, sheet: {SHEET_NAME}")
except Exception as e:
    #print(f"Error accessing spreadsheet or worksheet: {e}")
    raise

def process_acvalue(acvalue):
    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    #print(f"Current date: {current_date}")

    try:
        # Read existing data from Google Sheets
        data = sheet.get_all_values()
        #print("Data retrieved from Google Sheets.")
        #print("Retrieved data:", data)  # Debug #print to inspect the data
    except Exception as e:
        #print(f"Error reading Google Sheet: {e}")
        return

    # Check if a record for the current date exists
    row_index_to_update = None
    for index, row in enumerate(data):
        if len(row) > 0 and row[0] == current_date:
            row_index_to_update = index + 1  # Google Sheets is 1-indexed
            break

    if row_index_to_update:
        try:
            #print(f"Updating existing record at row {row_index_to_update} with AC value: {acvalue}")
            sheet.update_cell(row_index_to_update, 2, acvalue)  # Update 'acvalue' in the second column
            #print(f"Updated cell ({row_index_to_update}, 2) with value: {acvalue}")
        except Exception as e:
            #print(f"Error updating cell: {e}")
    else:
        new_row = [current_date, acvalue]
        try:
            #print(f"Adding new row to Google Sheets with data: {new_row}")
            sheet.append_row(new_row)
            #print(f"Added new row with data: {new_row}")
        except Exception as e:
            #print(f"Error appending row: {e}")

    # Save the updated data to a CSV file
    try:
        # Fetch all records from Google Sheets
        updated_data = sheet.get_all_values()
        # Convert data to DataFrame
        df = pd.DataFrame(updated_data, columns=['date', 'acvalue'])  # Manually define column names
        # Save DataFrame to CSV file
        df.to_csv(LOCAL_CSV_FILE, index=False)
        #print(f"Data saved to {LOCAL_CSV_FILE}")
    except Exception as e:
        #print(f"Error saving data to CSV: {e}")

def retrieve_acvalue():
    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    try:
        # Check if the local CSV file exists
        if os.path.exists(LOCAL_CSV_FILE):
            # Get the file modification date
            modification_time = datetime.utcfromtimestamp(os.path.getmtime(LOCAL_CSV_FILE))
            #print(f"Local file modification time: {modification_time}")

            # If the file was modified today, read from the local file
            if modification_time.date() == datetime.utcnow().date():
                #print("Local file is up-to-date. Reading AC value from local file.")
                df = pd.read_csv(LOCAL_CSV_FILE)
                # Ensure we have the latest entry for today
                if df['date'].iloc[-1] == current_date:
                    acvalue = float(df['acvalue'].iloc[-1])
                    #print(f"Retrieved AC value from local file: {acvalue}")
                    return acvalue

        # If the file doesn't exist or is not up-to-date, fetch from Google Sheets
        #print("Local file not found or not up-to-date. Fetching data from Google Sheets.")
        data = sheet.get_all_values()
        df = pd.DataFrame(data, columns=['date', 'acvalue'])
        df.to_csv(LOCAL_CSV_FILE, index=False)
        #print(f"Updated local file with data from Google Sheets: {LOCAL_CSV_FILE}")

        # Retrieve the latest AC value
        if df['date'].iloc[-1] == current_date:
            acvalue = float(df['acvalue'].iloc[-1])
            #print(f"Retrieved AC value from Google Sheets: {acvalue}")
            return acvalue
        else:
            #print("No record found for the current date.")
            return None

    except Exception as e:
        #print(f"Error retrieving AC value: {e}")
        return None
