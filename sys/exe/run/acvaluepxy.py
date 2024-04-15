import csv
from datetime import datetime

def process_acvalue(acvalue):
    current_date = datetime.utcnow().strftime('%Y-%m-%d')

    try:
        CSV_FILENAME = "your_filename.csv"  # Specify your CSV filename here
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

    if record_exists:
        with open(CSV_FILENAME, mode='w', newline='') as csvfile:
            fieldnames = ['date', 'acvalue']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)




