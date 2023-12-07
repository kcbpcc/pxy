import yfinance as yf
import pandas as pd
import warnings
from rich.console import Console
from rich.progress import track
from requests.exceptions import Timeout

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

console = Console()

intervals = [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
periods = [1, 2, 3, 4, 5, 6, 7]

def calculate_last_two_heikin_ashi_colors(symbol, period, interval):
    try:
        # Using specified periods and intervals for past and current candle
        data = yf.Ticker(symbol).history(period=f'{period}d', interval=f'{interval}m')

        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

        current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
        last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'

        return current_color, last_closed_color

    except Timeout:
        console.print("[red]Timeout error: Request to Yahoo Finance timed out[/red]")
        raise
    except Exception as e:
        console.print(f"[red]Exception occurred: {e}[/red]")
        return 'Error', 'Error'

def get_smbpxy_check(symbol):
    try:
        for interval in track(intervals, description="Intervals"):
            for period in periods:
                try:
                    current_color, last_closed_color = calculate_last_two_heikin_ashi_colors(symbol, period, interval)

                    if current_color and last_closed_color:
                        if current_color == 'Bear' and last_closed_color == 'Bear':
                            return 'Bear'
                        elif current_color == 'Bull' and last_closed_color == 'Bull':
                            return 'Bull'
                        elif current_color == 'Bear' and last_closed_color == 'Bull':
                            return 'Sell'
                        elif current_color == 'Bull' and last_closed_color == 'Bear':
                            return 'Buy'
                        else:
                            return 'None'

                except Exception as e:
                    console.print(f"[red]Error in period {period} and interval {interval}: {e}[/red]")

        return 'None'

    except Exception as e:
        console.print(f"[red]Error determining smbpxy check: {e}[/red]")
        return 'None'

for interval in range(min_interval, max_interval + 1):
    for retry in range(max_retries):
        try:
            result = get_smbpxy_check(symbol)
            if result != 'None':
                print(f"Smbpxy check result for interval {interval}: {result}")
                break
            else:
                print(f"No data found for interval {interval}. Trying the next interval.")
        except Timeout:
            print(f"Timeout error. Retrying...")


