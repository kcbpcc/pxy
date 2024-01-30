import csv
from datetime import datetime, timedelta
import time

def process_acvalue(acvalue):
    # Calculate the current time in minutes since midnight
    current_utc_time = time.gmtime().tm_hour * 60 + time.gmtime().tm_min

    # Define the time range in minutes since midnight (223 to 245)
    START_TIME = 210
    END_TIME = 224

    # Assuming you have the date of the current record in the variable 'current_date'
    current_date = datetime.utcnow().strftime('%Y-%m-%d')

    # Assuming 'csv_file_path' is the path where you want to store your CSV file
    csv_file_path = '/home/userland/pxy/sys/exe/run/acvalue.csv'

    try:
        # Read the last recorded acvalue from the CSV file
        with open(csv_file_path, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
    except FileNotFoundError:
        # If the file doesn't exist, create an empty list
        rows = []

    # Check if the current time is within the specified range
    if START_TIME <= current_utc_time <= END_TIME:
        # Calculate ydaypnl
        ydaypnl = acvalue - float(rows[-1]['acvalue']) if rows and rows[-1]['date'] == current_date else 0

        # Check if a record for the current date already exists
        record_exists = any(row['date'] == current_date for row in rows)

        if record_exists:
            # If a record for the current date already exists, update it
            for i, row in enumerate(rows):
                if row['date'] == current_date:
                    rows[i] = {'date': current_date, 'acvalue': acvalue, 'ydaypnl': ydaypnl}
                    break
        else:
            # If the record doesn't exist, add a new record
            rows.append({'date': current_date, 'acvalue': acvalue, 'ydaypnl': ydaypnl})

            # Write the records back to the CSV file
            with open(csv_file_path, mode='w', newline='') as csvfile:
                fieldnames = ['date', 'acvalue', 'ydaypnl']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Write the header
                writer.writeheader()

                # Write the records
                writer.writerows(rows)
    else:
        # Print the message only if a record for today doesn't exist
        if not any(row['date'] == current_date for row in rows):
            print(f"{datetime.utcnow().strftime('%Y-%m-%d')} A/C Value will be updated @9:15")


def get_current_acvalue():
    # Assuming 'csv_file_path' is the path where your CSV file is stored
    csv_file_path = '/home/userland/pxy/sys/exe/run/acvalue.csv'

    try:
        # Read the last recorded acvalue from the CSV file
        with open(csv_file_path, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
    except FileNotFoundError:
        # If the file doesn't exist, return default values (you can adjust this as needed)
        return 0, 0

    # Assuming you have the date of the current record in the variable 'current_date'
    current_date = datetime.utcnow().strftime('%Y-%m-%d')

    # Check if a record for the current date exists
    record_exists = any(row['date'] == current_date for row in rows)

    if record_exists:
        # Get the acvalue and ydaypnl for the current date
        current_acvalue = float([row['acvalue'] for row in rows if row['date'] == current_date][0])
        ydaypnl = float([row['ydaypnl'] for row in rows if row['date'] == current_date][0])

        # Return both current_acvalue and ydaypnl
        return current_acvalue, ydaypnl
    else:
        # If a record for the current date doesn't exist, return default values (you can adjust this as needed)
        return 0, 0

# Example usage in your main code
# Assuming 'acvalue' is a variable holding the current acvalue
# You can call process_acvalue(acvalue) to update the CSV file



