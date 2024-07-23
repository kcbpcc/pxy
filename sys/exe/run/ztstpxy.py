import sys
import traceback
import pandas as pd
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from toolkit.logger import Logger
import logging

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

def process_data(broker):
    try:
        holdings_response = broker.kite.holdings()
        positions_response = broker.kite.positions()['net']
        
        holdings_df = get_holdingsinfo(holdings_response, broker)
        if holdings_df is not None:
            holdings_df.to_csv('webholdings.csv', index=False)
        
        positions_df = get_positionsinfo(positions_response, broker)
        if positions_df is not None:
            positions_df.to_csv('webpositions.csv', index=False)
        
        # Assuming you need to combine the DataFrames for some reason
        combined_df = pd.concat([holdings_df, positions_df], ignore_index=True) if holdings_df is not None and positions_df is not None else None
        
        return combined_df
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    try:
        sys.stdout = open('output.txt', 'w')
        broker = get_kite()
        
        combined_df = process_data(broker)
        
        # Handle combined_df if necessary
        
    except Exception as e:
        remove_token(dir_path)
        print(traceback.format_exc())
        logging.error(f"{str(e)} unable to get holdings")
        sys.exit(1)
    finally:
        if sys.stdout != sys.__stdout__:
            sys.stdout.close()
            sys.stdout = sys.__stdout__

