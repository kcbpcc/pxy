#print("PXY® Trying to check if anything to buy")
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
decision, optdecision, available_cash , limit = calculate_decision()
import asyncio
import logging
import telegram
# Configure logging
logging.basicConfig(level=logging.INFO)
logging = Logger(30, dir_path + "main.log")
# Save the original sys.stdout
original_stdout = sys.stdout

try:
    # Redirect sys.stdout to 'output.txt'
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
if decision == "YES":
    try:
        df_fileHPdf = pd.read_csv('fileHPdf.csv')
        lst = df_fileHPdf['tradingsymbol'].to_list()
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
            lst_dct_orders = broker.orders
            if lst_dct_orders and any(lst_dct_orders):
                symbols_orders = [dct['symbol'] for dct in lst_dct_orders]
            else:
                symbols_orders = []
            all_symbols = symbols_orders
            lst_tlyne = lst_tlyne if lst_tlyne else []  # Initialize lst_tlyne if not defined
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
        ltp = -1
        try:
            def get_ltp(exchange):
                nonlocal ltp  # Use nonlocal to reference the outer ltp variablelimit
                key = f"{exchange}:{dct['tradingsymbol']}"
                resp = broker.kite.ltp(key)
                if resp and isinstance(resp, dict):
                    ltp = resp[key]['last_price']
                return ltp
            ltp_nse = get_ltp('NSE')
            logging.info(f"LTP for {dct['tradingsymbol']} on NSE is {ltp_nse}")
            if ltp_nse > 0 and available_cash > limit :
                order_id = broker.order_place(
                    tradingsymbol=dct['tradingsymbol'],
                    exchange='NSE',
                    transaction_type='BUY',
                    quantity = max(1, round(float(dct['QTY']))) ,                    
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
                        message_text = f"📊 Let's Buy {dct['tradingsymbol']}!\n📈 Current Price (LTP): {ltp}\n🔍 Check it out on TradingView: https://www.tradingview.com/chart/?symbol={dct['tradingsymbol']}"
                        bot_token = '6924826872:AAHTiMaXmjyYbGsCFhdZlRRXkyfZTpsKPug'  # Replace with your actual bot token
                        user_id = '-4135910842'  # Replace with your Telegram user ID
                        async def send_telegram_message(message_text):
                            bot = telegram.Bot(token=bot_token)
                            await bot.send_message(chat_id=user_id, text=message_text)
                        asyncio.run(send_telegram_message(message_text))
                    except Exception as e:
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
        lst_all_orders = [d for d in lst_dct_tlyne if d['tradingsymbol'] in lst_tlyne]
        response = broker.kite.margins()
        remaining_cash = response["equity"]["available"]["live_balance"]
        
        for d in lst_all_orders:
            symbol, remaining_cash = transact(d, remaining_cash, broker)
            Utilities().slp_til_nxt_sec()
            if remaining_cash < 9000:
                break
                
        print(f"Remaining Cash💰: {int(round(remaining_cash/1000))}K")
    
    elif decision == "NO":
        # Perform actions for "NO"
        print(f"\033[91mNo sufficient funds available Cash💰: {int(round(available_cash/1000))}K\033[0m")
        print("-" * 42)
