import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from utcpxy import peak_time

# Hardcoded credentials JSON
CREDS_JSON = """
{
  "type": "service_account",
  "project_id": "px-kcbpcc",
  "private_key_id": "93b9e72c2e01333c8e18e223914d8ec0a6683c05",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDM4F51KSbOUgCA\\nK0B1Q7k1QEFQxV8JPv2Da8cUhzgfdb+sJytywkaEpMvJCmW1nY9g3K4t+sWnjHcB\\n...\\n7l987pDhLgA8uXr/EK9ATbDRRdrNoRa4UuoOA72FxLzwVOPOJRXgiNtnxLwhbNyM\\n+vtzUB3hBoXCVkC3JZFvn74vWVo7sI/q4wkA8ukCgYB3jeodmlODYaEBBg7jIqBu\\n99z206XW2afHKqzPthdKgECdhxDNLH7Ii9evYOFYesN7ULd7P2sjCC/qNsj2Bbok\\nSk71m+IPoEhQcJdJupjF88oH8TlEZxWorYyLxlif4EVWpn4qJsl/MQUxe4FmiBAf\\n93QSs2sTF6gdKgHYuT8hRA==\\n-----END PRIVATE KEY-----\\n",
  "client_email": "accounvalue@px-kcbpcc.iam.gserviceaccount.com",
  "client_id": "105412308378850370123",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/accounvalue%40px-kcbpcc.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
"""

# Load the credentials from the JSON string
import json
credentials_dict = json.loads(CREDS_JSON)
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

# Create a client instance
client = gspread.authorize(creds)
SPREADSHEET_ID = '15WOo4nE8kK-ZjQKdeRpbtHnqwYExFX4w36IiXyLzVyA'
SHEET_NAME = 'Sheet1'  # Adjust if necessary
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

def process_acvalue(acvalue):
    peak = peak_time()

    if peak != 'PREPEAK':
        # Do nothing if peak != 'PREPEAK'
        return

    current_date = datetime.utcnow().strftime('%Y-%m-%d')

    try:
        # Read existing data from Google Sheets
        data = sheet.get_all_records()
    except Exception as e:
        # Handle the exception (e.g., log an error message)
        print(f"Error reading Google Sheet: {e}")
        return

    record_exists = False
    for row in data:
        if row['date'] == current_date:
            row_index = data.index(row) + 2  # Adding 2 because Google Sheets is 1-indexed and header row
            sheet.update_cell(row_index, 2, acvalue)  # Update 'acvalue' in the second column
            record_exists = True
            break

    if not record_exists:
        new_row = [current_date, acvalue]
        sheet.append_row(new_row)

def get_current_acvalue():
    try:
        # Read existing data from Google Sheets
        data = sheet.get_all_records()
    except Exception as e:
        # Handle the exception (e.g., log an error message)
        print(f"Error reading Google Sheet: {e}")
        return 0, 0

    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    record_exists = any(row['date'] == current_date for row in data)

    if record_exists:
        current_acvalue = float([row['acvalue'] for row in data if row['date'] == current_date][0])

        # Find the most recent past date
        past_dates = [row['date'] for row in data if row['date'] < current_date]
        if past_dates:
            latest_past_date = max(past_dates)
            yesterday_acvalue = float([row['acvalue'] for row in data if row['date'] == latest_past_date][0])
        else:
            yesterday_acvalue = 0  # or handle it according to your logic

        ydaypnl = current_acvalue - yesterday_acvalue

        return current_acvalue, ydaypnl
    else:
        # Handle the case when a record for the current date doesn't exist
        if data:
            # Assuming data is a list of dictionaries with 'date' and 'acvalue' keys
            latest_row = max(data, key=lambda row: row['date'])
            latest_acvalue = float(latest_row['acvalue'])

            return latest_acvalue, 0
        else:
            # Handle the case when the sheet is empty
            return 0, 0

