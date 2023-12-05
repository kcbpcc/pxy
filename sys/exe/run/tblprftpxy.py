import csv
from rich import print
from rich.table import Table

def process_csv(csv_file_path):
    # Set the overall table width
    table_width = 40

    # Specify the headers for printing
    headers_for_printing = ['product', 'source', 'key', 'PL%', 'PnL']

    # Create a table to display the selected columns with custom headers
    table = Table(show_header=True, header_style="bold cyan", min_width=table_width)

    # Add the specified columns to the table with custom headers
    for header in headers_for_printing:
        table.add_column(header, width=10)  # Adjust the width as needed

    # Initialize the total profit variable
    total_profit = 0

    try:
        # Open the CSV file for reading
        with open(csv_file_path, newline='') as csvfile:
            # Create a CSV reader
            csvreader = csv.reader(csvfile)

            # Skip the header row
            header_row = next(csvreader)

            # Find the indices of the last 5 columns based on headers_for_printing
            last_columns_indices = [header_row.index(col) for col in headers_for_printing]

            # Iterate over each row in the CSV file and add the last 5 columns to the table
            for row in csvreader:
                # Skip rows with unexpected number of columns
                if len(row) != len(header_row):
                    print(f"Skipping row with unexpected number of columns: {row}")
                    continue

                # Extract values of the last 5 columns
                last_columns_values = [row[idx] for idx in last_columns_indices]

                # Convert numerical values to strings and round them to two decimal places
                last_columns_values = [str(round(float(value), 2)) for value in last_columns_values]

                # Accumulate the total profit
                total_profit += float(last_columns_values[-1])  # Assuming PnL is the last column

                # Add the last 5 columns from the row to the table
                table.add_row(*last_columns_values)

    except FileNotFoundError:
        print("File not found!")

    # Print the table with the specified columns and headers
    print(table)

    # Print the total profit in INR (₹) format rounded to two decimal places
    total_profit = round(total_profit, 2)
    print(f"Total Profit: ₹{total_profit:.2f}")

    # Return the total_profit value
    return total_profit

# Replace "filePnL.csv" with your actual CSV file path
csv_file_path = "filePnL.csv"
# Call the function and get the total_profit value
total_profit_main = process_csv(csv_file_path)

# Now you can use total_profit_main in your main code
# print("Total Profit in Main:", total_profit_main)
