import time
import subprocess
import warnings
from rich import print
from rich.console import Console
import sys
import yfinance as yf
import os
import pandas as pd
import traceback
import logging
import telegram
import asyncio
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite
from cnstpxy import dir_path, fileutils, buybuff, max_target
from buypluspxy import Trendlyne
from fundpxy import calculate_decision
from mktpxy import get_market_check

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='your_log_file.log'
)

try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)

async def send_telegram_message(message_text):
    bot = telegram.Bot(token=bot_token)
    await bot.send_message(chat_id=user_id, text=message_text)

def transact(dct, remaining_cash):
    try:
        ltp = -1

        def get_ltp(exchange):
            nonlocal ltp
            key = f"{exchange}:{dct['tradingsymbol']}"
            resp = broker.kite.ltp(key)
            if resp and isinstance(resp, dict):
                ltp = resp[key]['last_price']
            return ltp

        ltp_nse = get_ltp('NSE')
        logging.info(f"LTP for {dct['tradingsymbol']} on NSE is {ltp_nse}")

        if ltp_nse <= 0:
            ltp_bse = get_ltp('BSE')
            logging.info(f"LTP for {dct['tradingsymbol']} on BSE is {ltp_bse}")

            if ltp_bse > 0:
                ltp = ltp_bse
            else:
                return f"Status: No LTP available for {dct['tradingsymbol']}", remaining_cash

        quantity = int(10000 / ltp)

        if quantity > 0:
            order_id = broker.order_place(
                tradingsymbol=dct['tradingsymbol'],
                exchange='NSE' if ltp_nse > 0 else 'BSE',
                transaction_type='BUY',
                quantity=quantity,
                order_type='LIMIT',
                product='CNC',
                variety='regular',
                price=round_to_paise(ltp, 0)
            )
            if order_id:
                logging.info(
                    f"BUY {order_id} placed for {dct['tradingsymbol']} successfully")
                try:
                    message_text = f"{ltp} \nhttps://www.tradingview.com/chart/?symbol={dct['tradingsymbol']}"
                    asyncio.run(send_telegram_message(message_text))
                except Exception as e:
                    print(f"Error sending message to Telegram: {e}")
                return f"Status: Buy order placed for {dct['tradingsymbol']}", remaining_cash
            else:
                reason = f"Failed to place order for {dct['tradingsymbol']}: Order placement API did not return an order ID"
                logging.error(reason)
                return f"Status: {reason}", remaining_cash
        else:
            reason = f"Skipping {dct['tradingsymbol']}: Calculated quantity is not positive"
            logging.warning(f"Status: {reason}")
            return f"Status: {reason}", remaining_cash

    except Exception as e:
        logging.error(f"Error while placing order: {str(e)}")
        return f"Status: Error while placing order for {dct['tradingsymbol']}", remaining_cash

# Set the python3IOENCODING environment variable to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Intervals
intervals = [5, 4, 3, 2, 1]
periods = [2, 3, 4, 5]

# Create a Console instance for rich print formatting
console = Console()

# Function to calculate the Heikin-Ashi candle colors for the last three closed candles (1-day interval)
def calculate_last_three_heikin_ashi_colors_day(symbol):
    data = yf.Ticker(symbol).history(period='5d', interval='1d')
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
    second_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'

    return current_color, last_closed_color, second_closed_color

# Function to calculate the Heikin-Ashi candle colors for the last three closed candles (5-minute interval)
def calculate_last_three_heikin_ashi_colors_min(symbol):
    data = yf.Ticker(symbol).history(period='1d', interval='5m')
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
    second_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'

    return current_color, last_closed_color, second_closed_color

def get_smbpxy_check(symbol):
    try:
        for interval in intervals:
            current_color_day, last_closed_color_day, second_closed_color_day = calculate_last_three_heikin_ashi_colors_day(symbol)
            current_color_min, last_closed_color_min, second_closed_color_min = calculate_last_three_heikin_ashi_colors_min(symbol)

            if (
                (current_color_day == 'Bear' and last_closed_color_day == 'Bull' and second_closed_color_day == 'Bull') and
                (current_color_min == 'Bear' and last_closed_color_min == 'Bull' and second_closed_color_min == 'Bull')
            ):
                action = 'Sell'
                status, remaining_cash = transact(symbol, remaining_cash)
                logging.info(f"Sell order placed for {symbol}")
                return f"Symbol: {symbol}, SMBPXY Check: {action}, {status}"

            elif (
                (current_color_day == 'Bull' and last_closed_color_day == 'Bear' and second_closed_color_day == 'Bear') and
                (current_color_min == 'Bull' and last_closed_color_min == 'Bear' and second_closed_color_min == 'Bear')
            ):
                action = 'Buy'
                status, remaining_cash = transact(symbol, remaining_cash)
                logging.info(f"Buy order placed for {symbol}")
                return f"Symbol: {symbol}, SMBPXY Check: {action}, {status}"

            else:
                action = 'NONE'

        return f"Symbol: {symbol}, SMBPXY Check: {action}, Status: No action"

    except Exception as e:
        console.print(f"[red]Error determining smbpxy check for {symbol}: {e}[/red]")
        return f"Symbol: {symbol}, SMBPXY Check: NONE, Status: Error determining smbpxy check"

# Read symbols from the CSV file
csv_file_path = 'zlistpxy.csv'
symbol_df = pd.read_csv(csv_file_path)

# Read symbols from fileHPdf.csv
exclude_symbols_path = 'fileHPdf.csv'
exclude_symbols_df = pd.read_csv(exclude_symbols_path, header=None)

response = broker.kite.margins()
remaining_cash = response["equity"]["available"]["live_balance"]

# Create a set of symbols to exclude
exclude_symbols_set = set(exclude_symbols_df.iloc[:, 0])

# Process each symbol
for symbol_row in symbol_df.iloc[:, 0]:
    symbol_with_ns = f"{symbol_row}.NS"
    symbol_without_ns = symbol_row

    if symbol_with_ns not in exclude_symbols_set and symbol_without_ns not in exclude_symbols_set:
        smbpxy_check_result = get_smbpxy_check(symbol_with_ns)
        
        # Print smbpxy_check result
        console.print(smbpxy_check_result)

        # Check if an order was placed and print the result
        if "Buy order placed" in smbpxy_check_result or "Sell order placed" in smbpxy_check_result:
            console.print(f"[green]Order placed for {symbol_with_ns}[/green]")
        else:
            console.print(f"[yellow]No order placed for {symbol_with_ns}[/yellow]")
    else:
        console.print(f"[italic]Symbol:[/italic] {symbol_with_ns} [yellow]skipped (present in fileHPdf.csv)[/yellow]")


