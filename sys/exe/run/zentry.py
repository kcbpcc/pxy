import time
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

# Intervals
intervals = [5, 4, 3, 2, 1]
periods = [1, 2, 3, 4, 5]

# Create a Console instance for rich print formatting
console = Console()

# Function to calculate the Heikin-Ashi candle colors for the last three closed candles
def calculate_last_three_heikin_ashi_colors(symbol, interval):
    # ... (unchanged code)

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

    except yf.errors.YfinanceError as yfe:
        console.print(f"[red]Yfinance error determining smbpxy check for symbol {symbol}: {yfe}[/red]")
        return 'NONE'
    except Exception as e:
        console.print(f"[red]Error determining smbpxy check for symbol {symbol}: {e}[/red]")
        return 'NONE'

# Read symbols from CSV file
csv_file_path = 'yxplist.csv'  # Replace with the actual path
try:
    symbols_df = pd.read_csv(csv_file_path)
    
    # Append ".NS" to each symbol
    symbols_df['Symbol'] = symbols_df['Symbol'].astype(str) + '.NS'
    
    symbols_list = symbols_df['Symbol'].tolist()

    for symbol in symbols_list:
        smbpxy_result = get_smbpxy_check(symbol)
        console.print(f"SMBPXY check for {symbol}: {smbpxy_result}")

except FileNotFoundError as fnfe:
    console.print(f"[red]CSV file not found: {fnfe}[/red]")
except pd.errors.EmptyDataError:
    console.print("[red]CSV file is empty[/red]")
except Exception as e:
    console.print(f"[red]Error reading symbols from CSV file: {e}[/red]")


