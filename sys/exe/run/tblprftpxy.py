import csv
from rich import print
from rich.table import Table

def process_csv(csv_file_path, ORDER_df):
    # Set the overall table width
    table_width = 40

    # Create a table to display all columns with custom headers
    table = Table(show_header=True, header_style="bold cyan", min_width=table_width)
    table.add_column("Source")
    table.add_column("Product")
    table.add_column("Qty")
    table.add_column("Key")
    table.add_column("Smbchk")
    table.add_column("Yxp")
    table.add_column("Pxy")
    table.add_column("DPL%")
    table.add_column("OPL%")
    table.add_column("APL%")

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
                    source, product, qty, key, smbchk, yxp, pxy, dPL, oPL, aPL, *rest = row
                else:
                    # Handle cases where the number of columns is different
                    print(f"Skipping row with unexpected number of columns: {row}")
                    continue

                # Remove "NSE:" or "BSE:" prefix from the "Key" column
                key = key.replace("NSE:", "").replace("BSE:", "")

                # Convert numerical values to strings and round them to two decimal places
                dPL = str(round(float(dPL), 2))
                oPL = str(round(float(oPL), 2))
                aPL = str(round(float(aPL), 2))

                # Accumulate the total profit
                total_profit += float(aPL)

                # Add the row to the table
                table.add_row(source, product, qty, key, smbchk, yxp, pxy, dPL, oPL, aPL)

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
# Replace ORDER_df with your actual DataFrame
ORDER_df = pxy_df[['source','product','qty','key','smbchk','yxp','pxy','dPL%','oPL%','aPL%']]
# Call the function and get the total_profit value
total_profit_main = process_csv(csv_file_path, ORDER_df)

# Now you can use total_profit_main in your main code
# print("Total Profit in Main:", total_profit_main)




