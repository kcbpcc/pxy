import sys
import traceback
import pandas as pd
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from toolkit.logger import Logger
import os

logging = Logger(30, os.path.join(dir_path, "main.log"))

def get_holdingsinfo(resp_list, broker):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'holdings'
        return df
    except Exception as e:
        logging.error(f"An error occurred in holdings: {e}")
        return None

def get_positionsinfo(resp_list, broker):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'positions'
        return df
    except Exception as e:
        logging.error(f"An error occurred in positions: {e}")
        return None

def get_ordersinfo(resp_list, broker):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'orders'
        return df
    except Exception as e:
        logging.error(f"An error occurred in orders: {e}")
        return None

try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite()
    
    holdings_response = broker.holdings()  # Assuming this method exists
    positions_response = broker.positions()  # Assuming this method exists
    orders_response = broker.orders()  # Assuming this method exists
    
    holdings_df = get_holdingsinfo(holdings_response, broker)
    positions_df = get_positionsinfo(positions_response, broker)
    orders_df = get_ordersinfo(orders_response, broker)
    
    if holdings_df is not None:
        holdings_csv_path = os.path.join(dir_path, 'holdings.csv')
        holdings_df.to_csv(holdings_csv_path, index=False)
        print(f"Holdings data saved to {holdings_csv_path}")
    
    if positions_df is not None:
        positions_csv_path = os.path.join(dir_path, 'positions.csv')
        positions_df.to_csv(positions_csv_path, index=False)
        print(f"Positions data saved to {positions_csv_path}")
    
    if orders_df is not None:
        orders_csv_path = os.path.join(dir_path, 'orders.csv')
        orders_df.to_csv(orders_csv_path, index=False)
        print(f"Orders data saved to {orders_csv_path}")

except Exception as e:
    remove_token(dir_path)
    logging.error(f"{str(e)} unable to get holdings, positions, or orders")
    print(traceback.format_exc())
    sys.exit(1)

finally:
    if sys.stdout != sys.__stdout__:
        sys.stdout.close()
        sys.stdout = sys.__stdout__

