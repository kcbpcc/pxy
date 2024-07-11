import pandas as pd

# Read the CSV files
hp_df = pd.read_csv('fileHPdf.csv')
ord_df = pd.read_csv('fileORDdf.csv')

# Rename columns to avoid confusion
hp_df = hp_df.add_prefix('hp_')
ord_df = ord_df.add_prefix('ord_')

# Remove the prefix from the 'tradingsymbol' column to match it for merging
hp_df = hp_df.rename(columns={'hp_tradingsymbol': 'tradingsymbol'})
ord_df = ord_df.rename(columns={'ord_tradingsymbol': 'tradingsymbol'})

# Merge the dataframes based on 'tradingsymbol'
merged_df = pd.merge(hp_df, ord_df, on='tradingsymbol', how='left')

# Dump the merged dataframe to a CSV file
merged_df.to_csv('merged_result.csv', index=False)

print("Merged dataframe has been saved to 'merged_result.csv'")

