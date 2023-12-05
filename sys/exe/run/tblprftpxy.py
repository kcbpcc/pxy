import csv
from rich import print
from rich.table import Table

def process_csv(csv_file_path):
    # Set the overall table width
    table_width = 40

    # Specify the indices of columns to include
    included_columns = [1, 3, 1, 1, 1]  # Adjust the indices based on the actual positions of columns in your data

    # Create a table to display the selected columns with custom headers
    table = Table(show_header=True, header_style="bold cyan", min_width=table_width)

    # Add the specified columns to the table with custom headers
    headers_for_printing = ["Product", "Source", "Key", "aPL%", "PnL"]
    for column_index, header in zip(included_columns, headers_for_printing):
        table.add_column(header, width=10)  # Adjust the width as needed

    # Initialize the total profit variable
    total_profit = 0

    try:
        # Open the CSV file for reading
        with open(csv_file_path, newline='') as csvfile:
            # Create a CSV reader
            csvreader = csv.reader(csvfile)

            # Iterate over each row in the CSV file and add it to the table
            for row in csvreader:
                # Adjust column indices to match your CSV file structure
                if len(row) == len(included_columns):
                    # Convert numerical values to strings and round them to two decimal places
                    row = [str(round(float(row[column_index]), 2)) for column_index in included_columns]

                    # Accumulate the total profit
                    total_profit += float(row[-1])  # Assuming PnL is the last column

                    # Add the specified columns from the row to the table
                    table.add_row(*row)

                else:
                    # Handle cases where the number of columns is different
                    print(f"Skipping row with unexpected number of columns: {row}")
                    continue

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
