from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite
from cnstpxy import dir_path, fileutils, max_target
from byhopxy import get
from pluspxy import Trendlyne
import pandas as pd
import traceback
import sys
import os
import asyncio

logging = Logger(10)
holdings = dir_path + "holdings.csv"
black_file = dir_path + "blacklist.txt"

# Define these values or adjust as per your implementation
some_quantity = 1
# Define or import calc_target and other necessary functions

def initialize():
    try:
        sys.stdout = open('output.txt', 'w')
        broker = get_kite(api="bypass", sec_dir=dir_path)
        if fileutils.is_file_not_2day(holdings):
            logging.debug("getting holdings for the day ...")
            resp = broker.kite.holdings()
            if resp and any(resp):
                df = get(resp)
                logging.debug(f"writing to csv ... {holdings}")
                df.to_csv(holdings, index=False)
            with open(black_file, 'w+'):
                pass
        return broker
    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} unable to get holdings")
        sys.exit(1)

def get_filtered_symbols(lst_tlyne, lst, broker):
    try:
        if any(lst_tlyne):
            logging.info(f"reading trendlyne ...{lst_tlyne}")
            lst_tlyne = [x for x in lst_tlyne if x not in lst]
            logging.info(f"filtered from holdings: {lst}")
            
            lst_dct_positions = broker.positions
            lst_dct_orders = [order for order in broker.orders if order.get('status') == 'OPEN']

            symbols_positions = [dct['symbol'] for dct in lst_dct_positions] if lst_dct_positions else []
            symbols_orders = [dct['symbol'] for dct in lst_dct_orders] if lst_dct_orders else []

            all_symbols = symbols_positions + symbols_orders

            # Assuming lst_tlyne is defined somewhere before this block
            lst_tlyne = lst_tlyne if lst_tlyne else []  # Initialize lst_tlyne if not defined

            # Filter lst_tlyne based on combined symbols
            lst_tlyne = [x for x in lst_tlyne if x not in all_symbols]

            logging.info(f"filtered from positions and orders ...{lst_tlyne}")
        return lst_tlyne
    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} unable to filter symbols")
        sys.exit(1)

def get_ltp(symbol, broker):
    try:
        ltp = -1
        key = f"NSE:{symbol}"  # Adjust based on your exchange requirements
        resp = broker.kite.ltp(key)
        if resp and isinstance(resp, dict):
            ltp = resp[key]['last_price']
        return ltp
    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} unable to get LTP for {symbol}")
        return -1

def transact(symbol, exchange, quantity, available_cash, broker):
    try:
        ltp = get_ltp(symbol, broker)
        if ltp == -1:
            return

        # Remove some_percentage and adjust target_price calculation as needed
        target_price = calc_target(ltp)

        if available_cash > 11000:
            # Place the buy order
            order_id_buy = broker.order_place(
                tradingsymbol=symbol,
                exchange=exchange,
                transaction_type='BUY',
                quantity=quantity,
                order_type='LIMIT',
                product='CNC',
                variety='regular',
                price=target_price
            )

            if order_id_buy:
                logging.info(f"BUY {order_id_buy} placed for {symbol} successfully")
                # Update available cash after placing the order
                response = broker.kite.margins()
                available_cash = response["equity"]["available"]["live_balance"]
        else:
            print(f"Insufficient available cash to place a buy order for {symbol}")

        Utilities().slp_til_nxt_sec()  # Sleep until the next second
    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} error while placing order for {symbol}")

def process_failed_symbols(lst_tlyne, lst_dct_tlyne, lst_failed_symbols, broker):
    try:
        new_list = []
        # Filter the original list based on the subset of 'tradingsymbol' values
        lst_all_orders = [d for d in lst_dct_tlyne if d['tradingsymbol'] in lst_tlyne]
        # Read the list of previously failed symbols from the file
        with open(black_file, 'r') as file:
            lst_failed_symbols = [line.strip() for line in file.readlines()]
        logging.info(f"ignored symbols: {lst_failed_symbols}")
        lst_orders = [d for d in lst_all_orders if d['tradingsymbol'] not in lst_failed_symbols]
        for d in lst_orders:
            failed_symbol = transact(d['tradingsymbol'], 'NSE', some_quantity, available_cash, broker)
            if failed_symbol:
                new_list.append(failed_symbol)
            Utilities().slp_til_nxt_sec()
        if any(new_list):
            with open(black_file, 'w') as file:
                for symbol in new_list:
                    file.write(symbol + '\n')
    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} error while processing failed symbols")


# Initialize
broker = initialize()

# Assuming lst_tlyne is defined somewhere before this block
lst_tlyne = [...]  # Replace with actual data
logging.info(f"filtered from positions and orders ...{lst_tlyne}")

# Filter lst_tlyne based on combined symbols
lst_tlyne = get_filtered_symbols(lst_tlyne, lst, broker)

logging.info(f"filtered from positions and orders ...{lst_tlyne}")

# Get the list of stocks from Trendlyne
lst_tlyne = [...]  # Replace with actual data

# Filter lst_tlyne based on combined symbols
lst_tlyne = [x for x in lst_tlyne if x not in all_symbols]

logging.info(f"filtered from positions and orders ...{lst_tlyne}")

# Iterate through the filtered list and check available cash for each symbol
exchange = 'NSE'  # or 'BSE' or any other valid value
for symbol in lst_tlyne:
    transact(symbol, exchange, some_quantity, available_cash, broker)

if any(lst_tlyne):
    process_failed_symbols(lst_tlyne, lst_dct_tlyne, lst_failed_symbols, broker)
elif available_cash <= 11000:
    print("Insufficient available cash to place a buy order.")



