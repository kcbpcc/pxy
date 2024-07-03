# PXYImports (place at the beginning)
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from trndlnpxy import Trendlyne
import pandas as pd
import traceback
import sys
import os
from fundpxy import calculate_decision
import asyncio
import logging
import telegram

# Configure logging
logging.basicConfig(level=logging.INFO)
logging = Logger(30, dir_path + "main.log")

# Save the original sys.stdout
try:
    original_stdout = sys.stdout
    with open('output.txt', 'w') as file:
        sys.stdout = file
        try:
            broker = get_kite()
        except Exception as e:
            remove_token(dir_path)
            print(traceback.format_exc())
            logging.error(f"{str(e)} unable to get holdings")
            sys.exit(1)
finally:
    sys.stdout = original_stdout

# Call the calculate_decision function to get the decision
decision = calculate_decision()

if decision == "YES":
    try:
        # Read the fileHPdf.csv directly
        df_fileHPdf = pd.read_csv('fileHPdf.csv')

        # Extract tradingsymbols from df_fileHPdf
        lst = df_fileHPdf['tradingsymbol'].tolist()

        # Initialize lst_tlyne
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

            # Get lists from orders
            lst_dct_orders = broker.orders

            if lst_dct_orders and any(lst_dct_orders):
                symbols_orders = [dct['symbol'] for dct in lst_dct_orders]
            else:
                symbols_orders = []

            # Combine symbols orders
            all_symbols = symbols_orders

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

    def transact(dct, broker):
        response = broker.kite.margins()
        available_cash = response["equity"]["available"]["live_balance"]

        try:
            def get_ltp(exchange):
                key = f"{exchange}:{dct['tradingsymbol']}"
                resp = broker.kite.ltp(key)
                if resp and isinstance(resp, dict):
                    return resp[key]['last_price']
                return -1

            # Try getting LTP from NSE only
            ltp_nse = get_ltp('NSE')
            logging.info(f"LTP for {dct['tradingsymbol']} on NSE is {ltp_nse}")

            # If LTP from NSE is available and greater than 0, proceed with the order
            if ltp_nse > 0 and available_cash > 2500000:
                # Place the order on NSE
                order_id = broker.order_place(
                    tradingsymbol=dct['tradingsymbol'],
                    exchange='NSE',
                    transaction_type='BUY',
                    quantity=int(float(dct['QTY'].replace(',', ''))),
                    order_type='LIMIT',
                    product='CNC',
                    variety='regular',
                    price=round_to_paise(ltp_nse, 0.2)  # Use the NSE LTP for price calculation
                )
                if order_id:
                    logging.info(f"BUY {order_id} placed for {dct['tradingsymbol']} successfully")
                    return f"Order placed successfully for {dct['tradingsymbol']}"
                else:
                    logging.warning(f"Failed to place order for {dct['tradingsymbol']}")
                    return f"Failed to place order for {dct['tradingsymbol']}"

            else:
                logging.warning(f"Skipping {dct['tradingsymbol']}: no LTP or insufficient cash")
                return f"Skipping {dct['tradingsymbol']}: no LTP or insufficient cash"

        except Exception as e:
            logging.error(f"Error while placing order: {str(e)}")
            return f"Error while placing order: {str(e)}"

    if any(lst_tlyne):
        for dct in lst_dct_tlyne:
            if dct['tradingsymbol'] in lst_tlyne:
                result = transact(dct, broker)
                print(result)
                Utilities().slp_til_nxt_sec()
                # Check if remaining cash falls below 25000 and exit the loop
                if broker.kite.margins()["equity"]["available"]["live_balance"] < 2500000:
                    break

elif decision == "NO":
    print("\033[91mNo sufficient funds available \033[0m")
    print("-" * 42)
