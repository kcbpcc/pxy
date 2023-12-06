import yfinance as yf
import pandas as pd
import warnings
from rich.console import Console
from yfinance.shared import NoDataError, InsufficientDataError


warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

console = Console()

intervals = [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
periods = [2, 3, 4, 5, 6, 7]

def calculate_last_two_heikin_ashi_colors(symbol, period, interval):
    try:
        # Using specified periods and intervals for past and current candle
        data = yf.Ticker(symbol).history(period=f'{period}d', interval=f'{interval}m')

        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

        current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
        last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'

        return current_color, last_closed_color

    except Exception as e:
        console.print(f"[red]Exception occurred: {e}[/red]")
        return 'Error', 'Error'

def get_smbpxy_check(symbol):
    try:
        # Loop through all intervals and periods
        for interval in intervals:
            for period in periods:
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

        return 'None'

    except yf.errors.NoDataError:
        console.print(f"[red]No data found for {symbol}, symbol may be delisted[/red]")
        return 'None'
    except yf.errors.InsufficientDataError:
        console.print(f"[red]Insufficient data points for Heikin-Ashi calculation for {symbol}[/red]")
        return 'None'

    except Exception as e:
        console.print(f"[red]Error determining smbpxy check: {e}[/red]")
        return 'None'

