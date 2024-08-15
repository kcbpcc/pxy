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
            positions_df.to_csv('pxypositions.csv', index=False)
            print("Positions DataFrame:")
            print(positions_df)
        else:
            logging.error("No positions data to display.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        traceback.print_exc()

# Call the function to process data
process_data()
