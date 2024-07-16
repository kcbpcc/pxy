import csv
from tabulate import tabulate

# ANSI color codes
YELLOW = '\033[93m'  # Bright yellow
RESET = '\033[0m'    # Reset color

#print("\n")

def display_csv_contents(filename, custom_header=''):
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)

            if not rows:  # Check if the file is empty
                print(f"{custom_header}: The file '{filename}' is empty.")
                return 0
            
            # Adjusting headers
            headers = rows[0]
            if 'pnl_y' in headers:
                headers[headers.index('pnl_y')] = 'PnL'
            
            data = rows[1:]
            
            # Check if there's data beyond headers
            if not data:
                print(f"{custom_header}🫙 Nothing has been booked yet in C&C...🫙")
                return 0
            
            # Calculate column widths
            col_widths = [max(len(str(row[i])) for row in data) + 2 for i in range(len(headers))]
            
            # Format table without headers
            table = tabulate(data, headers=[], tablefmt='plain')
            
            # Calculate subtotal for PnL
            pnl_column_index = headers.index('PnL')
            pnl_values = [int(row[pnl_column_index]) for row in data]
            subtotal = sum(pnl_values)
            
            # Print table with custom header and subtotal
            if custom_header:
                print(f"{custom_header}:")
            print(table)
            print(f"                           {YELLOW}Subtotal:{subtotal}{RESET}")
            print("\n")  # Adding two-line row space
            
            return subtotal
    except FileNotFoundError:
        print(f"{custom_header}🫙 Nothing has been booked yet in F&O...🫙")
        return 0
    except Exception as e:
        print(f"{custom_header}: An error occurred while processing the file '{filename}': {e}")
        return 0

# Display contents of filePnL_nrml.csv
subtotal1 = display_csv_contents('filePnL_nrml.csv')

# Display contents of filePnL.csv
subtotal2 = display_csv_contents('filePnL.csv')

# Calculate and print total of all tables
total = subtotal1 + subtotal2
print(f"\033[92m                              Total:{total}\033[0m")
#print("\n")

