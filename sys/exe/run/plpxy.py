import csv
from tabulate import tabulate

def display_csv_contents(filename, custom_header):
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    # Adjusting headers
    headers = rows[0]
    if 'pnl_y' in headers:
        headers[headers.index('pnl_y')] = 'PnL'
    
    data = rows[1:]
    table = tabulate(data, headers=headers, tablefmt='plain')
    print(f"{custom_header}:")
    print(table)
    print("\n")  # Adding two-line row space

# Display contents of filePnL_nrml.csv
display_csv_contents('filePnL_nrml.csv', custom_header='Options Profits')

# Display contents of filePnL.csv
display_csv_contents('filePnL.csv', custom_header='Stocks Profits')
