# ordpxy.py

import sys
from toolkit.logger import Logger
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path

logging = Logger(30, dir_path + "main.log")

def list_open_orders_by_symbol(symbol):
    try:
        broker = get_kite(api="bypass", sec_dir=dir_path)
    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get broker")
        sys.exit(1)

    try:
        orders = broker.kite.orders()

        for order in orders:
            if order['status'] == 'OPEN' and order['tradingsymbol'] == symbol:
                print(f"Symbol: {order['tradingsymbol']}")
                print(f"Order Status: {order['status']}")
                print("---")

    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get orders")
        sys.exit(1)
