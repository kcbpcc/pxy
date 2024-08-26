import sys
import numpy as np
import traceback
import pandas as pd
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from toolkit.logger import Logger
import csv
import os
import logging

logging = Logger(30, dir_path + "main.log")

def get_positionsinfo(resp_list, broker):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'positions'
        return df
    except Exception as e:
        print(f"An error occurred in positions: {e}")
        return None

def get_ordersinfo(broker):
    try:
        orders = broker.kite.orders()
        orders_df = pd.DataFrame(orders)
        orders_df['source'] = 'orders'
        return orders_df
    except Exception as e:
        print(f"An error occurred in orders: {e}")
        return None

try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite()

    # Fetch positions information
    positions_resp = broker.kite.positions()['net']
    positions_df = get_positionsinfo(positions_resp, broker)
    if positions_df is not None:
        print("Positions DataFrame:")
        print(positions_df)

    # Fetch orders information
    orders_df = get_ordersinfo(broker)
    if orders_df is not None:
        # Select only the specified columns
        columns_to_print = [
            'order_id', 'exchange_order_id', 'status', 'exchange', 
            'tradingsymbol', 'transaction_type', 'product', 
            'quantity', 'average_price', 'filled_quantity'
        ]
        orders_df = orders_df[columns_to_print]

        print("\nOrders DataFrame (Selected Columns):")
        print(orders_df)

        # Dump the selected columns to CSV
        orders_df.to_csv('orders_data.csv', index=False)
        print("Orders DataFrame has been saved to 'orders_data.csv'")

except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)
finally:
    # Ensure to close the file and restore stdout
    if sys.stdout != sys.__stdout__:
        sys.stdout.close()
        sys.stdout = sys.__stdout__

