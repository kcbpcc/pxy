import time
import subprocess
import warnings
from rich import print
from rich.console import Console
from rich.style import Style
import sys
import yfinance as yf
import os
import pandas as pd

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
    data = yf.Ticker(symbol).history(period=f'{periods[0]}d', interval='def get_smbpxy_check(symbol):
    try:
        # Loop through all intervals and periods
        for interval in intervals:
            # Check 1-day interval
            current_color_day, last_closed_color_day, second_closed_color_day = calculate_last_three_heikin_ashi_colors_day(symbol)

            # Check 5-minute interval
            current_color_min, last_closed_color_min, second_closed_color_min = calculate_last_three_heikin_ashi_colors_min(symbol)

            # Print statements for debugging
            print(f"Symbol: {symbol}, 1-day interval: {current_color_day}, {last_closed_color_day}, {second_closed_color_day}")
            print(f"Symbol: {symbol}, 5-minute interval: {current_color_min}, {last_closed_color_min}, {second_closed_color_min}")

            # Determine the overall condition based on both intervals
            if (
                (current_color_day == 'Bear' and last_closed_color_day == 'Bear' and second_closed_color_day == 'Bear') or
                (current_color_min == 'Bear' and last_closed_color_min == 'Bear' and second_closed_color_min == 'Bear')
            ):
                return 'Bear'
            elif (
                (current_color_day == 'Bull' and last_closed_color_day == 'Bull' and second_closed_color_day == 'Bull') or
                (current_color_min == 'Bull' and last_closed_color_min == 'Bull' and second_closed_color_min == 'Bull')
            ):
                return 'Bull'
            elif (
                (current_color_day == 'Bear' and last_closed_color_day == 'Bear' and second_closed_color_day == 'Bull') or
                (current_color_min == 'Bear' and last_closed_color_min == 'Bear' and second_closed_color_min == 'Bull')
            ):
                return 'Sell'
            elif (
                (current_color_day == 'Bull' and last_closed_color_day == 'Bull' and second_closed_color_day == 'Bear') or
                (current_color_min == 'Bull' and last_closed_color_min == 'Bull' and second_closed_color_min == 'Bear')
            ):
                return 'Buy'
            else:
                return 'NONE'

        return 'NONE'

    except Exception as e:
        console.print(f"[red]Error determining smbpxy check for {symbol}: {e}[/red]")
        return 'NONE'def get_smbpxy_check(symbol):
    try:
        # Loop through all intervals and periods
        for interval in intervals:
            # Check 1-day interval
            current_color_day, last_closed_color_day, second_closed_color_day = calculate_last_three_heikin_ashi_colors_day(symbol)

            # Check 5-minute interval
            current_color_min, last_closed_color_min, second_closed_color_min = calculate_last_three_heikin_ashi_colors_min(symbol)

            # Print statements for debugging
            print(f"Symbol: {symbol}, 1-day interval: {current_color_day}, {last_closed_color_day}, {second_closed_color_day}")
            print(f"Symbol: {symbol}, 5-minute interval: {current_color_min}, {last_closed_color_min}, {second_closed_color_min}")

            # Determine the overall condition based on both intervals
            if (
                (current_color_day == 'Bear' and last_closed_color_day == 'Bear' and second_closed_color_day == 'Bear') or
                (current_color_min == 'Bear' and last_closed_color_min == 'Bear' and second_closed_color_min == 'Bear')
            ):
                return 'Bear'
            elif (
                (current_color_day == 'Bull' and last_closed_color_day == 'Bull' and second_closed_color_day == 'Bull') or
                (current_color_min == 'Bull' and last_closed_color_min == 'Bull' and second_closed_color_min == 'Bull')
            ):
                return 'Bull'
            elif (
                (current_color_day == 'Bear' and last_closed_color_day == 'Bear' and second_closed_color_day == 'Bull') or
                (current_color_min == 'Bear' and last_closed_color_min == 'Bear' and second_closed_color_min == 'Bull')
            ):
                return 'Sell'
            elif (
                (current_color_day == 'Bull' and last_closed_color_day == 'Bull' and second_closed_color_day == 'Bear') or
                (current_color_min == 'Bull' and last_closed_color_min == 'Bull' and second_closed_color_min == 'Bear')
            ):
                return 'Buy'
            else:
                return 'NONE'

        return 'NONE'

    except Exception as e:
        console.print(f"[red]Error determining smbpxy check for {symbol}: {e}[/red]")
        return 'NONE'')

def calculate_last_three_heikin_ashi_colors_day(symbol):
    # Fetch real-time data for the specified interval
    data = yf.Ticker(symbol).history(period=f'{periods[0]}d', interval='1d')

    # Calculate Heikin-Ashi candles
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    # Calculate the colors of the last three closed candles
    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
    second_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'

    return current_color, last_closed_color, second_closed_color
    
def calculate_last_three_heikin_ashi_colors_min(symbol):
    # Fetch real-time data for the specified interval
    data = yf.Ticker(symbol).history(period=f'{periods[0]}d', interval='5m')

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
            print(f"Symbol: {symbol}, 1-day interval: {current_color_day}, {last_closed_color_day}, {second_closed_color_day}")
            print(f"Symbol: {symbol}, 5-minute interval: {current_color_min}, {last_closed_color_min}, {second_closed_color_min}")

            # Determine the overall condition based on both intervals
            if (
                (current_color_day == 'Bear' and last_closed_color_day == 'Bear' and second_closed_color_day == 'Bear') or
                (current_color_min == 'Bear' and last_closed_color_min == 'Bear' and second_closed_color_min == 'Bear')
            ):
                return 'Bear'
            elif (
                (current_color_day == 'Bull' and last_closed_color_day == 'Bull' and second_closed_color_day == 'Bull') or
                (current_color_min == 'Bull' and last_closed_color_min == 'Bull' and second_closed_color_min == 'Bull')
            ):
                return 'Bull'
            elif (
                (current_color_day == 'Bear' and last_closed_color_day == 'Bear' and second_closed_color_day == 'Bull') or
                (current_color_min == 'Bear' and last_closed_color_min == 'Bear' and second_closed_color_min == 'Bull')
            ):
                return 'Sell'
            elif (
                (current_color_day == 'Bull' and last_closed_color_day == 'Bull' and second_closed_color_day == 'Bear') or
                (current_color_min == 'Bull' and last_closed_color_min == 'Bull' and second_closed_color_min == 'Bear')
            ):
                return 'Buy'
            else:
                return 'NONE'

        return 'NONE'

    except Exception as e:
        console.print(f"[red]Error determining smbpxy check for {symbol}: {e}[/red]")
        return 'NONE'

# Read symbols from the CSV file
csv_file_path = 'zlistpxy.csv'
symbol_df = pd.read_csv(csv_file_path)

# Read symbols from fileHPdf.csv
exclude_symbols_path = 'fileHPdf.csv'
exclude_symbols_df = pd.read_csv(exclude_symbols_path, header=None)  # Assuming no header in fileHPdf.csv

# Create a set of symbols to exclude
exclude_symbols_set = set(exclude_symbols_df.iloc[:, 0])

# Process each symbol
for symbol_row in symbol_df.iloc[:, 0]:
    symbol_with_ns = f"{symbol_row}.NS"  # Append ".NS" to each symbol
    symbol_without_ns = symbol_row  # Symbol without ".NS" suffix

    # Check if the symbol with ".NS" suffix or without is in the exclusion list
    if symbol_with_ns not in exclude_symbols_set and symbol_without_ns not in exclude_symbols_set:
        smbpxy_check = get_smbpxy_check(symbol_with_ns)
        console.print(f"[bold]Symbol:[/bold] {symbol_with_ns}, [bold]SMBPXY Check:[/bold] {smbpxy_check}")
    else:
        console.print(f"[italic]Symbol:[/italic] {symbol_with_ns} [yellow]skipped (present in fileHPdf.csv)[/yellow]")



