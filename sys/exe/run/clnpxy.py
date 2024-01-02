#PXY®
import csv
from datetime import datetime, timedelta

# Specify the path to your CSV file
file_path = 'filePnL.csv'

# Function to check if the current time is between 2:00 AM and 3:45 AM UTC
def is_time_between(start_time, end_time):
    current_time = datetime.utcnow()
    return start_time <= current_time <= end_time

# Specify the time range during which you want to delete contents (2:00 AM to 3:00 AM UTC)
start_time = datetime.utcnow().replace(hour=2, minute=0, second=0, microsecond=0)
end_time = datetime.utcnow().replace(hour=3, minute=0, second=0, microsecond=0)

# Check if the current time is within the specified range
if is_time_between(start_time, end_time):
    # Open the file in write mode to truncate its contents
    with open(file_path, 'w', newline='') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)

        # Write an empty row to clear the contents
        csv_writer.writerow([])
