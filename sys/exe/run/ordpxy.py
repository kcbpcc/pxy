# ordpxy.py

import sys
from toolkit.logger import Logger
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path

logging = Logger(30, dir_path + "main.log")

def get_open_order_status(symbol):
    try:
        #sys.stdout = open('output.txt', 'w')
        broker = get_kite(api="bypass", sec_dir=dir_path)
    except Exception as e:
        remove_token(dir_path)
        #print(traceback.format_exc())
        logging.error(f"{str(e)} unable to get holdings")
        sys.exit(1)

    try:
        orders = broker.kite.orders()

        for order in orders:
            if order['status'] == 'OPEN' and order['tradingsymbol'] == symbol:
                return "YES"  # There is at least one open order for the symbol

    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get orders")
        sys.exit(1)

    return "NO"  # No open orders found for the symbol
