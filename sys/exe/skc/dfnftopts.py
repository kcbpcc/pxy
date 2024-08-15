import sys
import traceback
import pandas as pd
import os
import logging

from toolkit.logger import Logger
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path

# Setup logging
logging.basicConfig(filename=dir_path + "main.log", level=logging.INFO)

def get_positionsinfo(resp_list):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'positions'
        return df
    except Exception as e:
        logging.error(f"An error occurred in positions: {e}")
        return None

try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite()
except Exception as e:
    remove_token(dir_path)
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)
finally:
    # Ensure to close the file and restore stdout
    if sys.stdout != sys.__stdout__:
        sys.stdout.close()
        sys.stdout = sys.__stdout__

def process_data():
    try:
        positions_response = broker.kite.positions()['net']
        positions_df = get_positionsinfo(positions_response)
        
        if positions_df is not None:
            # Filter by exchange 'NFO' and tradingsymbol starting with 'NFTY'
            niftyoptions_df = positions_df[
                (positions_df['exchange'] == 'NFO') & 
                (positions_df['tradingsymbol'].str.startswith('NFTY'))
            ]

            # Select only the required columns
            niftyoptions_df = niftyoptions_df[['tradingsymbol', 'quantity', 'average_price', 'pnl']]
            
            # Rename columns to match desired output
            niftyoptions_df.rename(columns={
                'quantity': 'qty',
                'average_price': 'Invested',
                'pnl': 'PnL'
            }, inplace=True)

            # Calculate 'Invested' and 'PL%'
            niftyoptions_df['Invested'] = (niftyoptions_df['qty'] * niftyoptions_df['Invested']).round(0).astype(int)
            niftyoptions_df['PnL'] = niftyoptions_df['PnL'].round(2)
            niftyoptions_df['PL%'] = ((niftyoptions_df['PnL'] / niftyoptions_df['Invested']) * 100).round(2)
            
            # Save the final DataFrame to CSV
            niftyoptions_df.to_csv('pxypositions_filtered.csv', index=False)
            print("Filtered and Final DataFrame:")
            print(niftyoptions_df)
        else:
            logging.error("No positions data to display.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        traceback.print_exc()

# Call the function to process data
process_data()

