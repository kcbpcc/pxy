import warnings
import logging
import pandas as pd
import yfinance as yf
from rich.console import Console
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite
from cnstpxy import dir_path, fileutils, buybuff, max_target
from buypluspxy import Trendlyne
import pandas as pd
import traceback
import sys
import os
from fundpxy import calculate_decision
from mktpxy import get_market_check
import asyncio
import warnings
import logging
import pandas as pd
import yfinance as yf
from rich.console import Console

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='your_log_file.log'
)
mktchk = get_market_check('^NSEI')
logging = Logger(10)

try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)

except Exception as e:
    print(traceback.format_exc())
    sys.exit(1)
    
# Call the calculate_decision function to get the decision
decision = calculate_decision()

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Intervals
intervals = [5, 4, 3, 2, 1]

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

def order_place():
    try:
        exchsym = str(symbol)
        if len(exchsym) >= 2:
            logging.info(f"Placing order for {exchsym[1]}, {str(row)}")
            order_id = broker.order_place(
                tradingsymbol=exchsym[1],
                exchange=exchsym[0],
                transaction_type='SELL',
                quantity=int(row['qty']),
                order_type='LIMIT',
                product='CNC',
                variety='regular',
                price=round_to_paise(row['ltp'], -0.3)
            )
            if order_id:
                logging.info(f"Order {order_id} placed for {exchsym[1]} successfully")                                
                return True                
            else:
                logging.error("Order placement failed")       
        else:
            logging.error("Invalid format for 'index'")    
    except Exception as e:
        logging.error(f"{str(e)} while placing order")
    return False
    
# Function to check SMBPXY for a symbol
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
                status = order_place()
                logging.info(f"Sell order placed for {symbol}")
                return f"Symbol: {symbol}, SMBPXY Check: {action}, {status}"

            elif (
                (current_color_day == 'Bull' and last_closed_color_day == 'Bear' and second_closed_color_day == 'Bear') and
                (current_color_min == 'Bull' and last_closed_color_min == 'Bear' and second_closed_color_min == 'Bear')
            ):
                action = 'Buy'
                status = order_place()
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

# Process each symbol
for symbol_row in symbol_df.iloc[:, 0]:
    # Check SMBPXY and place order
    smbpxy_check_result = get_smbpxy_check(symbol_row+".NS")

    # Print smbpxy_check result
    console.print(smbpxy_check_result)

    # Check if an order was placed
    if "Buy order placed" in smbpxy_check_result or "Sell order placed" in smbpxy_check_result:
        console.print(f"[green]Order placed for {symbol_row}[/green]")
    else:
        console.print(f"[yellow]No order placed for {symbol_row}[/yellow]")
