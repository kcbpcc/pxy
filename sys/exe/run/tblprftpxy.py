import csv
from rich import print
from rich.table import Table

def process_csv(csv_file_path):
    # Set the overall table width
    table_width = 40

    # Create a table to display the selected columns with custom headers
    table = Table(show_header=True, header_style="bold cyan", min_width=table_width)
    table.add_column("Product", width=3)
    table.add_column("Source", width=3)
    table.add_column("Key", width=10)
    table.add_column("PnL%")
    table.add_column("PnL")

    # Initialize the total profit variable
    total_profit = 0

    try:
        # Open the CSV file for reading
        with open(csv_file_path, newline='') as csvfile:
            # Create a CSV reader
            csvreader = csv.reader(csvfile)

            # Skip the header row
            header_row = next(csvreader)

            # Iterate over each row in the CSV file and add it to the table
            for row in csvreader:
                # Adjust column names to match your CSV file structure
                if len(row) == 16:
                    qty, avg, close, ltp, open_price, high, low, pnl_h, dpnl, CM, PH, key, pxy, yxp, pnl_percentage, pnl = row
                else:
                    # Handle cases where the number of columns is different
                    print(f"Skipping row with unexpected number of columns: {row}")
                    continue

                # Remove "NSE:" or "BSE:" prefix from the "Key" column
                key = key.replace("NSE:", "").replace("BSE:", "")

                # Convert numerical values to strings and round them to two decimal places
                pnl_percentage = str(round(float(pnl_percentage), 2))
                pnl = str(round(float(pnl), 2))

                # Accumulate the total profit
                total_profit += float(pnl)

                # Add the row to the table
                table.add_row(CM, PH, key, pnl_percentage, pnl)

    except FileNotFoundError:
        print("File not found!")

    # Print the table with the updated column names
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





