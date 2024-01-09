import csv

# Specify the path to your first CSV file
file_path_pnl = 'filePnL.csv'

# Open the first file in write mode to truncate its contents
with open(file_path_pnl, 'w', newline='') as csvfile_pnl:
    # Create a CSV writer object for the first file
    csv_writer_pnl = csv.writer(csvfile_pnl)

    # Write an empty row to clear the contents
    csv_writer_pnl.writerow([])

    # Write 18 zeros separated by commas as the first row
    csv_writer_pnl.writerow(['0'] * 20)


