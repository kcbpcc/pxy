# main.py

import sys
import traceback
import pandas as pd
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from toolkit.logger import Logger

# Define logging
logging = Logger(30, dir_path + "main.log")

def get_holdingsinfo(resp_list, broker):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'holdings'
        return df
    except Exception as e:
        print(f"An error occurred in holdings: {e}")
        return None

def get_positionsinfo(resp_list, broker):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'positions'
        return df
    except Exception as e:
        print(f"An error occurred in positions: {e}")
        return None

def process_data():
    try:
        broker = get_kite()
        holdings_response = broker.kite.holdings()
        positions_response = broker.kite.positions()['net']
        holdings_df = get_holdingsinfo(holdings_response, broker)
        positions_df = get_positionsinfo(positions_response, broker)

        # Ensure there are keys for merging
        holdings_df['key'] = holdings_df['exchange'] + ":" + holdings_df['tradingsymbol'] if not holdings_df.empty else None
        positions_df['key'] = positions_df['exchange'] + ":" + positions_df['tradingsymbol'] if not positions_df.empty else None

        # Merge holdings and positions dataframes on 'key'
        merged_df = pd.merge(holdings_df, positions_df, on='key', how='outer', suffixes=('_h', '_p'))

        # Additional prefixing of columns
        merged_df = merged_df.add_prefix('h_')
        merged_df = merged_df.add_prefix('p_')

        return merged_df

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return None

def save_to_csv(df, filename):
    try:
        df.to_csv(filename, index=False)
        print(f"Dataframe saved to {filename}")
    except Exception as e:
        print(f"Error saving dataframe to CSV: {e}")
        traceback.print_exc()

def main():
    try:
        result_df = process_data()
        
        if result_df is not None:
            # Print the result to console
            print("Merged and prefixed dataframe:")
            print(result_df)

            # Save the result to a CSV file
            save_to_csv(result_df, 'output.csv')

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()

