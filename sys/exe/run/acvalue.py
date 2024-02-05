import csv
from datetime import datetime, timedelta
import time

START_TIME = 201
END_TIME = 214
CSV_FILENAME = 'acvalue.csv'

def process_acvalue(acvalue):
    current_utc_time = time.gmtime().tm_hour * 60 + time.gmtime().tm_min
    current_date = datetime.utcnow().strftime('%Y-%m-%d')

    try:
        with open(CSV_FILENAME, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
    except Exception as e:
        # Handle the exception (e.g., log an error message)
        print(f"Error reading CSV file: {e}")
        return

    if START_TIME <= current_utc_time <= END_TIME:
        record_exists = any(row['date'] == current_date for row in rows)

        if not record_exists:
            rows.append({'date': current_date, 'acvalue': acvalue})

            with open(CSV_FILENAME, mode='w', newline='') as csvfile:
                fieldnames = ['date', 'acvalue']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        else:
            print(f"Record for {current_date} already exists. Not updating.")

    else:
        if not any(row['date'] == current_date for row in rows):
            print(f"{datetime.utcnow().strftime('%Y-%m-%d')} A/C Value will be updated @9:01")

def get_current_acvalue():
    try:
        with open(CSV_FILENAME, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
    except Exception as e:
        # Handle the exception (e.g., log an error message)
        print(f"Error reading CSV file: {e}")
        return 0, 0

    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    record_exists = any(row['date'] == current_date for row in rows)

    if record_exists:
        current_acvalue = float([row['acvalue'] for row in rows if row['date'] == current_date][0])

        # Calculate ydaypnl by finding yesterday's acvalue
        yesterday_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
        yesterday_acvalue = float([row['acvalue'] for row in rows if row['date'] == yesterday_date][0])

        ydaypnl = current_acvalue - yesterday_acvalue

        return current_acvalue, ydaypnl
    else:
        # Handle the case when a record for the current date doesn't exist
        if rows:
            # Assuming rows is a list of dictionaries with 'date' and 'acvalue' keys
            latest_row = max(rows, key=lambda row: row['date'])
            latest_acvalue = float(latest_row['acvalue'])
    
            # You can log a message here if needed
            # print(f"No record found for {current_date} in CSV file. Returning latest data.")
    
            return latest_acvalue, 0
        else:
            # Handle the case when the file is empty
            # print("CSV file is empty. Unable to retrieve latest data.")
            return 0, 0
