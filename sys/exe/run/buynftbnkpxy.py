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

decision, optdecision, available_cash, limit = calculate_decision()

logging.basicConfig(level=logging.WARNING)
logging = Logger(30, os.path.join(dir_path, "main.log"))

# Constants
BOT_TOKEN = '6924826872:AAHTiMaXmjyYbGsCFhdZlRRXkyfZTpsKPug'
USER_ID = '-4135910842'

print("🌿🌿🌿 Lets Buy NIFTY50 & BANK Stocks 🌿🌿")
print(f"     Cash:💰{available_cash:.2f}💵 | 🚦{decision}🚦 to Buy")

# Function to calculate Heikin-Ashi colors
def calculate_heikin_ashi_colors(data):
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
    last_last_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'
    
    return current_color, last_closed_color, last_last_closed_color

# Function to calculate MACD
def calculate_macd(data):
    short_ema = data['Close'].ewm(span=12, adjust=False).mean()  # 12-day EMA
    long_ema = data['Close'].ewm(span=26, adjust=False).mean()   # 26-day EMA
    macd = short_ema - long_ema
    signal = macd.ewm(span=9, adjust=False).mean()               # 9-day EMA of MACD
    return macd, signal

# Function to check Heikin-Ashi candles and decide action
def check_ha_candles(symbol):
    data = yf.Ticker(symbol).history(period="6mo", interval="1d")  # Use a valid period
    current_data = data.tail(5)  # Use the last 5 days of data for Heikin-Ashi calculations
    
    current_color, last_closed_color, last_last_closed_color = calculate_heikin_ashi_colors(current_data)

    # Calculate the 50-day SMA
    data['50d_SMA'] = data['Close'].rolling(window=50).mean()
    current_price = data['Close'].iloc[-1]
    sma_50 = data['50d_SMA'].iloc[-1]
    
    # Check if the current price is above the 50-day SMA
    above_50d_sma = current_price > sma_50
    
    # Calculate MACD and check if the MACD is greater than 0
    macd, signal = calculate_macd(data)
    macd_above_0 = macd.iloc[-1] > 0

    if last_closed_color == 'Bear' and last_last_closed_color == 'Bear' and current_color == 'Bull' and above_50d_sma and macd_above_0:
        smbpxy = 'Buy'
    else:
        smbpxy = 'Hold'

    return smbpxy

# Function to send a Telegram message
async def send_telegram_message(bot_token, user_id, message_text):
    bot = telegram.Bot(token=bot_token)
    await bot.send_message(chat_id=user_id, text=message_text)

# Function to place an order
def place_order(symbol, broker, limit, quantity):
    try:
        remaining_cash = available_cash

        ltp_nse = broker.kite.ltp("NSE:" + symbol)[f"NSE:{symbol}"]['last_price']
        
        if ltp_nse > 0 and remaining_cash > limit:
            quantity = max(quantity, 1)
            
            order_id = broker.order_place(
                tradingsymbol=symbol,
                exchange='NSE',
                transaction_type='BUY',
                quantity=quantity,
                order_type='LIMIT',
                product='CNC',
                variety='regular',
                price=round_to_paise(ltp_nse, 0.2)
            )
            
            if order_id:
                logging.info(f"BUY {order_id} placed for {symbol} successfully")
                remaining_cash -= quantity * ltp_nse
                print(f"Order placed successfully for {symbol}")

                message_text = f"📊 Let's Buy {symbol}!\n📈 Current Price (LTP): {ltp_nse}\n🔍 Check it out on TradingView: https://www.tradingview.com/chart/?symbol={symbol}"
                
                asyncio.run(send_telegram_message(BOT_TOKEN, USER_ID, message_text))
            else:
                logging.warning(f"Failed to place order for {symbol}")
        else:
            logging.warning(f"Skipping {symbol}: no LTP or no cash")
    except Exception as e:
        logging.error(f"Error while placing order: {str(e)}")

# Define the list of symbols to include
symbols = [
    "KARURVYSYA", "KOTAKBANK", "KTKBANK", "MAHABANK", "PNB", "PSB", "RBLBANK", "SBIN", "SOUTHBANK", "SURYODAY",
    "TMB", "UCOBANK", "UJJIVANSFB", "UNIONBANK", "UTKARSHBNK", "YESBANK", "AUBANK", "AXISBANK", "BANDHANBNK", 
    "BANKBARODA", "BANKINDIA", "CANBK", "CAPITALSFB", "CENTRALBK", "CSBBANK", "CUB", "DCBBANK", "DHANBANK", 
    "EQUITASBNK", "ESAFSFB", "FEDERALBNK", "FINOPB", "HDFCBANK", "ICICIBANK", "IDBI", "IDFCFIRSTB", "INDIANB", 
    "INDUSINDBK", "IOB", "J&KBANK", "JSFB", "WIPRO", "ULTRACEMCO", "TITAN", "TECHM", "TCS", "TATASTEEL", 
    "TATAMOTORS", "TATACONSUM", "SUNPHARMA", "SHRIRAMFIN", "SBILIFE", "RELIANCE", "POWERGRID", "ONGC", "NTPC", 
    "NESTLEIND", "MARUTI", "M&M", "LTIM", "LT", "JSWSTEEL", "ITC", "INFY", "HINDUNILVR", "HINDALCO", "HEROMOTOCO", 
    "HDFCLIFE", "HCLTECH", "GRASIM", "EICHERMOT", "DRREDDY", "DIVISLAB", "COALINDIA", "CIPLA", "BRITANNIA", "BPCL", 
    "BHARTIARTL", "BAJFINANCE", "BAJAJFINSV", "BAJAJ-AUTO", "ASIANPAINT", "APOLLOHOSP", "ADANIPORTS", "ADANIENT"
]

# Fetch decision and other details
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

# Fetch positions and orders
try:
    lst_dct_positions = broker.kite.positions()
    positions_symbols = [pos["tradingsymbol"] for pos in lst_dct_positions["day"] + lst_dct_positions["net"]]

except Exception as e:
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to read positions")
    positions_symbols = []

# Fetch orders
try:
    lst_dct_orders = broker.orders  # Access the list directly
    orders_symbols = [order.get("tradingsymbol", "Unknown Symbol") for order in lst_dct_orders]

except Exception as e:
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to read orders")
    orders_symbols = []

# Fetch holdings
try:
    holdings = broker.kite.holdings()
    holdings_symbols = [holding["tradingsymbol"] for holding in holdings]

except Exception as e:
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to read holdings")
    holdings_symbols = []

# Combine symbols to skip
skip_symbols = set(positions_symbols + orders_symbols + holdings_symbols)

# Check Heikin-Ashi candles for each symbol and place orders if decision is "YES"
for symbol in symbols:
    if decision == "YES":
        yf_symbol = symbol + ".NS"
        smbpxy = check_ha_candles(yf_symbol)
        
        if symbol not in skip_symbols:
            ltp_nse = broker.kite.ltp(f"NSE:{symbol}")[f"NSE:{symbol}"]['last_price']
            if smbpxy == 'Buy' and ltp_nse < 10000:
                print(f"Placing order for {symbol}...")
                place_order(symbol, broker, limit, quantity=int(10000 / ltp_nse))
                remaining_cash = available_cash
                print(f"Remaining Cash💰: {int(round(remaining_cash / 1000))}K")
                
                if remaining_cash < limit:
                    print(f"Cash: {remaining_cash}, stopping further orders.")
                    break
            else:
                logging.info(f"Skipping {symbol}: smbpxy is not 'Buy'")
        else:
            logging.info(f"Skipping {symbol}: already part of positions, orders, or holdings")
    else:
        logging.info("Decision is not 'YES', skipping order placement.")

