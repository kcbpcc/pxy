import time
import subprocess
import yfinance as yf
from nftpxy import nse_action, nse_power
from rich.console import Console
from rich.style import Style
from rich import print
from looppxy import loop_duration
import os
import sys

# Intervals
intervals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
periods = [2, 3, 4, 5, 6, 7]

# Create a Console instance for rich print formatting
console = Console()

# Function to calculate the Heikin-Ashi candle colors for the last three closed candles
def calculate_last_three_heikin_ashi_colors(symbol, interval):
    try:
        # Fetch real-time data for the specified interval
        data = yf.Ticker(symbol).history(period=f'{periods[-1]}d', interval=f'{interval}m')

        # Check if there is enough data
        if len(data) < 3:
            raise ValueError("Insufficient data for the specified interval")

        # Calculate Heikin-Ashi candles
        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

        # Calculate the colors of the last three closed candles
        current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
        last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
        second_last_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'

        return current_color, last_closed_color, second_last_closed_color
    except Exception as e:
        console.print(f"Error: {e}")
        return 'None', 'None', 'None'

# Function to determine the market check based on candle colors
def get_market_check(symbol):
    selected_interval = None

    # Dynamically select the first available interval
    for interval in intervals:
        try:
            calculate_last_three_heikin_ashi_colors(symbol, interval)
            selected_interval = interval
            break
        except Exception:
            continue

    if selected_interval is None:
        console.print("No valid interval found. Waiting for more data... 🕰️")
        return 'None'

    current_color, last_closed_color, second_last_closed_color = calculate_last_three_heikin_ashi_colors(symbol, selected_interval)

# Function to determine the smbpxy check based on candle colors
def get_smbpxy_check(symbol):
    try:
        # Loop through all intervals and periods
        for interval in intervals:
            for period in periods:
                current_color, last_closed_color, _ = calculate_last_three_heikin_ashi_colors(symbol, interval)

                if current_color and last_closed_color:
                    if current_color == last_closed_color:
                        return 'Bear' if current_color == 'Bear' else 'Bull'
                    else:
                        return 'Sell' if current_color == 'Bear' else 'Buy'
        return 'None'

    except ValueError:
        console.print(f"[red]Insufficient data points for Heikin-Ashi calculation for {symbol}[/red]")
        return 'None'
    except Exception as e:
        console.print(f"[red]Error determining smbpxy check: {e}[/red]")
        return 'None'




