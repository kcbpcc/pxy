import yfinance as yf
import pandas as pd
import warnings
from rich.console import Console

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Function to calculate the Heikin-Ashi candle colors for the last two closed candles
def calculate_last_two_heikin_ashi_colors(symbol, interval):
    try:
        data = yf.Ticker(symbol).history(period='5d', interval=f'{interval}m')
        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2
        current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
        last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
        return current_color, last_closed_color
    except NoDataError as e:
        print(f"NoDataError occurred: {e}")
        return None, None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None, None

def get_smbpxy_check(symbol, interval, period='5d'):
    try:
        current_color, last_closed_color, second_last_closed_color = calculate_last_three_heikin_ashi_colors(symbol, interval, period)

        if current_color and last_closed_color and second_last_closed_color:
            if current_color == 'Bear' and last_closed_color == 'Bear':
                smbpxy = 'Bear'
            elif current_color == 'Bull' and last_closed_color == 'Bull':
                smbpxy = 'Bull'
            elif current_color == 'Bear' and last_closed_color == 'Bull':
                smbpxy = 'Sell'
            elif current_color == 'Bull' and last_closed_color == 'Bear':
                smbpxy = 'Buy'
            else:
                smbpxy = 'None'
        else:
            smbpxy = 'None'

        return smbpxy

    except NoDataError:
        #console.print(f"[red]No data found for {symbol}, symbol may be delisted[/red]")
        return None
    except InsufficientDataError:
        #console.print(f"[red]Insufficient data points for Heikin-Ashi calculation for {symbol}[/red]")
        return None
    except Exception as e:
        #console.print(f"[red]Error determining smbpxy check: {e}[/red]")
        return 'None'

