import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def get_ac_values():
    # Define the scope and credentials
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('accvalue.json', scope)

    # Authorize the client
    client = gspread.authorize(credentials)

    # Open the Google Sheet by its title
    sheet = client.open('accvalue').sheet1  # Use GOOGLE_SHEET_TITLE instead of hardcoded string if necessary

    # Get all the rows from the sheet
    rows = sheet.get_all_records()

    # Current date
    current_date = datetime.utcnow().strftime('%Y-%m-%d')

    # Check if record exists for current date
    record_exists = any(row['date'] == current_date for row in rows)

    if record_exists:
        # Extract current AC value
        current_acvalue = float([row['acvalue'] for row in rows if row['date'] == current_date][0])

        # Find the most recent past date
        past_dates = [row['date'] for row in rows if row['date'] < current_date]
        
        if past_dates:
            # Extract yesterday's AC value if available
            latest_past_date = max(past_dates)
            yesterday_acvalue = float([row['acvalue'] for row in rows if row['date'] == latest_past_date][0])
        else:
            yesterday_acvalue = 0  # or handle it according to your logic

        # Calculate day-to-day change in value
        ydaypnl = current_acvalue - yesterday_acvalue

        return current_acvalue, ydaypnl
    else:
        return None, None

# Call the function to get the values
current_acvalue, ydaypnl = get_ac_values()



