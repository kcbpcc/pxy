import csv
from tabulate import tabulate

# ANSI color codes
YELLOW = '\033[93m'  # Bright yellow
RESET = '\033[0m'    # Reset color
print("\n")
def display_csv_contents(filename, custom_header):
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    # Adjusting headers
    headers = rows[0]
    if 'pnl_y' in headers:
        headers[headers.index('pnl_y')] = 'PnL'
    
    data = rows[1:]
    
    # Calculate column widths
    col_widths = [max(len(str(row[i])) for row in [headers] + data) + 2 for i in range(len(headers))]
    
    # Format table
    table = tabulate(data, headers=headers, tablefmt='plain')
    
    # Calculate subtotal for PnL
    pnl_column_index = headers.index('PnL')
    pnl_values = [int(row[pnl_column_index]) for row in data]
    subtotal = sum(pnl_values)
    
    # Print table with custom header and subtotal
    print(f"{custom_header}:")
    print(table)
    print(f"                           {YELLOW}Subtotal: {subtotal}{RESET}")
    print("\n")  # Adding two-line row space
    
    return subtotal

# Display contents of filePnL_nrml.csv
subtotal1 = display_csv_contents('filePnL_nrml.csv', custom_header='123')

# Display contents of filePnL.csv
subtotal2 = display_csv_contents('filePnL.csv', custom_header='233')

# Calculate and print total of all tables
total = subtotal1 + subtotal2
print(f"\033[92mTotal:                            {total}\033[0m")
print("\n")

