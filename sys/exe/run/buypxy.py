# Imports (place at the beginning)
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path, fileutils, buybuff, max_target
from buypluspxy import Trendlyne
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

# Set up black file path
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
decision = calculate_decision()

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

    def transact(dct, remaining_cash, broker):
        response = broker.kite.margins()
        available_cash = response["equity"]["available"]["live_balance"]
    
        try:
            # Get LTP from NSE
            ltp = get_ltp(dct['tradingsymbol'], broker)
            logging.info(f"LTP for {dct['tradingsymbol']} on NSE is {ltp}")
    
            # Check if LTP is valid (> 0)
            if ltp <= 0:
                logging.warning(f"Skipping {dct['tradingsymbol']}: Invalid LTP")
                return dct['tradingsymbol'], remaining_cash
    
            # Check if available cash is greater than 5116
            if available_cash > 10000:
                # Place the order on NSE
                order_id = broker.order_place(
                    tradingsymbol=dct['tradingsymbol'],
                    exchange='NSE',
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
                    # Update remaining cash
                    remaining_cash -= ltp * int(float(dct['QTY'].replace(',', '')))
    
                    try:
                        message_text = f"{ltp} \nhttps://www.tradingview.com/chart/?symbol={dct['tradingsymbol']}"
    
                        # Define the bot token and your Telegram username or ID
                        bot_token = '6924826872:AAHTiMaXmjyYbGsCFhdZlRRXkyfZTpsKPug'  # Replace with your actual bot token
                        user_id = '-4136531362'  # Replace with your Telegram user ID
    
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
                logging.warning(
                    f"Skipping {dct['tradingsymbol']}: Remaining Cash: {int(remaining_cash)}")
            return dct['tradingsymbol'], remaining_cash
    
        except Exception as e:
            logging.error(f"Error while placing order: {str(e)}")
            return dct['tradingsymbol'], remaining_cash


elif decision == "NO":
    # Perform actions for "NO"
    print("\033[91mNo sufficient funds available \033[0m")
    print("-" * 42)


