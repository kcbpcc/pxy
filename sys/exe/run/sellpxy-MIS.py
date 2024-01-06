import time
import subprocess
import warnings
from rich import print
from rich.console import Console
import sys
import yfinance as yf
import os
import pandas as pd

# Set the python3IOENCODING environment variable to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def get_smbpxy_check(symbol):
    def calculate_ha_candles(periods, interval):
        # Fetch real-time data for the specified interval
        data = yf.Ticker(symbol).history(period=f'{periods}d', interval=f'{interval}m')

        # Calculate Heikin-Ashi candles
        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

        # Calculate the colors of the last three closed candles
        current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
        last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
        second_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'

        return current_color, last_closed_color, second_closed_color

    # Example for daily candles (1 day interval)
    periods_daily = 5  # Example: 5 days
    interval_daily = 1  # 1 day interval
    current_color_daily, last_closed_color_daily, second_closed_color_daily = calculate_ha_candles(periods_daily, interval_daily)

    # Example for 5-minute candles (5 minutes interval)
    periods_5min = 50  # Example: 50 intervals (totaling 250 minutes for a 5-minute interval)
    interval_5min = 5  # 5-minute interval
    current_color_5min, last_closed_color_5min, second_closed_color_5min = calculate_ha_candles(periods_5min, interval_5min)

    # Check conditions for BUY and SELL signals based on your criteria for both daily and 5-minute intervals
    buy_condition = second_closed_color_daily == 'Bear' and last_closed_color_daily == 'Bear' and current_color_daily == 'Bull' and second_closed_color_5min == 'Bear' and last_closed_color_5min == 'Bear' and current_color_5min == 'Bull'
    sell_condition = second_closed_color_daily == 'Bull' and last_closed_color_daily == 'Bull' and current_color_daily == 'Bear' and second_closed_color_5min == 'Bull' and last_closed_color_5min == 'Bull' and current_color_5min == 'Bear'

    # Return signals
    if buy_condition:
        return "Buy"
    elif sell_condition:
        return "Sell"
    else:
        return "NONE"

csv_file_path = 'zlistpxy.csv'
symbol_df = pd.read_csv(csv_file_path, header=0)  # Assuming the header is in the first row

# Process each symbol
for symbol_row in symbol_df['STOCK']:
    symbol = f"{symbol_row}.NS"  # Append ".NS" to each symbol
    smbpxy_check = get_smbpxy_check(symbol)
    console = Console()
    console.print(f"[bold]{symbol}:[/bold] ", end="")
    
    if "Buy" in smbpxy_check:
        console.print(f"[green]{smbpxy_check}[/green] 🔴🟢🟢")
    elif "Sell" in smbpxy_check:
        console.print(f"[red]{smbpxy_check}[/red] 🟢🔴🔴")

