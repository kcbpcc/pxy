import csv
from tabulate import tabulate

def display_csv_contents(filename, table_format, custom_header):
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
    headers = rows[0]
    data = rows[1:]
    table = tabulate(data, headers=headers, tablefmt=table_format)
    print(f"{custom_header}:")
    print(table)

# Display contents of filePnL_nrml.csv
display_csv_contents('filePnL_nrml.csv', table_format='plain', custom_header='Contents of filePnL_nrml.csv: Options Profits')

# Display contents of filePnL.csv
display_csv_contents('filePnL.csv', table_format='plain', custom_header='Contents of filePnL.csv: Stocks Profits')
