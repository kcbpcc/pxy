import pandas as pd

# Read the CSV file
combined_df = pd.read_csv('pxycombined.csv')

# Filter for exchange 'NFO' and sort by 'PL%' in descending order for optpxy
optpxy_df = combined_df[combined_df['exchange'] == 'NFO']
optpxy_df = optpxy_df[['tradingsymbol', 'unrealised', 'PnL', 'PL%']]
optpxy_df = optpxy_df.rename(columns={'unrealised': 'UNREAL'})  # Rename column
optpxy_df['UNREAL'] = optpxy_df['UNREAL'].astype(int)  # Convert UNREAL to integer
optpxy_df = optpxy_df.sort_values(by='PL%', ascending=False)

# Save the filtered and sorted DataFrame to CSV files
nifty_df = optpxy_df[optpxy_df['tradingsymbol'].str.startswith('NIFTY')]
nifty_df.to_csv('NIFTYOPTS.csv', index=False)

banknifty_df = optpxy_df[optpxy_df['tradingsymbol'].str.startswith('BANKNIFTY')]
banknifty_df.to_csv('BANKNIFTYOPTS.csv', index=False)

print("Files have been created successfully.")
