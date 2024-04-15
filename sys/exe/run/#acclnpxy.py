import csv
from datetime import date

# Function to remove today's entry from the CSV file
def remove_today_entry(csv_file):
    today = date.today().strftime("%Y-%m-%d")

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Remove today's entry
    data = [row for row in data if row[0] != today]

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Example usage
csv_file = 'acvalue.csv'
remove_today_entry(csv_file)
print("Today's entry removed from the CSV file.")
