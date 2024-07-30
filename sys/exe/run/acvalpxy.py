import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from utcpxy import peak_time

# Path to the JSON file containing credentials
CREDENTIALS_FILE = 'acvalpxy.json'

# Debugging: Print the path of the credentials file
print(f"Loading credentials from: {CREDENTIALS_FILE}")

try:
    # Load the credentials from the JSON file
    with open(CREDENTIALS_FILE, 'r') as file:
        credentials_dict = json.load(file)
    print("Credentials loaded successfully.")
except Exception as e:
    print(f"Error loading credentials: {e}")
    raise

try:
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        credentials_dict,
        ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    )
    print("Credentials for Google Sheets API created successfully.")
except Exception as e:
    print(f"Error creating credentials: {e}")
    raise

# Create a client instance
try:
    client = gspread.authorize(creds)
    print("Authenticated with Google Sheets API successfully.")
except Exception as e:
    print(f"Error authenticating with Google Sheets API: {e}")
    raise

SPREADSHEET_ID = '15WOo4nE8kK-ZjQKdeRpbtHnqwYExFX4w36IiXyLzVyA'
SHEET_NAME = 'Sheet1'  # Adjust if necessary

try:
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    print(f"Connected to spreadsheet: {SPREADSHEET_ID}, sheet: {SHEET_NAME}")
except Exception as e:
    print(f"Error accessing spreadsheet or worksheet: {e}")
    raise

def process_acvalue(acvalue):
    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    print(f"Current date: {current_date}")

    try:
        # Read existing data from Google Sheets
        data = sheet.get_all_records()
        print("Data retrieved from Google Sheets.")
    except Exception as e:
        print(f"Error reading Google Sheet: {e}")
        return

    # Check if a record for the current date exists
    record_exists = False
    for row in data:
        if row['date'] == current_date:
            row_index = data.index(row) + 2  # Google Sheets is 1-indexed and header row
            try:
                print(f"Updating existing record at row {row_index} with AC value: {acvalue}")
                sheet.update_cell(row_index, 2, acvalue)  # Update 'acvalue' in the second column
                print(f"Updated cell ({row_index}, 2) with value: {acvalue}")
            except Exception as e:
                print(f"Error updating cell: {e}")
            record_exists = True
            break

    if not record_exists:
        new_row = [current_date, acvalue]
        try:
            print(f"Adding new row to Google Sheets with data: {new_row}")
            sheet.append_row(new_row)
            print(f"Added new row with data: {new_row}")
        except Exception as e:
            print(f"Error appending row: {e}")

    # Save the updated data to a CSV file
    try:
        # Fetch all records from Google Sheets
        updated_data = sheet.get_all_records()
        # Convert data to DataFrame
        df = pd.DataFrame(updated_data)
        # Save DataFrame to CSV file
        csv_filename = 'acvalpxy.csv'
        df.to_csv(csv_filename, index=False)
        print(f"Data saved to {csv_filename}")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")



def get_current_acvalue():
    print("Retrieving current AC value.")
    
    try:
        # Read existing data from Google Sheets
        data = sheet.get_all_records()
        print("Data retrieved from Google Sheets.")
        print("Retrieved data:", data)
    except Exception as e:
        print(f"Error reading Google Sheet: {e}")
        return 0, 0

    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    print(f"Current date: {current_date}")

    record_exists = any(row['date'] == current_date for row in data)
    print(f"Record exists for current date: {record_exists}")

    if record_exists:
        current_acvalue = float([row['acvalue'] for row in data if row['date'] == current_date][0])
        print(f"Current AC value: {current_acvalue}")

        # Find the most recent past date
        past_dates = [row['date'] for row in data if row['date'] < current_date]
        if past_dates:
            latest_past_date = max(past_dates)
            yesterday_acvalue = float([row['acvalue'] for row in data if row['date'] == latest_past_date][0])
            print(f"Yesterday's AC value: {yesterday_acvalue}")
        else:
            yesterday_acvalue = 0  # or handle it according to your logic
            print("No past data found. Using default value for yesterday's AC value.")

        ydaypnl = current_acvalue - yesterday_acvalue
        print(f"Calculated PNL: {ydaypnl}")

        return current_acvalue, ydaypnl
    else:
        # Handle the case when a record for the current date doesn't exist
        if data:
            # Assuming data is a list of dictionaries with 'date' and 'acvalue' keys
            latest_row = max(data, key=lambda row: row['date'])
            latest_acvalue = float(latest_row['acvalue'])
            print(f"Latest AC value: {latest_acvalue}")

            return latest_acvalue, 0
        else:
            print("No data found. Returning default values.")
            return 0, 0
