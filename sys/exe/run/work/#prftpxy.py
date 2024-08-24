import csv
from rich import print
from rich.table import Table

def process_csv(csv_file_path):
    # Set the overall table width
    table_width = 30

    # Specify the headers for printing
    headers_for_printing = ['product', 'source', 'key', 'PL%', 'PnL']

    # Create a table to display the selected columns with custom headers
    table = Table(show_header=True, header_style="bold cyan", min_width=table_width)

    # Define specific column widths
    column_widths = {'product': 2, 'source': 2, 'key': 8, 'PL%': 6, 'PnL': 8}

    # Add the specified columns to the table with custom headers and width
    for header in headers_for_printing:
        if header in ['PL%', 'PnL']:
            # Align 'PL%' and 'PnL' columns to the right
            table.add_column(header, width=column_widths[header], justify='right')
        else:
            table.add_column(header, width=column_widths[header])

    # Initialize the total profit variable
    total_profit = 0

    try:
        # Open the CSV file for reading
        with open(csv_file_path, newline='') as csvfile:
            # Create a CSV reader
            csvreader = csv.reader(csvfile)

            # Iterate over each row in the CSV file and add the last 5 columns to the table
            for row in csvreader:
                # Skip empty rows
                if not row:
                    continue

                # Skip rows with unexpected number of columns
                if len(row) < len(headers_for_printing):
                    # Optionally, you can choose to print a message here if needed
                    continue

                # Extract values of the last 5 columns
                last_columns_values = row[-5:]

                # Convert numerical values to strings and round them to two decimal places
                processed_values = []
                for idx, value in enumerate(last_columns_values):
                    try:
                        processed_value = str(round(float(value), 2))
                    except ValueError:
                        processed_value = value  # Keep non-numeric values as they are

                    # Remove prefixes "BSE:" or "NSE:" from the 'key' column
                    if headers_for_printing[idx] == 'key':
                        processed_value = processed_value.replace('BSE:', '').replace('NSE:', '')

                    processed_values.append(processed_value)

                # Accumulate the total profit
                try:
                    total_profit += float(processed_values[-1])  # Assuming PnL is the last column
                except ValueError:
                    # Handle the case where the total profit value cannot be converted to float
                    print(f"Warning: Unable to convert total profit value '{processed_values[-1]}' to float.")

                # Add the last 5 columns from the row to the table
                table.add_row(*processed_values)

    except FileNotFoundError:
        print("File not found!")

    # Print the table with the specified columns and headers
    print(table)

    # Print the total profit in INR (₹) format rounded to two decimal places
    total_profit = round(total_profit, 2)
    print(f"Booked: ₹{total_profit:.2f}".rjust(40))

    # Return the total_profit value
    return total_profit

# Replace "filePnL.csv" with your actual CSV file path
csv_file_path = "filePnL.csv"
# Call the function and get the total_profit value
total_profit_main = process_csv(csv_file_path)

# Now you can use total_profit_main in your main code
# print("Total Profit in Main:", total_profit_main)
