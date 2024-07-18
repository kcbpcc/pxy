import csv

def read_csv_and_sum(filename):
    first_columns = []
    last_columns = []
    total_sum = 0

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip the header row
        for row in reader:
            if row:  # Check if row is not empty
                first_columns.append(row[0])
                try:
                    last_columns.append(int(row[-1]))  # Convert last column to integer
                except ValueError:
                    print(f"Warning: Non-numeric value found in last column: {row[-1]}")

    max_first_col_width = max(len(str(first)) for first in first_columns)
    max_last_col_width = max(len(str(last)) for last in last_columns)
    
    for first, last in zip(first_columns, last_columns):
        print(f"{first.ljust(max_first_col_width)}: {str(last).rjust(max_last_col_width)}")
        total_sum += last

    print(f"\nSubtotal: {total_sum}\n")
    return total_sum

# File paths
pxycncprofit_file = 'pxycncprofit.csv'
pxyoptprofit_file = 'pxyoptprofit.csv'

# Reading and processing pxycncprofit.csv
print("C&C Profits")
subtotal_cnc = read_csv_and_sum(pxycncprofit_file)

# Reading and processing pxyoptprofit.csv
print("F&0 Profits")
subtotal_opt = read_csv_and_sum(pxyoptprofit_file)

# Calculating total sum
total_sum = subtotal_cnc + subtotal_opt
print(f"Total Sum: {total_sum}")
