import csv
from tabulate import tabulate

def display_csv_contents(filename):
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
    headers = rows[0]
    data = rows[1:]
    table = tabulate(data, headers=headers, tablefmt='pretty')
    print(f"Contents of {filename}:")
    print(table)

# Display contents of filePnL_nrml.csv
display_csv_contents('filePnL_nrml.csv')

# Display contents of filePnL.csv
display_csv_contents('filePnL.csv')
