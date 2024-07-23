import sys
import traceback
import pandas as pd
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from toolkit.logger import Logger
import os

logging = Logger(30, os.path.join(dir_path, "main.log"))

def get_holdingsinfo(broker):
    try:
        resp_list = broker.holdings()
        df = pd.DataFrame(resp_list)
        df['source'] = 'holdings'
        return df
    except Exception as e:
        print(f"An error occurred in holdings: {e}")
        logging.error(f"An error occurred in holdings: {e}")
        return None

def get_positionsinfo(broker):
    try:
        resp_list = broker.positions()
        df = pd.DataFrame(resp_list['net'])
        df['source'] = 'positions'
        return df
    except Exception as e:
        print(f"An error occurred in positions: {e}")
        logging.error(f"An error occurred in positions: {e}")
        return None

def get_ordersinfo(broker):
    try:
        resp_list = broker.orders()
        df = pd.DataFrame(resp_list)
        df['source'] = 'orders'
        return df
    except Exception as e:
        print(f"An error occurred in orders: {e}")
        logging.error(f"An error occurred in orders: {e}")
        return None

try:
    broker = get_kite()
    
    holdings_df = get_holdingsinfo(broker)
    positions_df = get_positionsinfo(broker)
    orders_df = get_ordersinfo(broker)

    if holdings_df is not None:
        holdings_df.to_csv(os.path.join(dir_path, 'holdings.csv'), index=False)
        print(f"Holdings data saved to {os.path.join(dir_path, 'holdings.csv')}")
    if positions_df is not None:
        positions_df.to_csv(os.path.join(dir_path, 'positions.csv'), index=False)
        print(f"Positions data saved to {os.path.join(dir_path, 'positions.csv')}")
    if orders_df is not None:
        orders_df.to_csv(os.path.join(dir_path, 'orders.csv'), index=False)
        print(f"Orders data saved to {os.path.join(dir_path, 'orders.csv')}")
    
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings, positions, or orders")
    sys.exit(1)
