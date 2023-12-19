import csv

def remove_rows_with_inf(csv_file_path):
    try:
        with open(csv_file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = [row for row in reader if 'inf' not in row]

        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)

        print("Rows with 'inf' values removed successfully.")

    except FileNotFoundError:
        print("File not found!")

# Replace "filePnL.csv" with your actual CSV file path
csv_file_path = "filePnL.csv"
remove_rows_with_inf(csv_file_path)
