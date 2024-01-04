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


try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)

def transact(dct, remaining_cash):

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

        # Calculate quantity based on the formula 10000 / ltp
        quantity = int(10000 / ltp)

        # Place the order only if the calculated quantity is positive
        if quantity > 0:
            # Place the order on the exchange where LTP is available
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
                # No need to calculate remaining available cash in this case

                try:
                    message_text = f"{ltp} \nhttps://www.tradingview.com/chart/?symbol={dct['tradingsymbol']}"

                    # Define the bot token and your Telegram username or ID
                    bot_token = '6603707685:AAFhWgPpliYjDqeBY24UyDipBbuBavcb4Bo'  # Replace with your actual bot token
                    user_id = '-4080532935'  # Replace with your Telegram user ID

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
                f"Skipping {dct['tradingsymbol']}: Calculated quantity is not positive")
        return dct['tradingsymbol'], remaining_cash

    except Exception as e:
        logging.error(f"Error while placing order: {str(e)}")
        return dct['tradingsymbol'], remaining_cash


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
    # Fetch real-time data for the specified interval
    data = yf.Ticker(symbol).history(period='5d', interval='1d')

    # Calculate Heikin-Ashi candles
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    # Calculate the colors of the last three closed candles
    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
    second_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'

    return current_color, last_closed_color, second_closed_color
    
# Function to calculate the Heikin-Ashi candle colors for the last three closed candles (5-minute interval)
def calculate_last_three_heikin_ashi_colors_min(symbol):
    # Fetch real-time data for the specified interval
    data = yf.Ticker(symbol).history(period='1d', interval='5m')

    # Calculate Heikin-Ashi candles
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    # Calculate the colors of the last three closed candles
    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
    second_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'

    return current_color, last_closed_color, second_closed_color

def get_smbpxy_check(symbol):
    try:
        # Loop through all intervals and periods
        for interval in intervals:
            # Check 1-day interval
            current_color_day, last_closed_color_day, second_closed_color_day = calculate_last_three_heikin_ashi_colors_day(symbol)

            # Check 5-minute interval
            current_color_min, last_closed_color_min, second_closed_color_min = calculate_last_three_heikin_ashi_colors_min(symbol)

            # Print statements for debugging
            # print(f"Symbol: {symbol}, 1-day interval: {current_color_day}, {last_closed_color_day}, {second_closed_color_day}")
            # print(f"Symbol: {symbol}, 5-minute interval: {current_color_min}, {last_closed_color_min}, {second_closed_color_min}")

            # Determine the overall condition based on both intervals
            if (
                (current_color_day == 'Bear' and last_closed_color_day == 'Bull' and second_closed_color_day == 'Bull') and
                (current_color_min == 'Bear' and last_closed_color_min == 'Bull' and second_closed_color_min == 'Bull')
            ):
                action = 'Sell'
                
                # Place order if condition is "Buy"
                symbol, remaining_cash = transact(symbol, remaining_cash)

                # Log the Buy action
                logging.info(f"Buy order placed for {symbol}")

                # Return the action after placing the order
                return action

            
            elif (
                (current_color_day == 'Bull' and last_closed_color_day == 'Bear' and second_closed_color_day == 'Bear') and
                (current_color_min == 'Bull' and last_closed_color_min == 'Bear' and second_closed_color_min == 'Bear')
            ):
                action = 'Buy'

                # Place order if condition is "Buy"
                symbol, remaining_cash = transact(symbol, remaining_cash)

                # Log the Buy action
                logging.info(f"Buy order placed for {symbol}")

                # Return the action after placing the order
                return action

            else:
                action = 'NONE'

        return action

    except Exception as e:
        console.print(f"[red]Error determining smbpxy check for {symbol}: {e}[/red]")
        return 'NONE'


# Read symbols from the CSV file
csv_file_path = 'zlistpxy.csv'
symbol_df = pd.read_csv(csv_file_path)

# Read symbols from fileHPdf.csv
exclude_symbols_path = 'fileHPdf.csv'
exclude_symbols_df = pd.read_csv(exclude_symbols_path, header=None)  # Assuming no header in fileHPdf.csv

response = broker.kite.margins()
available_cash = response["equity"]["available"]["live_balance"]


# Create a set of symbols to exclude
exclude_symbols_set = set(exclude_symbols_df.iloc[:, 0])

# Process each symbol
for symbol_row in symbol_df.iloc[:, 0]:
    symbol_with_ns = f"{symbol_row}.NS"  # Append ".NS" to each symbol
    symbol_without_ns = symbol_row  # Symbol without ".NS" suffix

    if symbol_with_ns not in exclude_symbols_set and symbol_without_ns not in exclude_symbols_set:
        smbpxy_check = get_smbpxy_check(symbol_with_ns)
        
        if smbpxy_check == 'Buy' or smbpxy_check == 'Sell':
            console.print(f"[bold]Symbol:[/bold] {symbol_with_ns}, [bold]SMBPXY Check:[/bold] {smbpxy_check}")
        else:
            console.print(f"[italic]Symbol:[/italic] {symbol_with_ns} [yellow]skipped (SMBPXY check returned None)[/yellow]")
    else:
        console.print(f"[italic]Symbol:[/italic] {symbol_with_ns} [yellow]skipped (present in fileHPdf.csv)[/yellow]")
