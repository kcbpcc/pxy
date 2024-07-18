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

    for first, last in zip(first_columns, last_columns):
        print(f"{first}: {last}")
        total_sum += last

    print(f"Subtotal for {filename}: {total_sum}\n")
    return total_sum

# File paths
pxycncprofit_file = 'pxycncprofit.csv'
pxyoptprofit_file = 'pxyoptprofit.csv'

# Reading and processing pxycncprofit.csv
print("Reading pxycncprofit.csv:")
subtotal_cnc = read_csv_and_sum(pxycncprofit_file)

# Reading and processing pxyoptprofit.csv
print("Reading pxyoptprofit.csv:")
subtotal_opt = read_csv_and_sum(pxyoptprofit_file)

# Calculating total sum
total_sum = subtotal_cnc + subtotal_opt
print(f"Total Sum: {total_sum}")
