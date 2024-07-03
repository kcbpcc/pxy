# PXYImports (place at the beginning)
import os
import sys
import pandas as pd
import logging
import asyncio
import telegram
import traceback
import yfinance as yf
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite, remove_token
from trndlnpxy import Trendlyne
from fundpxy import calculate_decision
from cnstpxy import dir_path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = Logger(30, os.path.join(dir_path, "main.log"))

# Telegram bot token and user ID (replace with your actual values)
bot_token = '6867988078:AAGNBJqs4Rf8MR4xPGoL1-PqDOYouPan7b0'
user_id = '-4136531362'

# Function to send Telegram message
async def send_telegram_message(message_text):
    bot = telegram.Bot(token=bot_token)
    await bot.send_message(chat_id=user_id, text=message_text)

# Calculate decisions and set up variables
decision, optdecision, available_cash, limit = calculate_decision()

# Ensure blacklist_file points to the correct path
blacklist_file = os.path.join(dir_path, "blacklist.txt")

# Check if the file exists, create it if not
if not os.path.exists(blacklist_file):
    try:
        with open(blacklist_file, 'w') as file:
            pass  # Creating an empty file
    except IOError as e:
        logger.error(f"Error creating {blacklist_file}: {e}")
        sys.exit(1)

# Save the original sys.stdout
original_stdout = sys.stdout

try:
    with open('output.txt', 'w') as file:
        sys.stdout = file
        try:
            broker = get_kite()
        except Exception as e:
            remove_token(dir_path)
            logger.error(f"{str(e)} unable to get holdings")
            print(traceback.format_exc())
            sys.exit(1)
finally:
    sys.stdout = original_stdout

# Call the calculate_decision function to get the decision
if decision == "YES":
    try:
        df_fileHPdf = pd.read_csv('fileHPdf.csv')
        holdings_list = df_fileHPdf['tradingsymbol'].tolist()
        trendlyne_symbols = [dct['tradingsymbol'] for dct in Trendlyne().entry() if dct]
    except Exception as e:
        logger.error(f"{str(e)} unable to read Trendlyne calls")
        print(traceback.format_exc())
        sys.exit(1)

    trendlyne_symbols = [sym for sym in trendlyne_symbols if sym not in holdings_list]
    logger.info(f"Filtered symbols from holdings: {holdings_list}")

    try:
        orders_list = broker.orders
        orders_symbols = [order['symbol'] for order in orders_list] if orders_list else []
        trendlyne_symbols = [sym for sym in trendlyne_symbols if sym not in orders_symbols]
        logger.info(f"Filtered symbols from orders: {orders_symbols}")
    except Exception as e:
        logger.error(f"{str(e)} unable to read positions")
        print(traceback.format_exc())
        sys.exit(1)

    def calc_target(ltp, perc):
        resistance = round_to_paise(ltp, perc)
        target = round_to_paise(ltp, max_target)
        return max(resistance, target)

    def transact(dct, remaining_cash, broker):
        ltp = -1
        try:
            def get_ltp(exchange):
                nonlocal ltp
                key = f"{exchange}:{dct['tradingsymbol']}"
                resp = broker.kite.ltp(key)
                if resp and isinstance(resp, dict):
                    ltp = resp[key]['last_price']
                return ltp
            
            ltp_nse = get_ltp('NSE')
            logger.info(f"LTP for {dct['tradingsymbol']} on NSE is {ltp_nse}")
            
            if ltp_nse > 0 and remaining_cash > limit:
                order_id = broker.order_place(
                    tradingsymbol=dct['tradingsymbol'],
                    exchange='NSE',
                    transaction_type='BUY',
                    quantity=max(1, round(float(dct['QTY']))),
                    order_type='LIMIT',
                    product='CNC',
                    variety='regular',
                    price=round_to_paise(ltp_nse, 0.2)
                )
                
                if order_id:
                    logger.info(f"BUY {order_id} placed for {dct['tradingsymbol']} successfully")
                    remaining_cash -= int(float(dct['QTY'].replace(',', ''))) * ltp_nse
                    print(f"Order placed successfully for {dct['tradingsymbol']} and cash remained {remaining_cash}")
                    
                    try:
                        message_text = (f"📊 Let's Buy {dct['tradingsymbol']}!\n"
                                        f"📈 Current Price (LTP): {ltp}\n"
                                        f"🔍 Check it out on TradingView: "
                                        f"https://www.tradingview.com/chart/?symbol={dct['tradingsymbol']}")
                        asyncio.run(send_telegram_message(message_text))
                    except Exception as e:
                        logger.error(f"Error sending message to Telegram: {e}")
                    
                    return dct['tradingsymbol'], remaining_cash
            
            else:
                logger.warning(f"Skipping {dct['tradingsymbol']}: no LTP or insufficient cash")
                return dct['tradingsymbol'], remaining_cash
        except Exception as e:
            logger.error(f"Error while placing order: {str(e)}")
            return dct['tradingsymbol'], remaining_cash

    if trendlyne_symbols:
        new_blacklist = []
        with open(blacklist_file, 'r') as file:
            failed_symbols = [line.strip() for line in file.readlines()]
        
        logger.info(f"Ignored symbols: {failed_symbols}")
        valid_orders = [d for d in trendlyne_symbols if d not in failed_symbols]
        response = broker.kite.margins()
        remaining_cash = response["equity"]["available"]["live_balance"]

        for order in valid_orders:
            symbol, remaining_cash = transact(order, remaining_cash, broker)
            Utilities().slp_til_nxt_sec()
            if remaining_cash < 6000:
                break

        if new_blacklist:
            with open(blacklist_file, 'w') as file:
                for symbol in new_blacklist:
                    file.write(symbol + '\n')

        print(f"Remaining Cash💰: {int(round(remaining_cash / 1000))}K")
elif decision == "NO":
    print(f"\033[91mNo sufficient funds available Cash💰: {int(round(available_cash / 1000))}K\033[0m")
    print("-" * 42)

