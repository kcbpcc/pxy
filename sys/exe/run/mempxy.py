import csv

# ANSI escape codes for text formatting
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Specify the CSV file name
file_name = 'mempxy.csv'

# Read the current value from the CSV file
try:
    with open(file_name, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            current_auto_value = row.get('AUTO', 'MANUAL')  # Default to 'MANUAL' if 'AUTO' is not found
except FileNotFoundError:
    current_auto_value = 'MANUAL'  # Assume 'MANUAL' if the file doesn't exist

# Display the current value in red
print(f'AUTO from {file_name}: {RED}{current_auto_value}{RESET}')

# Toggle between 'AUTO' and 'MANUAL'
new_auto_value = 'AUTO' if current_auto_value == 'MANUAL' else 'MANUAL'

# Prompt the user to confirm the change
user_confirmation = input(f"toggle AUTO value to '{new_auto_value}'? Enter 'Y' to confirm or any other key to cancel: ").upper()

# Update the value if the user confirms the change
if user_confirmation == 'Y':
    try:
        with open(file_name, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['AUTO'])
            writer.writeheader()
            writer.writerow({'AUTO': new_auto_value})

        # Print the changed value in green
        print(f'{file_name} AUTO toggled to {GREEN}{new_auto_value}{RESET}.')
    except Exception as e:
        print(f'Error updating {file_name}: {e}')
else:
    print(f'{file_name} remains unchanged. AUTO is still set to {current_auto_value}.')


