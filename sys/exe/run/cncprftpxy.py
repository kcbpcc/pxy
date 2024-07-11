import pandas as pd

# Read the CSV files
hp_df = pd.read_csv('fileHPdf.csv')
ord_df = pd.read_csv('fileORDdf.csv')

# Filter rows where product is 'CNC' and qty is negative
cnc_df = hp_df[(hp_df['product'] == 'CNC') & (hp_df['qty'] < 0)].copy()

# Convert qty to positive
cnc_df['qty'] = cnc_df['qty'].abs()

# Merge with ord_df to get the average_price for the corresponding tradingsymbol
merged_df = pd.merge(cnc_df, ord_df[['tradingsymbol', 'average_price']], on='tradingsymbol', how='left')

# Calculate sold_amount and investment
merged_df['sold_amount'] = merged_df['qty'] * merged_df['average_price']
merged_df['investment'] = merged_df['qty'] * merged_df['avg']  # Assuming 'avg' column exists in hp_df

# Calculate profit
merged_df['profit'] = merged_df['sold_amount'] - merged_df['investment']

# Display the result
print(merged_df[['tradingsymbol', 'qty', 'average_price', 'sold_amount', 'investment', 'profit']])

# If you want to save the result to a CSV file
merged_df.to_csv('result.csv', index=False)
