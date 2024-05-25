import yfinance as yf
import pandas as pd
import traceback
import sys
import os
import asyncio
import logging
import telegram
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from fundpxy import calculate_decision
from trndlnpxy import Trendlyne

logging.basicConfig(level=logging.INFO)
logging = Logger(30, dir_path + "main.log")

def calculate_heikin_ashi_colors(data):
    # Calculate Heikin-Ashi candles
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
    
    return current_color, last_closed_color

def check_ha_candles(symbol):
    # Fetch historical data for the stock with daily interval
    data = yf.Ticker(symbol).history(period="5d", interval="1d")

    # Calculate Heikin-Ashi candles colors
    current_color, last_closed_color = calculate_heikin_ashi_colors(data)

    # Check for market position
    if current_color == 'Bear' and last_closed_color == 'Bull':
        smbpxy = 'Sell'
    elif current_color == 'Bull' and last_closed_color == 'Bear':
        smbpxy = 'Buy'
    else:
        smbpxy = 'Hold'

    return smbpxy

def place_order(symbol, broker):
    try:
        response = broker.kite.margins()
        remaining_cash = response["equity"]["available"]["live_balance"]
        
        ltp_nse = broker.kite.ltp("NSE:" + symbol)[f"NSE:{symbol}"]['last_price']
        
        if ltp_nse > 0 and remaining_cash > limit:
            quantity = int(10000 / ltp_nse)  # Calculate quantity based on available cash and LTP
            
            order_id = broker.order_place(
                tradingsymbol=symbol,
                exchange='NSE',
                transaction_type='BUY',
                quantity=quantity,
                order_type='LIMIT',
                product='CNC',
                variety='regular',
                price=round_to_paise(ltp_nse, 0.2)  # Use the NSE LTP for price calculation
            )
            
            if order_id:
                logging.info(f"BUY {order_id} placed for {symbol} successfully")
                remaining_cash -= quantity * ltp_nse
                print(f"Order placed successfully for {symbol} and cash remained {remaining_cash}")

                message_text = f"📊 Let's Buy {symbol}!\n📈 Current Price (LTP): {ltp_nse}\n🔍 Check it out on TradingView: https://www.tradingview.com/chart/?symbol={symbol}"
                bot_token = '6924826872:AAHTiMaXmjyYbGsCFhdZlRRXkyfZTpsKPug'  # Replace with your actual bot token
                user_id = '-4135910842'  # Replace with your Telegram user ID
                
                async def send_telegram_message(message_text):
                    bot = telegram.Bot(token=bot_token)
                    await bot.send_message(chat_id=user_id, text=message_text)

                asyncio.run(send_telegram_message(message_text))
            else:
                logging.warning(f"Failed to place order for {symbol}")
        else:
            logging.warning(f"Skipping {symbol}: no LTP or no cash")
    except Exception as e:
        logging.error(f"Error while placing order: {str(e)}")

# List of stock symbols
symbols = ["HDFCBANK", "ICICIBANK", "AXISBANK", "SBIN", "KOTAKBANK", "INDUSINDBK", "BANKBARODA", "PNB", "FEDERALBNK", "IDFCFIRSTB"]

# Fetching decision and other details
decision, optdecision, available_cash, limit = calculate_decision()

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

# Fetch holdings, positions, and orders
try:
    lst_dct_tlyne = Trendlyne().entry()
    positions_symbols = [dct.get('tradingsymbol') for dct in lst_dct_tlyne]

except Exception as e:
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to read positions")
    positions_symbols = []

try:
    lst_dct_orders = broker.orders
    orders_symbols = [dct.get('tradingsymbol') for dct in lst_dct_orders]

except Exception as e:
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to read orders")
    orders_symbols = []

# Combine all symbols to skip
skip_symbols = set(positions_symbols + orders_symbols)

# Check Heikin-Ashi candles for each symbol and place orders if decision is "YES"
for symbol in symbols:
    if decision == "YES":
        if symbol not in skip_symbols:
            yf_symbol = symbol + ".NS"  # Add .NS for Yahoo Finance
            smbpxy = check_ha_candles(yf_symbol)
            if smbpxy == 'Buy':
                # Place order without .NS
                print(f"Placing order for {symbol}...")
                place_order(symbol, broker)
                
                # Check remaining cash
                response = broker.kite.margins()
                remaining_cash = response["equity"]["available"]["live_balance"]
                print(f"Remaining Cash💰: {int(round(remaining_cash/1000))}K")
                
                if remaining_cash < 6000:
                    print(f"Cash : {remaining_cash}, stopping further orders.")
                    break
            else:
                logging.info(f"Skipping {symbol}: smbpxy is not 'Buy'")
        else:
            logging.info(f"Skipping {symbol}: already part of positions or orders")
    else:
        logging.info("Decision is not 'YES', skipping order placement.")
