
import sys
import os
import logging
import pandas as pd
from rich.console import Console
import yfinance as yf
from toolkit.logger import Logger
from cnstpxy import dir_path
from login_get_kite import get_kite

# Constants
BLACK_FILE = os.path.join(dir_path, "blacklist.txt")
LOG_FILE = "your_log_file.log"
CSV_FILE_PATH = "zlistpxy.csv"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=LOG_FILE
)

# Initialize logging
logger = Logger(10)

# Initialize console for rich print formatting
console = Console()

# Initialize Kite API
try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)
except Exception as e:
    logging.error(f"Error initializing Kite API: {str(e)}")
    sys.exit(1)

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
                logging.info(f"Sell signal for {symbol}")
                return f"Symbol: {symbol}, SMBPXY Check: {action}"

            elif (
                (current_color_day == 'Bull' and last_closed_color_day == 'Bear' and second_closed_color_day == 'Bear') and
                (current_color_min == 'Bull' and last_closed_color_min == 'Bear' and second_closed_color_min == 'Bear')
            ):
                action = 'Buy'
                logging.info(f"Buy signal for {symbol}")
                return f"Symbol: {symbol}, SMBPXY Check: {action}"

            else:
                action = 'NONE'

        return f"Symbol: {symbol}, SMBPXY Check: {action}, Status: No action"

    except Exception as e:
        console.print(f"[red]Error determining smbpxy check for {symbol}: {e}[/red]")
        return f"Symbol: {symbol}, SMBPXY Check: NONE, Status: Error determining smbpxy check"

# Function to calculate the Heikin-Ashi candle colors for the last three closed candles (1-day interval)
def calculate_last_three_heikin_ashi_colors_day(symbol):
    try:
        data = yf.Ticker(symbol).history(period='5d', interval='1d')
        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

        current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
        last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
        second_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'

        return current_color, last_closed_color, second_closed_color
    except Exception as e:
        logging.error(f"Error calculating Heikin-Ashi colors for {symbol} (1-day): {str(e)}")
        raise

# Function to calculate the Heikin-Ashi candle colors for the last three closed candles (5-minute interval)
def calculate_last_three_heikin_ashi_colors_min(symbol):
    try:
        data = yf.Ticker(symbol).history(period='1d', interval='5m')
        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

        current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
        last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
        second_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'

        return current_color, last_closed_color, second_closed_color
    except Exception as e:
        logging.error(f"Error calculating Heikin-Ashi colors for {symbol} (5-minute): {str(e)}")
        raise

# Assuming 'calculated' column needs to be set to 1 for all rows
calculated = 1

try:
    symbol_df = pd.read_csv(CSV_FILE_PATH)
except FileNotFoundError:
    logging.error(f"CSV file '{CSV_FILE_PATH}' not found.")
    sys.exit(1)

for _, row in symbol_df.iterrows():
    symbol_row = row['STOCK']

    # Check SMBPXY and print result
    smbpxy_check_result = get_smbpxy_check(symbol_row + ".NS")

    # Print smbpxy_check result
    console.print(smbpxy_check_result)

    # Check if an order was placed
    if "Buy signal" in smbpxy_check_result or "Sell signal" in smbpxy_check_result:
        console.print(f"[green]Signal detected for {symbol_row}[/green]")
    else:
        console.print(f"[yellow]No signal detected for {symbol_row}[/yellow]")



