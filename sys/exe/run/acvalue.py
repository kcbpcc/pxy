import csv
from datetime import datetime, timedelta
import time

START_TIME = 210
END_TIME = 224
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
        ydaypnl = acvalue - float(rows[-1]['acvalue']) if rows and rows[-1]['date'] == current_date else 0

        record_exists = any(row['date'] == current_date for row in rows)

        if record_exists:
            for i, row in enumerate(rows):
                if row['date'] == current_date:
                    rows[i] = {'date': current_date, 'acvalue': acvalue, 'ydaypnl': ydaypnl}
                    break
        else:
            rows.append({'date': current_date, 'acvalue': acvalue, 'ydaypnl': ydaypnl})

            with open(CSV_FILENAME, mode='w', newline='') as csvfile:
                fieldnames = ['date', 'acvalue', 'ydaypnl']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
    else:
        if not any(row['date'] == current_date for row in rows):
            print(f"{datetime.utcnow().strftime('%Y-%m-%d')} A/C Value will be updated @9:15")


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
        ydaypnl = float([row['ydaypnl'] for row in rows if row['date'] == current_date][0])
        return current_acvalue, ydaypnl
    else:
        # Handle the case when a record for the current date doesn't exist (e.g., log a message)
        print(f"No record found for {current_date} in CSV file")
        return 0, 0


