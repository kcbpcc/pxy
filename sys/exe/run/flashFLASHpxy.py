import pandas as pd
import subprocess
import getpass

# Define color constants
BRIGHT_YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

# Define the correct password
CORRECT_PASSWORD = '089608'

# Disclaimer text
DISCLAIMER = (
    "DISCLAIMER: You are about to exit all stocks that are currently at a loss. "
    "Please review your portfolio and ensure that this decision aligns with your investment strategy. "
    "Once executed, this action cannot be undone."
)

# Print disclaimer text in red
print(f"{RED}{DISCLAIMER}{RESET}")

# Prompt user for password
password = getpass.getpass("Enter password: ")

# Check if the password is correct
if password != CORRECT_PASSWORD:
    print("Incorrect password. Exiting.")
    exit()

# Read the CSV file
combined_df = pd.read_csv('pxycombined.csv')

# Filter the DataFrame based on conditions
filtered_df = combined_df[
    (combined_df['product'] == 'CNC') &
    (combined_df['qty'] > 0)
]

# Calculate green stocks profit/loss
green_Stocks_profit_loss = filtered_df['PnL'].sum()

# Calculate green stocks capital percentage
total_invested = filtered_df['Invested'].sum()
if total_invested != 0:
    green_Stocks_capital_percentage = (green_Stocks_profit_loss / total_invested) * 100
else:
    green_Stocks_capital_percentage = 0

# Format each row to fit within 40 spaces
def format_row(pnl, percentage):
    row = f"Profit/Loss: {pnl:<20} Capital %: {percentage:>19.2f}%"
    return row.ljust(40)  # Ensure each row has a total width of 40 spaces

# Print formatted output
formatted_output = format_row(green_Stocks_profit_loss, green_Stocks_capital_percentage)
print(formatted_output)

# Prompt user for initial confirmation with color formatting
initial_input = input(f"Want to book {BRIGHT_YELLOW}{green_Stocks_profit_loss}{RESET} @ {BRIGHT_YELLOW}{green_Stocks_capital_percentage:.2f}%{RESET}? (Yes/No): ").strip()

# Check if the user input is exactly "Yes" or "No"
if initial_input == 'Yes':
    # Additional confirmation step
    final_confirmation = input("Are you sure you want to proceed with exiting all stocks with a loss? This action cannot be undone. (Yes/No): ").strip()
    
    if final_confirmation == 'Yes':
        # Call the external script with the updated argument
        subprocess.run(['python', 'cntrlcncpxy.py', '-flashFLASH'])
        print("Command executed.")
    elif final_confirmation == 'No':
        print("Action canceled.")
    else:
        print("Invalid input. Please enter 'Yes' or 'No'.")
elif initial_input == 'No':
    print("Command not executed.")
else:
    print("Invalid input. Please enter 'Yes' or 'No'.")
