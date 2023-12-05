import csv
from rich import print
from rich.table import Table

def process_csv(csv_file_path):
    # Set the overall table width
    table_width = 40

    # Specify the index of the last column to include
    last_column_index = 19  # Adjust the index based on the actual position of the "PnL" column in your data

    # Specify the header for printing
    header_for_printing = "PnL"

    # Create a table to display the selected column with custom header
    table = Table(show_header=True, header_style="bold cyan", min_width=table_width)
    table.add_column(header_for_printing, width=10)  # Adjust the width as needed

    # Initialize the total profit variable
    total_profit = 0

    try:
        # Open the CSV file for reading
        with open(csv_file_path, newline='') as csvfile:
            # Create a CSV reader
            csvreader = csv.reader(csvfile)

            # Iterate over each row in the CSV file and add the last column to the table
            for row in csvreader:
                # Skip rows with unexpected number of columns
                if len(row) != last_column_index + 1:
                    print(f"Skipping row with unexpected number of columns: {row}")
                    continue

                # Get the value of the last column ("PnL")
                pnl_value = row[last_column_index]

                # Convert numerical value to string and round it to two decimal places
                pnl_value = str(round(float(pnl_value), 2))

                # Accumulate the total profit
                total_profit += float(pnl_value)

                # Add the last column from the row to the table
                table.add_row(pnl_value)

    except FileNotFoundError:
        print("File not found!")

    # Print the table with the specified column and header
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

