import sys
import traceback
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from toolkit.logger import Logger
import logging
import kiteconnect

# Initialize logging
logging = Logger(30, dir_path + "main.log")

try:
    broker = get_kite(api="bypass", sec_dir=dir_path)
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)

def get_infy_ltp():
    try:
        # Retrieve OHLC data for INFY
        resp = broker.kite.ohlc(['NSE:INFY'])

        # Extract LTP from the response
        infy_ltp = resp.get('NSE:INFY', {}).get('ohlc', {}).get('open', 0)

        return infy_ltp
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    infy_ltp = get_infy_ltp()
    if infy_ltp is not None:
        print(f"INFY LTP: {infy_ltp}")
    else:
        print("Failed to retrieve INFY LTP.")

