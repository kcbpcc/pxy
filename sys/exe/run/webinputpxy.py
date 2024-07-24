import pandas as pd

# Read the CSV files
combined_df = pd.read_csv('pxycombined.csv')
merged_df = pd.read_csv('pxymergedcsv.csv')

# Select specific columns (replace 'column1', 'column2', etc. with actual column names)
selected_columns_combined = combined_df[['tradingsymbol', 'PnL', 'PL%']]
selected_columns_merged = merged_df[['tradingsymbol', 'PnL', 'PL%']]
# Write the selected columns to new CSV files
selected_columns_combined.to_csv('optpxy.csv', index=False)
selected_columns_merged.to_csv('cncpxy.csv', index=False)

print("Files have been created successfully.")
