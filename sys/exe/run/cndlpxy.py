import warnings
import yfinance as yf
import pandas as pd
import colorama
from colorama import Fore

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

def dayprinter(o, h, l, c, prev_close):
    total_length = 22
    
    # Calculate the lengths of different segments as percentages
    if c > o:
        n = round(((o - (l-1)) / ((h+1) - (l-1))) * 100)
        x = round(((c - o) / ((h+1) - (l-1))) * 100)
        m = 100 - n - x
    else:
        n = round(((c - (l-1)) / ((h+1) - (l-1))) * 100)
        x = round(((o - c) / ((h+1) - (l-1))) * 100)
        m = 100 - n - x

    # Print both the previous day's close and today's close in a single sentence with color
    arrow = " ━━🟢🟢━━ " if c > prev_close else " ━━🔴🔴━━ "
    print(f"Yesterday:{int(prev_close)} {arrow} Today-Now:{int(c)}")
    
    # Print the colored bar graph with red and green emojis
    print(Fore.LIGHTWHITE_EX + '🔴' * int((n / 100) * total_length), end='')
    if c > o:
        print(Fore.RED + '🟩' * int((x / 100) * total_length), end='')
    if o > c:
        print(Fore.GREEN + '🟥' * int((x / 100) * total_length), end='')
    print(Fore.LIGHTWHITE_EX + '🟢' * int((m / 100) * total_length))

    # Determine the color based on the comparison of today's close with yesterday's close
    color = Fore.GREEN if c > prev_close else Fore.RED

# Example usage in the main program
previous_day_close = get_previous_day_close()
today_close = get_today_close()

if previous_day_close is not None and today_close is not None:
    today_data = get_nifty50_data().iloc[-1][OHLC_COLUMNS]
    dayprinter(*today_data, previous_day_close)
else:
    print("Unable to fetch data.")
