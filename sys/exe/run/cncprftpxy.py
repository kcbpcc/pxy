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

# Save the result to a new CSV file
common_entries_df.to_csv('common_entries.csv', index=False)

print("Filtered entries have been saved to 'common_entries.csv'")
