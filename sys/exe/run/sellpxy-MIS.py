#PXY®
import sys
import os
import time
import datetime
import subprocess
import warnings
import csv
import random
import asyncio
import logging
import numpy as np
import pandas as pd
import yfinance as yf
from rich import print
from rich.console import Console
from rich.style import Style
import telegram
from colorama import Fore, Style
from cnstpxy import dir_path, sellbuff, secs, perc_col_name
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from login_get_kite import get_kite, remove_token
from mktpxy import get_market_check
from nftpxy import nse_action, nse_power, Day_Change, Open_Change
from bukdpxy import sum_last_numerical_value_in_each_row
from swchpxy import analyze_stock
from selfpxy import get_random_spiritual_message
import logging
mktpxy = get_market_check('^NSEI')
from fundpxy import calculate_decision

############################################"PXY® PreciseXceleratedYield Pvt Ltd™###########################################
sys.stdout = open('output.txt', 'w')
logging = Logger(30, dir_path + "main.log")
try:

    broker = get_kite(api="bypass", sec_dir=dir_path)
    decision = calculate_decision()
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} Unable to get holdings")
    sys.exit(1)
sys.stdout.close()
sys.stdout = sys.__stdout__
############################################"PXY® PreciseXceleratedYield Pvt Ltd™###########################################
def mis_sell_order_place(STOCK):
    try:
        # Specify the stock symbol without '.NS' or any exchange suffix
        symbol = STOCK.split(".")[0]

        # Fetch stock information using yfinance
        stock_info = yf.Ticker(STOCK)
        ltp = stock_info.history(period='1d')['Close'].iloc[-1]

        if not np.isnan(ltp) and ltp > 0:
            calculated_quantity = round(50000 / ltp)
            logging.info(f"Placing order for {symbol} with calculated quantity: {calculated_quantity}")

            # Use the extracted symbol for order placement
            order_id = broker.order_place(
                tradingsymbol=symbol,
                exchange='NSE',
                transaction_type='SELL',
                quantity=calculated_quantity,
                order_type='MARKET',
                product='CNC',
                variety='regular',
                price=None
            )

            if order_id:
                logging.info(f"Order {order_id} placed successfully")
                return True
            else:
                logging.error("Order placement failed")
        else:
            logging.error("Invalid last traded price (ltp)")
    except Exception as e:
        logging.error(f"{str(e)} while placing order")
    return False

############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################

# Set the python3IOENCODING environment variable to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Specify the stock symbol (NIFTY 50)
symbol = '^NSEI'

# Intervals
intervals = [5, 4, 3, 2, 1]
periods = [1, 2, 3, 4, 5]

# Create a Console instance for rich print formatting
console = Console()

# Function to calculate the Heikin-Ashi candle colors for the last three closed candles
def calculate_last_three_heikin_ashi_colors(symbol, interval):
    # Check if the current time is within the specified time range (3:45 AM to 4:00 AM UTC)
    current_utc_time = time.gmtime().tm_hour * 60 + time.gmtime().tm_min

    if 222 <= current_utc_time < 233:
        sys.stdout = open(os.devnull, 'w')

        # Download data for the specified number of days (fixed to 5 days)
        data = yf.download(symbol, period="5d")
        
        # Extract today's open, yesterday's close, and current price
        today_open = data['Open'].iloc[-1]
        today_high = data['High'].iloc[-1]
        today_low = data['Low'].iloc[-1]
        current_price = data['Close'].iloc[-1]
        
        yesterday_close = data['Close'].iloc[-2]
        yesterday_open = data['Open'].iloc[-2]
        
        sys.stdout.close()
        sys.stdout = sys.__stdout__

        day_open = today_open  # Open of the day
        ltp = current_price  # Last traded price
    
        current_color = 'Bear' if day_open > ltp else 'Bull'
        last_closed_color = 'Bear' if day_open > ltp else 'Bull'
        second_closed_color = 'Bear' if day_open > ltp else 'Bull'
    else:
        # Fetch real-time data for the specified interval
        data = yf.Ticker(symbol).history(period=f'{periods[0]}d', interval=f'{interval}m')

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
            for period in periods:
                current_color, last_closed_color, second_closed_color = calculate_last_three_heikin_ashi_colors(symbol, interval)

                if current_color and last_closed_color:
                    if current_color == 'Bear' and last_closed_color == 'Bear' and second_closed_color == 'Bear':
                        return 'Bear'
                    elif current_color == 'Bull' and last_closed_color == 'Bull' and second_closed_color == 'Bull':
                        return 'Bull'
                    elif current_color == 'Bear' and last_closed_color == 'Bear' and second_closed_color == 'Bull':
                        return 'Sell'
                    elif current_color == 'Bull' and last_closed_color == 'Bull' and second_closed_color == 'Bear':
                        return 'Buy'
                    else:
                        return 'NONE'

        return 'NONE'

    except Exception as e:
        console.print(f"[red]Error determining smbpxy check: {e}[/red]")
        return 'NONE'

############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
# Read symbols from a CSV file
csv_file_path = 'listpxy-MIS.csv'
symbol_df = pd.read_csv(csv_file_path, header=0)

# Process each symbol
for symbol_row in symbol_df['STOCK'] :
    symbol = f"{symbol_row}.NS"  # Append ".NS" to each symbol
    smbpxy_check = get_smbpxy_check(symbol)

    console = Console()
    console.print(f"[bold]{symbol}:[/bold] ", end="")

    try:
        if "Sell" in smbpxy_check and mktpxy == "Sell" and decision == "YES":
            console.print(f"[red]{smbpxy_check}[/red] 🔴🔴🔴")
            success = mis_sell_order_place(symbol)
            if success:
                print(f"Order for {symbol} placed successfully!")
            else:
                print(f"Failed to place order for {symbol}. Check logs for details.")
        elif mktpxy == "Sell" and decision == "YES": 
            console.print(f"[green]{smbpxy_check}[/green] ")
            success = mis_sell_order_place(symbol)
    except Exception as e:
        print(f"Error processing symbol {symbol}: {e}")
mktpxy = get_market_check('^NSEI')
