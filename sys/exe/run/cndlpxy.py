import warnings
import yfinance as yf
import pandas as pd
import colorama
from colorama import Fore, Style  # Add Style to the imports

colorama.init(autoreset=True)

OHLC_COLUMNS = ['Open', 'High', 'Low', 'Close']

def get_nifty50_data(days=2):
    ticker_symbol = "^NSEI"  # NIFTY50 index symbol on Yahoo Finance

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=FutureWarning)
            # Create a Ticker object
            nifty_ticker = yf.Ticker(ticker_symbol)

            # Get historical data for specified number of days
            nifty_data = nifty_ticker.history(period=f'{days}d')

        # Extract OHLC data
        ohlc_data = nifty_data[OHLC_COLUMNS]

        return ohlc_data

    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error

def get_previous_day_close():
    nifty50_ohlc = get_nifty50_data(days=2)
    if not nifty50_ohlc.empty:
        return nifty50_ohlc.iloc[-2]['Close']
    else:
        return None  # Handle the case when data is not available

def get_today_close():
    nifty50_ohlc = get_nifty50_data(days=1)
    if not nifty50_ohlc.empty:
        return nifty50_ohlc.iloc[-1]['Close']
    else:
        return None  # Handle the case when data is not available

def dayprinter(o, h, l, c, prev_close, use_heikin_ashi=False):
    total_length = 43
    
    if use_heikin_ashi:
        ha_close = (o + h + l + c) / 4
        arrow = " ━━🟢━━ " if ha_close > prev_close else " ━━🔴━━ "
        print(f"Heikin-Ashi Yesterday:{int(prev_close)} {arrow} Today-Now:{int(ha_close)}")
    else:
        arrow = " ━━🟩━━ " if c > prev_close else " ━━🟥━━ "
        print(f"Yesterday:{int(prev_close)} {arrow} Today-Now:{int(c)}")

    # Calculate the lengths of different segments as percentages
    if c > o:
        print(Fore.GREEN + '▌' * int((abs(c - o) / (h - l)) * 100) + Style.RESET_ALL, end='')
    elif o > c:
        print(Fore.RED + '▌' * int((abs(c - o) / (h - l)) * 100) + Style.RESET_ALL, end='')

    print(Fore.LIGHTWHITE_EX + '━' * int(((h - l) - abs(c - o)) / (h - l) * total_length))
    
    # Determine the color based on the comparison of today's close with yesterday's close
    color = Fore.GREEN if (use_heikin_ashi and ha_close > prev_close) else (Fore.GREEN if c > prev_close else Fore.RED)
    
def option_to_trade():
    today_data = get_nifty50_data().iloc[-1][OHLC_COLUMNS]
    today_open = today_data['Open']
    today_close = today_data['Close']
    option_value = round(today_close / 50) * 50
    return option_value

# Example usage in the main program
previous_day_close = get_previous_day_close()
today_close = get_today_close()

if previous_day_close is not None and today_close is not None:
    today_data = get_nifty50_data().iloc[-1][OHLC_COLUMNS]
    dayprinter(*today_data, previous_day_close)
else:
    print("Unable to fetch data.")
