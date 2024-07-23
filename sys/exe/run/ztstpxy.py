import pandas as pd
import traceback
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from toolkit.logger import Logger

logging = Logger(30, dir_path + "main.log")

def get_holdingsinfo(resp_list):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'holdings'
        return df
    except Exception as e:
        print(f"An error occurred in holdings: {e}")
        return None

def get_positionsinfo(resp_list):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'positions'
        return df
    except Exception as e:
        print(f"An error occurred in positions: {e}")
        return None

def get_ordersinfo(resp_list):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'orders'
        return df
    except Exception as e:
        print(f"An error occurred in orders: {e}")
        return None

def process_data():
    try:
        broker = get_kite()
        holdings_response = broker.kite.holdings()
        positions_response = broker.kite.positions()['net']
        orders_response = broker.kite.orders()
        
        holdings_df = get_holdingsinfo(holdings_response)
        positions_df = get_positionsinfo(positions_response)
        orders_df = get_ordersinfo(orders_response)
        
        # Save dataframes to CSV files with web<*>.csv naming
        holdings_df.to_csv('webholdings.csv', index=False) if holdings_df is not None else pd.DataFrame().to_csv('webholdings.csv', index=False)
        positions_df.to_csv('webpositions.csv', index=False) if positions_df is not None else pd.DataFrame().to_csv('webpositions.csv', index=False)
        orders_df.to_csv('weborders.csv', index=False) if orders_df is not None else pd.DataFrame().to_csv('weborders.csv', index=False)

        return holdings_df, positions_df, orders_df
        
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return None, None, None

