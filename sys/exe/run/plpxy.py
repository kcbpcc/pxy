import csv
from tabulate import tabulate

# ANSI color codes for bright green
GREEN = '\033[92m'
RESET = '\033[0m'

def display_csv_contents(filename, custom_header):
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    # Adjusting headers
    headers = rows[0]
    if 'pnl_y' in headers:
        headers[headers.index('pnl_y')] = 'PnL'
    
    data = rows[1:]
    table = tabulate(data, headers=headers, tablefmt='grid')
    
    # Calculate subtotal for PnL
    pnl_column_index = headers.index('PnL')
    pnl_values = [int(row[pnl_column_index]) for row in data]
    subtotal = sum(pnl_values)
    
    # Print table with custom header and subtotal
    print(f"{custom_header}:")
    print(table)
    print(f"Subtotal: {subtotal}")
    print("\n")  # Adding two-line row space
    
    return subtotal

# Display contents of filePnL_nrml.csv
subtotal1 = display_csv_contents('filePnL_nrml.csv', custom_header='Options Profits')

# Display contents of filePnL.csv
subtotal2 = display_csv_contents('filePnL.csv', custom_header='Stocks Profits')

# Calculate and print total of all tables
total = subtotal1 + subtotal2
print(f"{GREEN}Total: {total}{RESET}")
