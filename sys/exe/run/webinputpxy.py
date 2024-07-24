import pandas as pd

# Read the CSV file
combined_df = pd.read_csv('pxycombined.csv')

# Filter for exchange 'BSE' or 'NSE' and sort by 'PL%' in descending order for cncpxy
cncpxy_df = combined_df[(combined_df['exchange'].isin(['BSE', 'NSE']))]
cncpxy_df = cncpxy_df[['tradingsymbol','oPL%','dPL%', 'PnL', 'PL%']].sort_values(by='PL%', ascending=False)
cncpxy_df.to_csv('cncpxy.csv', index=False)

# Filter for exchange 'NFO' and sort by 'PL%' in descending order for optpxy
optpxy_df = combined_df[combined_df['exchange'] == 'NFO']
optpxy_df = optpxy_df[['tradingsymbol', 'unrealised', 'PnL', 'PL%']].sort_values(by='PL%', ascending=False)
optpxy_df.to_csv('optpxy.csv', index=False)

print("Files have been created successfully.")
