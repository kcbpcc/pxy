import pandas as pd

# Read the CSV file
hp_df = pd.read_csv('fileHPdf.csv')

# Separate the rows based on the 'source' column
holdings_df = hp_df[hp_df['source'] == 'holdings']
positions_df = hp_df[hp_df['source'] == 'positions']

# Find the common 'tradingsymbol' in both dataframes
common_symbols = set(holdings_df['tradingsymbol']).intersection(set(positions_df['tradingsymbol']))

# Filter the original dataframe to get the entries where 'tradingsymbol' exists in both sources
common_entries_df = hp_df[hp_df['tradingsymbol'].isin(common_symbols)]

# Initialize an empty list to store profit calculations
profit_list = []

# Iterate over each common symbol and calculate profit
for symbol in common_symbols:
    holdings = holdings_df[holdings_df['tradingsymbol'] == symbol]
    positions = positions_df[positions_df['tradingsymbol'] == symbol]

    # Calculate total investment from holdings
    holdings_qty = holdings['quantity'].sum()
    holdings_avg_price = holdings['average_price'].mean()  # Assuming the average price is consistent
    total_investment = holdings_qty * holdings_avg_price

    # Calculate total sold amount from positions
    positions_qty = positions['quantity'].abs().sum()
    positions_avg_price = positions['average_price'].mean()  # Assuming the average price is consistent
    total_sold_amount = positions_qty * positions_avg_price

    # Calculate profit
    profit = total_sold_amount - total_investment

    # Append to the profit list
    profit_list.append({
        'tradingsymbol': symbol,
        'holdings_qty': holdings_qty,
        'holdings_avg_price': holdings_avg_price,
        'total_investment': total_investment,
        'positions_qty': positions_qty,
        'positions_avg_price': positions_avg_price,
        'total_sold_amount': total_sold_amount,
        'profit': profit
    })

# Convert the profit list to a DataFrame
profit_df = pd.DataFrame(profit_list)

# Save the profit calculations to a new CSV file
profit_df.to_csv('profit_calculations.csv', index=False)

print("Profit calculations have been saved to 'profit_calculations.csv'")
