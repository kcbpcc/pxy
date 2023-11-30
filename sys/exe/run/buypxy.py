from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite
from cnstpxy import dir_path, fileutils, buybuff, max_target
from byhopxy import get
from pluspxy import Trendlyne
import pandas as pd
import traceback
import sys
import os
import ynfndpxy
from ynfndpxy import calculate_decision
from mktpxy import mktpxy
from mktchksmbl import getsmktchk
from swchpxy import analyze_stock
from nftpxy import nse_action
import asyncio

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
    if any(lst_tlyne):
        logging.info(f"reading trendlyne ...{lst_tlyne}")
        lst_tlyne = [
            x for x in lst_tlyne if x not in lst]
        logging.info(f"filtered from holdings: {lst}")

        # get list from positions
        lst_dct = broker.positions
        if lst_dct and any(lst_dct):
            lst = [dct['symbol'] for dct in lst_dct]
            lst_tlyne = [
                x for x in lst_tlyne if x not in lst]
            logging.info(f"filtered from positions ...{lst}")
except Exception as e:
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to read positions")
    sys.exit(1)


def calc_target(ltp, perc):
    resistance = round_to_paise(ltp, perc)
    target = round_to_paise(ltp, max_target)
    return max(resistance, target)


def transact(dct):
    try:
        def get_ltp():
            ltp = -1
            key = "NSE:" + dct['tradingsymbol']
            resp = broker.kite.ltp(key)
            if resp and isinstance(resp, dict):
                ltp = resp[key]['last_price']
            return ltp

        ltp = get_ltp()
        logging.info(f"ltp for {dct['tradingsymbol']} is {ltp}")
        if ltp <= 0:
            return dct['tradingsymbol']

        order_id = broker.order_place(
            tradingsymbol=dct['tradingsymbol'],
            exchange='NSE',
            transaction_type='BUY',
            quantity=int(float(dct['calculated'])),
            order_type='LIMIT',
            product='CNC',
            variety='regular',
            price=round_to_paise(ltp, buff)
        )
        if order_id:
            logging.info(
                f"BUY {order_id} placed for {dct['tradingsymbol']} successfully")
            order_id = broker.order_place(
                tradingsymbol=dct['tradingsymbol'],
                exchange='NSE',
                transaction_type='SELL',
                quantity=int(float(dct['calculated'])),
                order_type='LIMIT',
                product='CNC',
                variety='regular',
                price=calc_target(ltp, dct['res_3'])
            )
            if order_id:
                logging.info(
                    f"SELL {order_id} placed for {dct['tradingsymbol']} successfully")
    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} while placing order")
        return dct['tradingsymbol']


if any(lst_tlyne):
    new_list = []
    # Filter the original list based on the subset of 'tradingsymbol' values
    lst_all_orders = [
        d for d in lst_dct_tlyne if d['tradingsymbol'] in lst_tlyne]

    # Read the list of previously failed symbols from the file
    with open(black_file, 'r') as file:
        lst_failed_symbols = [line.strip() for line in file.readlines()]
    logging.info(f"ignored symbols: {lst_failed_symbols}")
    lst_orders = [d for d in lst_all_orders if d['tradingsymbol']
                  not in lst_failed_symbols]

    # place trades for symbol
    for d in lst_orders:
        failed_symbol = transact(d)
        if failed_symbol:
            new_list.append(failed_symbol)
        Utilities().slp_til_nxt_sec()

    # write the failed symbols to file, so we dont repeat them again
    if any(new_list):
        with open(black_file, 'w') as file:
            for symbol in new_list:
                file.write(symbol + '\n')
