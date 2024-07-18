import csv

def read_csv_and_sum(filename):
    first_columns = []
    last_columns = []
    total_sum = 0

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Check if row is not empty
                first_columns.append(row[0])
                last_columns.append(float(row[-1]))  # Assuming last column contains numbers
    
    for first, last in zip(first_columns, last_columns):
        print(f"{first}: {last}")
        total_sum += last
    
    print(f"\nTotal Sum: {total_sum}")

# File paths
pxycncprofit_file = 'pxycncprofit.csv'
pxyoptprofit_file = 'pxyoptprofit.csv'

# Reading and processing pxycncprofit.csv
print("Reading pxycncprofit.csv:")
read_csv_and_sum(pxycncprofit_file)

# Reading and processing pxyoptprofit.csv
print("\nReading pxyoptprofit.csv:")
read_csv_and_sum(pxyoptprofit_file)
