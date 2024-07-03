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
        lst = df_fileHPdf['tradingsymbol'].to_list()

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
                    # Update remaining cash if the order is successful
                    remaining_cash -= int(float(dct['QTY'].replace(',', ''))) * ltp_nse
                    print(f"Order placed successfully for {dct['tradingsymbol']} and cash remained {remaining_cash}")
                    try:
                        message_text = f"{ltp} \nhttps://www.tradingview.com/chart/?symbol={dct['tradingsymbol']}"
    
                        # Define the bot token and your Telegram username or ID
                        bot_token = '6924826872:AAHTiMaXmjyYbGsCFhdZlRRXkyfZTpsKPug'  # Replace with your actual bot token
                        user_id = '-4135910842'  # Replace with your Telegram user ID
                        # Function to send a message to Telegram
                        async def send_telegram_message(message_text):
                            bot = telegram.Bot(token=bot_token)
                            await bot.send_message(chat_id=user_id, text=message_text)
    
                        # Send the 'row' content as a message to Telegram immediately after printing the row
                        asyncio.run(send_telegram_message(message_text))
                        
                    except Exception as e:
                        # Handle the exception (e.g., log it) and continue with your code
                        print(f"Error sending message to Telegram: {e}")
                    return dct['tradingsymbol'], remaining_cash
    
            else:
                logging.warning(f"Skipping {dct['tradingsymbol']}:no LTP or no cash")
                return dct['tradingsymbol'], remaining_cash
    
        except Exception as e:
            logging.error(f"Error while placing order: {str(e)}")
            return dct['tradingsymbol'], remaining_cash

    
    if any(lst_tlyne):
        new_list = []
    
        # Filter the original list based on the subset of 'tradingsymbol' values
        lst_all_orders = [d for d in lst_dct_tlyne if d['tradingsymbol'] in lst_tlyne]
    
        # Read the list of previously failed symbols from the file
        with open(black_file, 'r') as file:
            lst_failed_symbols = [line.strip() for line in file.readlines()]
        logging.info(f"Ignored symbols: {lst_failed_symbols}")
        lst_orders = [d for d in lst_all_orders if d['tradingsymbol'] not in lst_failed_symbols]
    
        response = broker.kite.margins()
        remaining_cash = response["equity"]["available"]["live_balance"]
    
        for d in lst_orders:
            symbol, remaining_cash = transact(d, remaining_cash, broker)
            Utilities().slp_til_nxt_sec()
    
            # Check if remaining cash falls below 25000 and exit the loop
            if remaining_cash < 2500000:
                break
    
        # Write the failed symbols to file, so we don't repeat them again
        if any(new_list):
            with open(black_file, 'w') as file:
                for symbol in new_list:
                    file.write(symbol + '\n')
    
        # Print remaining cash after the loop completes
        print(f"Remaining Cash💰: {int(round(remaining_cash))}")

elif decision == "NO":
    # Perform actions for "NO"
    print("\033[91mNo sufficient funds available \033[0m")
    print("-" * 42)
