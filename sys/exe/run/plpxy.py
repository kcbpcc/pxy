import csv

def display_csv_contents(filename):
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

# Display contents of filePnL_nrml.csv
print("Contents of filePnL_nrml.csv:")
display_csv_contents('filePnL_nrml.csv')

# Display contents of filePnL.csv
print("\nContents of filePnL.csv:")
display_csv_contents('filePnL.csv')
