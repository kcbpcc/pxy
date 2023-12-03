import yfinance as yf
import pandas as pd
import warnings
from rich.console import Console

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def calculate_last_three_heikin_ashi_colors(symbol, interval, period='5d'):
    try:
        data = yf.Ticker(symbol).history(period=period, interval=f'{interval}m')
        
        if data.empty or len(data) < 3:
            return None, None, None

        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

        current_color = 'Buy' if ha_close.iloc[-1] > ha_open.iloc[-1] else 'Sell'
        last_closed_color = 'Buy' if ha_close.iloc[-2] > ha_open.iloc[-2] else 'Sell'
        second_last_closed_color = 'Buy' if ha_close.iloc[-3] > ha_open.iloc[-3] else 'Sell'

        return current_color, last_closed_color, second_last_closed_color

    except Exception as e:
        # Suppress any exception messages
        return None, None, None


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

