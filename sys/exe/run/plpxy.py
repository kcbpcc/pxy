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
    
    # Printing table with custom header and underlines
    print(f"{custom_header}:")
    print(table)
    
    # Calculate subtotal and total for PnL
    pnl_column_index = headers.index('PnL')
    pnl_values = [int(row[pnl_column_index]) for row in data]
    subtotal = sum(pnl_values)
    total = sum(pnl_values)
    
    # Print subtotals
    print(f"Subtotal: {subtotal}")
    print(f"Total: {total}")
    
    # Add an underline
    print(f"{'-' * len(custom_header)}")
    print("\n")  # Adding two-line row space

# Display contents of filePnL_nrml.csv
display_csv_contents('filePnL_nrml.csv', custom_header='Options Profits')

# Display contents of filePnL.csv
display_csv_contents('filePnL.csv', custom_header='Stocks Profits')
