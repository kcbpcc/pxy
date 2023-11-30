from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite
from cnstpxy import dir_path
from byhopxy import get
from pluspxy import Trendlyne
import pandas as pd
import traceback
import sys
import os

logging = Logger(30)
file_path = "fileHPdf.csv"
black_file = dir_path + "blacklist.txt"

try:
    broker = get_kite(api="bypass", sec_dir=dir_path)
except Exception as e:
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)

try:
    lst = []

    # Read from fileHPdf
    file_size_in_bytes = os.path.getsize(file_path)
    logging.debug(f"fileHPdf file size: {file_size_in_bytes} bytes")
    if file_size_in_bytes > 50:
        logging.debug(f"reading from csv ...{file_path}")
        df_holdings = pd.read_csv(file_path)
        if not df_holdings.empty:
            # Check both trading symbol columns
            lst_tradingsymbol1 = df_holdings['tradingsymbol1'].to_list()
            lst_tradingsymbol2 = df_holdings['tradingsymbol2'].to_list()

            # Combine both lists to get unique symbols
            lst = list(set(lst_tradingsymbol1 + lst_tradingsymbol2))

    # Get list from Trendlyne
    lst_tlyne = []
    lst_dct_tlyne = Trendlyne().entry()
    if lst_dct_tlyne and any(lst_dct_tlyne):
        print(pd.DataFrame(
            lst_dct_tlyne).set_index('tradingsymbol').rename_axis('Trendlyne'), "\n")
        lst_tlyne = [dct['tradingsymbol'] for dct in lst_dct_tlyne]

    # Fetch orders from Zerodha Kite
    orders = broker.kite.orders()

    # Extract trading symbols from Zerodha orders
    lst_kite = [order['tradingsymbol'] for order in orders]

    # Combine lists from fileHPdf, Trendlyne, and Zerodha Kite
    lst = list(set(lst + lst_tlyne + lst_kite))

except Exception as e:
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to read fileHPdf, Trendlyne calls, or fetch orders from Zerodha Kite")
    sys.exit(1)


try:
    # Your existing code to get data from Trendlyne
    if any(lst_tlyne):
        logging.info(f"reading trendlyne ...{lst_tlyne}")
        lst_tlyne = [x for x in lst_tlyne if x not in lst]
        logging.info(f"filtered from holdings: {lst}")

        # get list from positions
        lst_dct_positions = broker.positions
        if lst_dct_positions and any(lst_dct_positions):
            lst_positions = [dct['symbol'] for dct in lst_dct_positions]
            lst_tlyne = [x for x in lst_tlyne if x not in lst_positions]
            logging.info(f"filtered from positions ...{lst_positions}")

    # Fetch orders from Zerodha Kite
    lst_dct_orders = broker.kite.orders()
    if lst_dct_orders and any(lst_dct_orders):
        lst_orders = [order['tradingsymbol'] for order in lst_dct_orders]

        # Combine lists from Trendlyne, positions, and Zerodha Kite orders
        lst_tlyne = list(set(lst_tlyne + lst_positions + lst_orders))

except Exception as e:
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to read positions or fetch orders from Zerodha Kite")
    sys.exit(1)


def calc_target(ltp, perc):
    # Assuming that max_target is not being used
    resistance = round_to_paise(ltp, perc)
    return resistance

def transact(stock_data):
    try:
        # Get margins information
        response = broker.kite.margins()
        available_cash = response["equity"]["available"]["live_balance"]

        # Check if available_cash is greater than 10000
        if available_cash > 10000:
            def get_ltp():
                ltp_nse, ltp_bse = -1, -1
                key_nse = "NSE:" + stock_data['tradingsymbol']
                key_bse = "BSE:" + stock_data['tradingsymbol']

                resp_nse = broker.kite.ltp(key_nse)
                resp_bse = broker.kite.ltp(key_bse)

                if resp_nse and isinstance(resp_nse, dict):
                    ltp_nse = resp_nse[key_nse]['last_price']

                if resp_bse and isinstance(resp_bse, dict):
                    ltp_bse = resp_bse[key_bse]['last_price']

                return ltp_nse, ltp_bse

            ltp_nse, ltp_bse = get_ltp()
            logging.info(f"LTP for {stock_data['tradingsymbol']} (NSE): {ltp_nse}")
            logging.info(f"LTP for {stock_data['tradingsymbol']} (BSE): {ltp_bse}")

            if 0 < ltp_nse < ltp_bse:
                # Place the order on NSE
                exchange = 'NSE'
                ltp = ltp_nse
            elif 0 < ltp_bse < ltp_nse:
                # Place the order on BSE
                exchange = 'BSE'
                ltp = ltp_bse
            else:
                # No valid LTP, return the symbol
                return stock_data['tradingsymbol']

            # Rest of the code to place the order using 'exchange' and 'ltp'
            order_id = broker.order_place(
                tradingsymbol=stock_data['tradingsymbol'],
                exchange=exchange,
                transaction_type='BUY',
                quantity=int(float(stock_data['QTY'])),
                order_type='LIMIT',
                product='CNC',
                variety='regular',
                price=round_to_paise(ltp, +0.2)
            )

            if order_id:
                logging.info(
                    f"BUY {order_id} placed for {stock_data['tradingsymbol']} successfully on {exchange} exchange")

    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} while placing order")
        return stock_data['tradingsymbol']

if any(lst_tlyne):
    new_list = []
    # Filter the original list based on the subset of 'tradingsymbol' values
    lst_all_orders = [d for d in lst_dct_tlyne if d['tradingsymbol'] in lst_tlyne]

    # Read the list of previously failed symbols from the file
    with open(black_file, 'r') as file:
        lst_failed_symbols = [line.strip() for line in file.readlines()]
    logging.info(f"ignored symbols: {lst_failed_symbols}")
    lst_orders = [d for d in lst_all_orders if d['tradingsymbol'] not in lst_failed_symbols]

    # place trades for symbol
    for stock_data in lst_orders:
        failed_symbol = transact(stock_data)
        if failed_symbol:
            new_list.append(failed_symbol)
        Utilities().slp_til_nxt_sec()

    # write the failed symbols to file, so we don't repeat them again
    if any(new_list):
        with open(black_file, 'w') as file:
            for symbol in new_list:
                file.write(symbol + '\n')

