import csv

# Specify the path to your first CSV file
file_path_pnl = 'filePnL.csv'
file_path_pnl_nrml = 'filePnL_nrml.csv'

# Clear contents for filePnL.csv
with open(file_path_pnl, 'w', newline='') as csvfile_pnl:
    csv_writer_pnl = csv.writer(csvfile_pnl)

    # Write an empty row to clear the contents
    csv_writer_pnl.writerow([])

    # Write 20 zeros separated by commas as the first row
    csv_writer_pnl.writerow(['0'] * 20)

# Clear contents for filePnL_nrml.csv
with open(file_path_pnl_nrml, 'w', newline='') as csvfile_pnl_nrml:
    csv_writer_pnl_nrml = csv.writer(csvfile_pnl_nrml)

    # Write an empty row to clear the contents
    csv_writer_pnl_nrml.writerow([])

    # Write 20 zeros separated by commas as the first row
    csv_writer_pnl_nrml.writerow(['0'] * 20)
