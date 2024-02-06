# Imports (place at the beginning)
import pandas as pd
import traceback
import sys
import asyncio
import logging
import telegram

from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path, fileutils, buybuff, max_target
from buypluspxy import Trendlyne
from fundpxy import calculate_decision

# Configure logging
logging.basicConfig(level=logging.INFO)
logging = Logger(30, dir_path + "main.log")

# Constants
NSE = 'NSE'
BUY = 'BUY'

# Set up black file path
black_file = dir_path + "blacklist.txt"

def get_ltp(symbol, broker):
    key = f"{NSE}:{symbol}"
    resp = broker.kite.ltp(key)
    if resp and isinstance(resp, dict):
        return resp[key]['last_price']
    return -1

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

        # Check if available cash is sufficient
        if available_cash > 10000:
            # Place the order on NSE
            order_id = broker.order_place(
                tradingsymbol=dct['tradingsymbol'],
                exchange=NSE,
                transaction_type=BUY,
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

                    # Send the message to Telegram
                    asyncio.run(send_telegram_message(message_text))
                    
                except Exception as e:
                    # Handle the exception (e.g., log it) and continue with your code
                    logging.error(f"Error sending message to Telegram: {e}")

                return dct['tradingsymbol'], remaining_cash

        else:
            logging.warning(
                f"Skipping {dct['tradingsymbol']}: Insufficient remaining cash: {int(remaining_cash)}")
        return dct['tradingsymbol'], remaining_cash

    except Exception as e:
        logging.error(f"Error while placing order: {str(e)}")
        return dct['tradingsymbol'], remaining_cash


if __name__ == "__main__":
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
            holdings = df_fileHPdf['tradingsymbol'].to_list()

            # Get list from Trendlyne
            trendlyne_symbols = []
            lst_dct_tlyne = Trendlyne().entry()
            if lst_dct_tlyne and any(lst_dct_tlyne):
                trendlyne_symbols = [dct['tradingsymbol'] for dct in lst_dct_tlyne]

        except Exception as e:
            print(traceback.format_exc())
            logging.error(f"{str(e)} unable to read Trendlyne calls")
            sys.exit(1)

        try:
            if any(trendlyne_symbols):
                logging.info(f"Reading Trendlyne: {trendlyne_symbols}")
                trendlyne_symbols = [x for x in trendlyne_symbols if x not in holdings]
                logging.info(f"Filtered from holdings and positions: {holdings}")

                # Get lists from orders
                lst_dct_orders = broker.orders

                if lst_dct_orders and any(lst_dct_orders):
                    symbols_orders = [dct['symbol'] for dct in lst_dct_orders]
                else:
                    symbols_orders = []

                # Combine symbols orders
                all_symbols = symbols_orders

                # Filter trendlyne_symbols based on combined symbols
                trendlyne_symbols = [x for x in trendlyne_symbols if x not in all_symbols]

                logging.info(f"Filtered from orders, these are not in orders: {trendlyne_symbols}")

        except Exception as e:
            print(traceback.format_exc())
            logging.error(f"{str(e)} unable to read positions")
            sys.exit(1)

        # Remaining cash initialization
        remaining_cash = 0

        for symbol in trendlyne_symbols:
            # Assuming dct is the dictionary containing trading symbol and other details
            dct = {'tradingsymbol': symbol, 'QTY': '...', 'other_key': 'other_value'}  # Include other relevant key-value pairs
            symbol, remaining_cash = transact(dct, remaining_cash, broker)
            Utilities().slp_til_nxt_sec()

        # Write the failed symbols to file, so we don't repeat them again
        if any(new_list):
            with open(black_file, 'w') as file:
                for symbol in new_list:
                    file.write(symbol + '\n')

        print(f"Remaining Cash💰: {round(remaining_cash, 0)}")

    elif decision == "NO":
        # Perform actions for "NO"
        print("\033[91mNo sufficient funds available \033[0m")
        print("-" * 42)


