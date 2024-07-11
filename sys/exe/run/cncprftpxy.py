import pandas as pd

# Read the CSV files
hp_df = pd.read_csv('fileHPdf.csv')
ord_df = pd.read_csv('fileORDdf.csv')

# Display the column names to check for discrepancies
print("Columns in fileHPdf.csv:", hp_df.columns)
print("Columns in fileORDdf.csv:", ord_df.columns)

# Filter rows where product is 'CNC' and qty is negative
cnc_df = hp_df[(hp_df['product'] == 'CNC') & (hp_df['qty'] < 0)].copy()

# Convert qty to positive
cnc_df['qty'] = cnc_df['qty'].abs()

# Verify the columns before merging
print("Filtered CNC DataFrame:\n", cnc_df.head())

# Merge with ord_df to get the average_price for the corresponding tradingsymbol
merged_df = pd.merge(cnc_df, ord_df[['tradingsymbol']], on='tradingsymbol', how='left', suffixes=('', '_ord'))

# Verify the merged DataFrame
print("Merged DataFrame:\n", merged_df.head())

# Check if 'average_price_ord' column exists in the merged DataFrame
if 'average_price_ord' not in merged_df.columns:
    raise KeyError("The column 'average_price_ord' does not exist in the merged DataFrame. Please check your input files.")

# Check if 'avg' column exists in the hp_df before the merge
if 'avg' not in hp_df.columns:
    raise KeyError("The column 'avg' does not exist in the hp_df. Please check your input files.")

# Calculate sold_amount and investment
merged_df['sold_amount'] = merged_df['qty'] * merged_df['average_price_ord']
merged_df['investment'] = merged_df['qty'] * merged_df['avg']  # Using 'avg' column from hp_df

# Calculate profit
merged_df['profit'] = merged_df['sold_amount'] - merged_df['investment']

# Display the result
print(merged_df[['tradingsymbol', 'qty', 'average_price_ord', 'sold_amount', 'investment', 'profit']])

# If you want to save the result to a CSV file
merged_df.to_csv('result.csv', index=False)
