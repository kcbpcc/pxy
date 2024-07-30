import csv
from datetime import datetime, timedelta
import time
import subprocess
from utcpxy import peak_time

CSV_FILENAME = 'acvalue.csv'

def process_acvalue(acvalue):
    peak = peak_time()

    if peak != 'PREPEAK':
        # Do nothing if peak != 'PREPEAK'
        return

    current_date = datetime.utcnow().strftime('%Y-%m-%d')

    try:
        with open(CSV_FILENAME, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
    except Exception as e:
        # Handle the exception (e.g., log an error message)
        print(f"Error reading CSV file: {e}")
        return

    record_exists = False
    for row in rows:
        if row['date'] == current_date:
            row['acvalue'] = acvalue
            record_exists = True
            break

    if not record_exists:
        rows.append({'date': current_date, 'acvalue': acvalue})
        with open(CSV_FILENAME, mode='w', newline='') as csvfile:
            fieldnames = ['date', 'acvalue']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

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

        # Find the most recent past date
        past_dates = [row['date'] for row in rows if row['date'] < current_date]
        if past_dates:
            latest_past_date = max(past_dates)
            yesterday_acvalue = float([row['acvalue'] for row in rows if row['date'] == latest_past_date][0])
        else:
            yesterday_acvalue = 0  # or handle it according to your logic

        ydaypnl = current_acvalue - yesterday_acvalue

        return current_acvalue, ydaypnl
    else:
        # Handle the case when a record for the current date doesn't exist
        if rows:
            # Assuming rows is a list of dictionaries with 'date' and 'acvalue' keys
            latest_row = max(rows, key=lambda row: row['date'])
            latest_acvalue = float(latest_row['acvalue'])

            return latest_acvalue, 0
        else:
            # Handle the case when the file is empty
            # print("CSV file is empty. Unable to retrieve latest data.")
            return 0, 0
