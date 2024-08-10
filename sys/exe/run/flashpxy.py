import pandas as pd
import subprocess
import textwrap  # Make sure this import is included

# Define color code for red
RED = "\033[91m"
RESET = "\033[0m"

# Message to print in red
message = "If you want to exit all you may call my big brother with flashFLASHpxy.py to do the task"

# Wrap the message to fit 40 characters per line
wrapped_message = textwrap.fill(message, width=40)

# Print the wrapped message in red
print(f"{RED}{wrapped_message}{RESET}")

# Define color constants
BRIGHT_YELLOW = '\033[93m'

# Read the CSV file
combined_df = pd.read_csv('pxycombined.csv')

# Filter the DataFrame based on conditions
filtered_df = combined_df[
    (combined_df['product'] == 'CNC') &
    (combined_df['qty'] > 0) &
    (combined_df['PL%'] > 0)
]

# Calculate green stocks profit/loss
green_Stocks_profit_loss = filtered_df['PnL'].sum()

# Calculate green stocks capital percentage
total_invested = filtered_df['Invested'].sum()
if total_invested != 0:
    green_Stocks_capital_percentage = (green_Stocks_profit_loss / total_invested) * 100
else:
    green_Stocks_capital_percentage = 0

# Prompt user for confirmation with color formatting
user_input = input(f"Want to book {BRIGHT_YELLOW}{green_Stocks_profit_loss}{RESET} @ {BRIGHT_YELLOW}{green_Stocks_capital_percentage:.2f}%{RESET}? (Yes/No): ").strip()

# Check if the user input is exactly "Yes" or "No"
if user_input == 'Yes':
    # Call the external script
    subprocess.run(['python', 'cntrlcncpxy.py', '-flash'])
    print("Command executed.")
elif user_input == 'No':
    print("Command not executed.")
else:
    print("Invalid input. Please enter 'Yes' or 'No'.")


