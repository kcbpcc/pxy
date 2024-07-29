import csv
import io
import sys
from telsumrypxy import check_and_send_summary
from datetime import datetime
import os

# Get the current datetime
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def trim_first_column(value):
    if value.startswith('BANKNIFTY24'):
        return 'B' + value.replace('BANKNIFTY24', '')
    elif value.startswith('NIFTY24'):
        return 'N' + value.replace('NIFTY24', '')
    return value

def read_csv_and_sum(filename):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        print(f"File '{filename}' is empty or does not exist.")
        return 0, []

    first_columns = []
    last_columns = []
    entries = []
    total_sum = 0

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip the header row
        for row in reader:
            if row:  # Check if row is not empty
                trimmed_first_col = trim_first_column(row[0])
                try:
                    profit = float(row[-1])  # Convert last column to float
                    first_columns.append(trimmed_first_col)
                    last_columns.append(profit)
                    entry = f"{trimmed_first_col}: {profit:.2f}"
                    entries.append(entry)
                    total_sum += profit
                except ValueError:
                    print(f"Warning: Non-numeric value found in last column: {row[-1]}")

    if first_columns and last_columns:
        max_first_col_width = max(len(str(first)) for first in first_columns)
        max_last_col_width = max(len(str(last)) for last in last_columns)

        for first, last in zip(first_columns, last_columns):
            print(f"{first.ljust(max_first_col_width)}: {str(last).rjust(max_last_col_width)}")

    print(f"\nSubtotal: {total_sum:.2f}\n")  # Format subtotal to 2 decimal places
    return total_sum, entries

# Capture the output in a StringIO object
output = io.StringIO()
sys.stdout = output

# File paths
pxycncprofit_file = 'pxycncprofit.csv'
pxyoptprofit_file = 'pxyoptprofit.csv'

# Reading and processing pxycncprofit.csv
print("---------PXY® Score Board--------")
print("PreciseXceleratedYield Pvt Ltd")
print("******************************")

print("💵C&C Profits💵")
subtotal_cnc, cnc_entries = read_csv_and_sum(pxycncprofit_file)

# Reading and processing pxyoptprofit.csv
print("💸F&O Profits💸")
subtotal_opt, opt_entries = read_csv_and_sum(pxyoptprofit_file)

# Calculating total sum
total_sum = subtotal_cnc + subtotal_opt

print(f"💰💰💰 Total Sum: {total_sum:.2f}")  # Format total sum to 2 decimal places
print("******************************")
print("[---------PXY® Dash Board----------](https://console.zerodha.com/verified/783d6dad)")

# Reset stdout
sys.stdout = sys.__stdout__

# Get the captured output
profitinfo = output.getvalue()
output.close()

# Prepare Telegram message
telegram_message = (
    f"🚀 *PXY® Score Board* 🚀\n\n"
    f"🔹 *PreciseXceleratedYield Pvt Ltd* 🔹\n\n"
    f"💵 *C&C Profits* 💵\n"
    + "\n".join(cnc_entries) + f"\n\n"
    f"💸 *F&O Profits* 💸\n"
    + "\n".join(opt_entries) + f"\n\n"
    f"💰💰💰 *Total Sum:* {total_sum:.2f}\n\n"
    f"🔗 [PXY® Dash Board](https://console.zerodha.com/verified/783d6dad)"
)

# Print detailed entries to console
print("\nDetailed Entries Preview:\n")
print(telegram_message)

# Send the summary
check_and_send_summary(telegram_message, 'plpxy')

