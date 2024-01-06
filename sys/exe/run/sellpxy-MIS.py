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

############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################

# Set the python3IOENCODING environment variable to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

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
        console.print(f"[red]Error determining smbpxy check for {symbol}: {e}[/red]")
        return 'NONE'

# Read symbols from the CSV file
csv_file_path = 'zlistpxy.csv'
symbol_df = pd.read_csv(csv_file_path)

# Process each symbol
for symbol_row in symbol_df.iloc[:, 0]:
    symbol = f"{symbol_row}.NS"  # Append ".NS" to each symbol
    smbpxy_check = get_smbpxy_check(symbol)
    console.print(f"[bold]{symbol} is:[/bold] ", end="")

    if "Bull" in smbpxy_check:
        console.print(f"[green]{smbpxy_check}[/green]" 🟢)
    elif "Buy" in smbpxy_check:
        console.print(f"[green]{smbpxy_check}[/green]"🟢)
    elif "NONE" in smbpxy_check:
        console.print(f"[yellow]{smbpxy_check}[/yellow]"⚪)
    elif "Sell" in smbpxy_check:
        console.print(f"[red]{smbpxy_check}[/red]"🔴)
    elif "Bear" in smbpxy_check:
        console.print(f"[red]{smbpxy_check}[/red]"🔴)
    else:
        console.print(smbpxy_check)



