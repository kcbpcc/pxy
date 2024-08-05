import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to the JSON file containing credentials
CREDENTIALS_FILE = 'acvalpxy.json'
LOCAL_CSV_FILE = 'acvalpxy.csv'

try:
    # Load the credentials from the JSON file
    with open(CREDENTIALS_FILE, 'r') as file:
        credentials_dict = json.load(file)
    #logging.info("Credentials loaded successfully.")
except Exception as e:
    logging.error(f"Error loading credentials: {e}")
    raise

try:
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        credentials_dict,
        ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    )
    #logging.info("Credentials for Google Sheets API created successfully.")
except Exception as e:
    logging.error(f"Error creating credentials: {e}")
    raise

try:
    client = gspread.authorize(creds)
    #logging.info("Authenticated with Google Sheets API successfully.")
except Exception as e:
    logging.error(f"Error authenticating with Google Sheets API: {e}")
    raise

SPREADSHEET_ID = '15WOo4nE8kK-ZjQKdeRpbtHnqwYExFX4w36IiXyLzVyA'
SHEET_NAME = 'Sheet1'  # Adjust if necessary

try:
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    #logging.info(f"Connected to spreadsheet: {SPREADSHEET_ID}, sheet: {SHEET_NAME}")
except Exception as e:
    logging.error(f"Error accessing spreadsheet or worksheet: {e}")
    raise

def process_acvalue(acvalue):
    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    #logging.info(f"Current date: {current_date}")

    try:
        # Read existing data from Google Sheets
        data = sheet.get_all_values()
        #logging.info("Data retrieved from Google Sheets.")
    except Exception as e:
        logging.error(f"Error reading Google Sheet: {e}")
        return

    row_index_to_update = None
    for index, row in enumerate(data):
        if len(row) > 0 and row[0] == current_date:
            row_index_to_update = index + 1
            break

    if row_index_to_update:
        try:
            sheet.update_cell(row_index_to_update, 2, acvalue)
            #logging.info(f"Updated cell ({row_index_to_update}, 2) with value: {acvalue}")
        except Exception as e:
            logging.error(f"Error updating cell: {e}")
            raise
    else:
        new_row = [current_date, acvalue]
        try:
            sheet.append_row(new_row)
            #logging.info(f"Added new row with data: {new_row}")
        except Exception as e:
            logging.error(f"Error appending row: {e}")
            raise

    try:
        updated_data = sheet.get_all_values()
        df = pd.DataFrame(updated_data, columns=['date', 'acvalue'])
        df.to_csv(LOCAL_CSV_FILE, index=False)
        #logging.info(f"Data saved to {LOCAL_CSV_FILE}")
    except Exception as e:
        logging.error(f"Error saving data to CSV: {e}")
        raise

def retrieve_acvalue():
    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    logging.info(f"Retrieving AC value for date: {current_date}")

    try:
        if os.path.exists(LOCAL_CSV_FILE):
            logging.info(f"Local CSV file {LOCAL_CSV_FILE} exists.")
            modification_time = datetime.utcfromtimestamp(os.path.getmtime(LOCAL_CSV_FILE))
            logging.info(f"Modification time of CSV file: {modification_time}")

            if modification_time.date() == datetime.utcnow().date():
                logging.info("CSV file is up-to-date.")
                df = pd.read_csv(LOCAL_CSV_FILE)
                logging.info("Data loaded from CSV file.")
                logging.debug(f"DataFrame from CSV: \n{df}")

                if 'date' in df.columns:
                    if df['date'].iloc[-1] == current_date:
                        logging.info("Found current date in CSV file.")
                        acvalue = df['acvalue'].iloc[-1]
                        if pd.notna(acvalue):
                            logging.info(f"Retrieved AC value from CSV: {acvalue}")
                            return float(acvalue)
                        else:
                            logging.warning("AC value is NaN, returning 0.")
                            return 0
                    else:
                        logging.warning("Current date not found in CSV, returning 0.")
                        return 0
                else:
                    logging.error("CSV file does not contain 'date' column.")
                    return 0
            else:
                logging.warning("CSV file is outdated, fetching fresh data.")

        data = sheet.get_all_values()
        logging.info("Data retrieved from Google Sheets.")
        # Print all values for debugging
        for row in data:
            print(row)

        # Check if data contains a header row; if not, add one
        if len(data) > 0 and 'date' not in data[0]:
            data.insert(0, ['date', 'acvalue'])
            logging.warning("Added header row to data.")

        df = pd.DataFrame(data[1:], columns=data[0])  # Skip header row for data
        logging.info("DataFrame created from Google Sheets data.")
        logging.debug(f"DataFrame from Google Sheets: \n{df}")

        df.to_csv(LOCAL_CSV_FILE, index=False)
        logging.info(f"Data saved to {LOCAL_CSV_FILE}")

        if 'date' in df.columns:
            if df['date'].iloc[-1] == current_date:
                acvalue = df['acvalue'].iloc[-1]
                if pd.notna(acvalue):
                    logging.info(f"Retrieved AC value from Google Sheets: {acvalue}")
                    return float(acvalue)
                else:
                    logging.warning("AC value is NaN, returning 0.")
                    return 0
            else:
                logging.warning("Current date not found in Google Sheets data, returning 0.")
                return 0
        else:
            logging.error("Google Sheets data does not contain 'date' column.")
            return 0

    except Exception as e:
        logging.error(f"Error retrieving AC value: {e}")
        return 0


