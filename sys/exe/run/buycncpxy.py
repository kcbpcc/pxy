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

# Hardcoded constants
BOT_TOKEN = '6924826872:AAHTiMaXmjyYbGsCFhdZlRRXkyfZTpsKPug'
USER_ID = '-4135910842'

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = Logger(30, os.path.join(dir_path, "main.log"))

# Fetch trading decision and available cash
decision, optdecision, available_cash,live_balance, limit = calculate_decision()

print("🌿🌿🌿 Lets Buy NIFTY50 & BANK Stocks 🌿🌿")
print(f"     Cash:💰{available_cash:.2f}💵 | 🚦{decision}🚦 to Buy")

def calculate_heikin_ashi_colors(data):
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
    last_last_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'
    
    return current_color, last_closed_color, last_last_closed_color

def calculate_macd(data):
    short_ema = data['Close'].ewm(span=12, adjust=False).mean()
    long_ema = data['Close'].ewm(span=26, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def check_ha_candles(symbol):
    data = yf.Ticker(symbol).history(period="6mo", interval="1d")
    current_data = data.tail(5)
    
    current_color, last_closed_color, last_last_closed_color = calculate_heikin_ashi_colors(current_data)

    data['50d_SMA'] = data['Close'].rolling(window=50).mean()
    current_price = data['Close'].iloc[-1]
    sma_50 = data['50d_SMA'].iloc[-1]
    above_50d_sma = current_price > sma_50
    
    macd, signal = calculate_macd(data)
    macd_above_0 = macd.iloc[-1] > 0

    if (last_closed_color == 'Bear' and 
        last_last_closed_color == 'Bear' and 
        current_color == 'Bull' and 
        above_50d_sma and 
        macd_above_0):
        smbpxy = 'Buy'
    else:
        smbpxy = 'Hold'

    return smbpxy

async def send_telegram_message(bot_token, user_id, message_text):
    bot = telegram.Bot(token=bot_token)
    await bot.send_message(chat_id=user_id, text=message_text)

def place_order(symbol, broker, purchase_limit, quantity):
    try:
        remaining_cash = available_cash
        ltp_nse = broker.kite.ltp("NSE:" + symbol)[f"NSE:{symbol}"]['last_price']
        
        if ltp_nse > 0 and remaining_cash > purchase_limit:
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
                logger.info(f"BUY {order_id} placed for {symbol} successfully")
                remaining_cash -= quantity * ltp_nse
                print(f"Order placed successfully for {symbol}")

                message_text = (f"📊 Let's Buy {symbol}!\n"
                                f"📈 Current Price (LTP): {ltp_nse}\n"
                                f"🔍 Check it out on TradingView: https://www.tradingview.com/chart/?symbol={symbol}")
                
                asyncio.run(send_telegram_message(BOT_TOKEN, USER_ID, message_text))
            else:
                logger.warning(f"Failed to place order for {symbol}")
        else:
            logger.warning(f"Skipping {symbol}: no LTP or no cash")
    except Exception as e:
        logger.error(f"Error while placing order: {str(e)}")

def main():
    symbols = [
        "KARURVYSYA", "KOTAKBANK", "KTKBANK", "MAHABANK", "PNB", "PSB", "RBLBANK", "SBIN",
        "SOUTHBANK", "SURYODAY", "TMB", "UCOBANK", "UJJIVANSFB", "UNIONBANK", "UTKARSHBNK",
        "YESBANK", "AUBANK", "AXISBANK", "BANDHANBNK", "BANKBARODA", "BANKINDIA", "CANBK",
        "CAPITALSFB", "CENTRALBK", "CSBBANK", "CUB", "DCBBANK", "DHANBANK", "EQUITASBNK",
        "ESAFSFB", "FEDERALBNK", "FINOPB", "HDFCBANK", "ICICIBANK", "IDBI", "IDFCFIRSTB",
        "INDIANB", "INDUSINDBK", "IOB", "J&KBANK", "JSFB", "WIPRO", "ULTRACEMCO", "TITAN",
        "TECHM", "TCS", "TATASTEEL", "TATAMOTORS", "TATACONSUM", "SUNPHARMA", "SHRIRAMFIN",
        "SBILIFE", "RELIANCE", "POWERGRID", "ONGC", "NTPC", "NESTLEIND", "MARUTI", "M&M",
        "LTIM", "LT", "JSWSTEEL", "ITC", "INFY", "HINDUNILVR", "HINDALCO", "HEROMOTOCO",
        "HDFCLIFE", "HCLTECH", "GRASIM", "EICHERMOT", "DRREDDY", "DIVISLAB", "COALINDIA",
        "CIPLA", "BRITANNIA", "BPCL", "BHARTIARTL", "BAJFINANCE", "BAJAJFINSV", "BAJAJ-AUTO",
        "ASIANPAINT", "APOLLOHOSP", "ADANIPORTS", "ADANIENT"
    ]

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
        # Reset sys.stdout to its default value
        sys.stdout = sys.__stdout__

    try:
        lst_dct_positions = broker.kite.positions()
        positions_symbols = [pos["tradingsymbol"] for pos in lst_dct_positions["day"] + lst_dct_positions["net"]]
    except Exception as e:
        logger.error(f"{str(e)} unable to read positions")
        positions_symbols = []

    try:
        lst_dct_orders = broker.orders
        orders_symbols = [order.get("tradingsymbol", "Unknown Symbol") for order in lst_dct_orders]
    except Exception as e:
        logger.error(f"{str(e)} unable to read orders")
        orders_symbols = []

    try:
        holdings = broker.kite.holdings()
        holdings_symbols = [holding["tradingsymbol"] for holding in holdings]
    except Exception as e:
        logger.error(f"{str(e)} unable to read holdings")
        holdings_symbols = []

    skip_symbols = set(positions_symbols + orders_symbols)

    for symbol in symbols:
        decision, optdecision, available_cash,live_balance, limit = calculate_decision()
        if decision == "YES":
            yf_symbol = symbol + ".NS"
            smbpxy = check_ha_candles(yf_symbol)
            
            ltp_nse = broker.kite.ltp(f"NSE:{symbol}")[f"NSE:{symbol}"]['last_price']
            purchase_limit = 0  # Default value in case no condition matches

            if smbpxy == 'Buy' and ltp_nse < 10000:
                if symbol in holdings_symbols and symbol not in orders_symbols and symbol not in positions_symbols:
                    purchase_limit = 2000
                elif symbol not in holdings_symbols and symbol not in orders_symbols and symbol not in positions_symbols:
                    purchase_limit = 10000

                if purchase_limit > 0:
                    quantity = int(purchase_limit / ltp_nse)
                    print(f"Placing order for {symbol}...")
                    place_order(symbol, broker, purchase_limit, quantity)
                    remaining_cash = available_cash
                    print(f"Remaining Cash💰: {int(round(remaining_cash / 1000))}K")
                    
                    if remaining_cash < limit:
                        print(f"Cash: {int(remaining_cash)}, stopping further orders.")
                        break
                else:
                    logger.info(f"Skipping {symbol}: purchase_limit is not set")
            else:
                logger.info(f"Skipping {symbol}: smbpxy is not 'Buy' or price is too high")
        else:
            logger.info("Decision is not 'YES', skipping order placement.")

if __name__ == "__main__":
    main()
