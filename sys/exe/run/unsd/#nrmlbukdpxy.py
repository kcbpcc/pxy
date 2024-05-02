import csv

def sum_last_numerical_value_in_each_row_nrml(csv_file_nrml):
    total_sum = 0

    with open(csv_file_nrml, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                last_value = row[-1].strip()  # Use strip to remove leading/trailing whitespaces
                try:
                    numerical_value = float(last_value)
                    # Ignore negative values in the last column
                    if numerical_value >= 0:
                        total_sum += numerical_value
                except ValueError:
                    # Ignore non-numeric values in the last column
                    pass

    return total_sum

# Replace 'filePnL_nrml.csv' with the path to your actual CSV file
file_path_nrml = 'filePnL_nrml.csv'
result_nrml = sum_last_numerical_value_in_each_row_nrml(file_path_nrml)

#print(f"Extras: {result}")
