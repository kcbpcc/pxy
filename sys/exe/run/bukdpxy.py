import csv

def sum_last_numerical_value_in_each_row(csv_file):
    total_sum = 0

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                last_value = row[-1].strip()  # Use strip to remove leading/trailing whitespaces
                try:
                    numerical_value = float(last_value)
                    total_sum += numerical_value
                except ValueError:
                    # Ignore non-numeric values in the last column
                    pass

    return total_sum

# Replace 'filePnL.csv' with the path to your actual CSV file
file_path = 'filePnL.csv'
result = sum_last_numerical_value_in_each_row(file_path)

print(f"Booked Profit: {result}")
