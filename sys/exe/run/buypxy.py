from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite
from cnstpxy import dir_path, fileutils, buybuff, max_target
from byhopxy import get
from buypluspxy import Trendlyne
import pandas as pd
import traceback
import sys
import os
from fundpxy import calculate_decision
from mktpxy import get_market_check
import asyncio

mktchk = get_market_check('^NSEI')
logging = Logger(10)

holdings_file = "fileHPdf.csv"
black_file = dir_path + "blacklist.txt"

try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)
    
    # Read the fileHPdf.csv directly
    df_holdings = pd.read_csv(holdings_file)

    logging.debug(f"Read holdings file: {holdings_file}")

except Exception as e:
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to read holdings file: {holdings_file}")
    sys.exit(1)

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
            print(pd.DataFrame(
                lst_dct_tlyne).set_index('tradingsymbol').rename_axis('Trendlyne'), "\n")
            lst_tlyne = [dct['tradingsymbol'] for dct in lst_dct_tlyne]

    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} unable to read Trendlyne calls")
        sys.exit(1)

    try:
        if any(lst_tlyne):
            logging.info(f"reading trendlyne ...{lst_tlyne}")
            lst_tlyne = [
                x for x in lst_tlyne if x not in lst]

            logging.info(f"filtered from holdings: {lst}")

            # get lists from positions and orders
            lst_dct_positions = broker.positions
            lst_dct_orders = broker.orders

            if lst_dct_positions and any(lst_dct_positions):
                symbols_positions = [dct['symbol'] for dct in lst_dct_positions]
            else:
                symbols_positions = []

            if lst_dct_orders and any(lst_dct_orders):
                symbols_orders = [dct['symbol'] for dct in lst_dct_orders]
            else:
                symbols_orders = []

            # Combine symbols from positions and orders
            all_symbols = symbols_positions + symbols_orders

            # Assuming lst_tlyne is defined somewhere before this block
            lst_tlyne = lst_tlyne if lst_tlyne else []  # Initialize lst_tlyne if not defined

            # Filter lst_tlyne based on combined symbols
            lst_tlyne = [x for x in lst_tlyne if x not in all_symbols]

            logging.info(f"filtered from positions and orders ...{lst_tlyne}")

    except Exception as e:
        print(traceback.format_exc())
        logging.error(f"{str(e)} unable to read positions")
        sys.exit(1)


    def calc_target(ltp, perc):
        resistance = round_to_paise(ltp, perc)
        target = round_to_paise(ltp, max_target)
        return max(resistance, target)

    def transact(dct, remaining_cash):
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
    
            # Check if available cash is greater than 5116
            if available_cash > 5116:
                # Place the order on the exchange where LTP is available
                order_id = broker.order_place(
                    tradingsymbol=dct['tradingsymbol'],
                    exchange='NSE' if ltp_nse > 0 else 'BSE',
                    transaction_type='BUY',
                    quantity=int(float(dct['QTY'].replace(',', ''))), 
                    order_type='LIMIT',
                    product='CNC',
                    variety='regular',
                    price=round_to_paise(ltp, 0.2)
                )
                if order_id:
                    logging.info(
                        f"BUY {order_id} placed for {dct['tradingsymbol']} successfully")
                    # No need to calculate remaining available cash in this case
                    return dct['tradingsymbol'], remaining_cash
            else:
                logging.warning(
                    f"Skipping {dct['tradingsymbol']}: Remaining Cash: {int(remaining_cash)}"
                )
            return dct['tradingsymbol'], remaining_cash
    
        except Exception as e:
            logging.error(f"Error while placing order: {str(e)}")
            return dct['tradingsymbol'], remaining_cash
        
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
    
        response = broker.kite.margins()
        remaining_cash = response["equity"]["available"]["live_balance"]
        
        for d in lst_orders:
            symbol, remaining_cash = transact(d, remaining_cash)
            Utilities().slp_til_nxt_sec()
    
        # write the failed symbols to file, so we dont repeat them again
        if any(new_list):
            with open(black_file, 'w') as file:
                for symbol in new_list:
                    file.write(symbol + '\n')
      
        print(f"Available Cash: {remaining_cash}")
elif decision == "NO":
    # Perform actions for "NO"
    print("\033[91mNo Funds Avalable \033[0m") 
