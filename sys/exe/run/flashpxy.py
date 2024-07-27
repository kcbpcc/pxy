import pandas as pd
import subprocess

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

# Print the results
print(f"Green Stocks Profit/Loss: {green_Stocks_profit_loss}")
print(f"Green Stocks Capital Percentage: {green_Stocks_capital_percentage:.2f}%")

# Prompt user for confirmation
user_input = input("Do you want to execute 'cntrlpxy.py -flash'? (Yes/No): ").strip().lower()

if user_input == 'yes':
    # Call the external script
    subprocess.run(['python', 'cntrlpxy.py', '-flash'])
    print("Command executed.")
else:
    print("Command not executed.")
