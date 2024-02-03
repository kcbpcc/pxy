from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite
from cnstpxy import dir_path, fileutils, buybuff, max_target
from buypluspxy import Trendlyne
import pandas as pd
import traceback
import sys
import os
from fundpxy import calculate_decision
decision = calculate_decision()
from mktpxy import get_market_check
onemincandlesequance, mktpxy = get_market_check()    
import asyncio
import logging
import telegram

logging.basicConfig(level=logging.INFO)
logging = Logger(30, dir_path + "main.log")

black_file = dir_path + "blacklist.txt"

# Save the original sys.stdout
original_stdout = sys.stdout

try:
    # Redirect sys.stdout to 'output.txt'
    with open('output.txt', 'w') as file:
        sys.stdout = file

        try:
            broker = get_kite(api="bypass", sec_dir=dir_path)
        except Exception as e:
            remove_token(dir_path)
            print(traceback.format_exc())
            logging.error(f"{str(e)} unable to get holdings")
            sys.exit(1)

finally:
    # Reset sys.stdout to its original value
    sys.stdout = original_stdout

# Call the calculate_decision function to get the decision
if decision == "YES":
    try:
        # Read the fileHPdf.csv directly
        df_fileHPdf = pd.read_csv('fileHPdf.csv')

        # Extract tradingsymbols from df_fileHPdf
        lst = df_fileHPdf['tradingsymbol'].to_list()

        # get list from Trendlyne
        lst_tlyne = []
        lst_dct_tlyne = Trendlyne().entry()
        if lst_dct_tlyne and any(lst_dct_tlyne):
            lst_tlyne = [dct['tradingsymbol'] for dct in lst_dct_tlyne]

    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} unable to read Trendlyne calls")
        sys.exit(1)

    try:
        if any(lst_tlyne):
            logging.info(f"reading trendlyne ...{lst_tlyne}")
            lst_tlyne = [x for x in lst_tlyne if x not in lst]
            logging.info(f"filtered from holdings and positions: {lst}")

            # get lists from orders
            lst_dct_orders = broker.orders

            if lst_dct_orders and any(lst_dct_orders):
                symbols_orders = [dct['symbol'] for dct in lst_dct_orders]
            else:
                symbols_orders = []

            # Combine symbols orders
            all_symbols = symbols_orders

            # Assuming lst_tlyne is defined somewhere before this block
            lst_tlyne = lst_tlyne if lst_tlyne else []  # Initialize lst_tlyne if not defined

            # Filter lst_tlyne based on combined symbols
            lst_tlyne = [x for x in lst_tlyne if x not in all_symbols]

            logging.info(f"filtered from orders, these are not in orders ...{lst_tlyne}")

    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} unable to read positions")
        sys.exit(1)

    def calc_target(ltp, perc):
        resistance = round_to_paise(ltp, perc)
        target = round_to_paise(ltp, max_target)
        return max(resistance, target)

    # Define the transact function
    def transact(dct, remaining_cash, broker):
        response = broker.kite.margins()
        available_cash = response["equity"]["available"]["live_balance"]

        # Define ltp before the try block
        ltp = -1

        try:
            def get_ltp(exchange):
                nonlocal ltp  # Use nonlocal to reference the outer ltp variable
                key = f"{exchange}:{dct['tradingsymbol']}"
                resp = broker.kite.ltp(key)
                if resp and isinstance(resp, dict):
                    ltp = resp[key]['last_price']
                return ltp

            # Try getting LTP from NSE
            ltp_nse = get_ltp('NSE')
            logging.info(f"LTP for {dct['tradingsymbol']} on NSE is {ltp_nse}")

            # If LTP from NSE is not available or <= 0, try getting LTP from BSE
            if ltp_nse <= 0:
                ltp_bse = get_ltp('BSE')
                logging.info(f"LTP for {dct['tradingsymbol']} on BSE is {ltp_bse}")

                # If LTP from BSE is available, use it
                if ltp_bse > 0:
                    ltp = ltp_bse
                else:
                    # Neither NSE nor BSE LTP is available, return with remaining_cash
                    return dct['tradingsymbol'], remaining_cash

            # ... (rest of the existing transact function code)

        except Exception as e:
            print(f"Error in transact function: {e}")
            # Handle the exception if needed

        return dct['tradingsymbol'], remaining_cash

    if any(lst_tlyne):
        new_list = []

        # Filter the original list based on the subset of 'tradingsymbol' values
        lst_all_orders = [d for d in lst_dct_tlyne if d['tradingsymbol'] in lst_tlyne]

        # Read the list of previously failed symbols from the file
        with open(black_file, 'r') as file:
            lst_failed_symbols = [line.strip() for line in file.readlines()]
        logging.info(f"ignored symbols: {lst_failed_symbols}")
        lst_orders = [d for d in lst_all_orders if d['tradingsymbol'] not in lst_failed_symbols]

        response = broker.kite.margins()
        remaining_cash = response["equity"]["available"]["live_balance"]

        for d in lst_orders:
            symbol, remaining_cash = transact(d, remaining_cash, broker)
            Utilities().slp_til_nxt_sec()

        # write the failed symbols to file, so we don't repeat them again
        if any(new_list):
            with open(black_file, 'w') as file:
                for symbol in new_list:
                    file.write(symbol + '\n')

        print(f"Remaining Cash💰: {round(remaining_cash, 0)}")

elif decision == "NO":
    # Perform actions for "NO"
    print("\033[91mNo sufficient funds available \033[0m")
    print("-" * 42)

