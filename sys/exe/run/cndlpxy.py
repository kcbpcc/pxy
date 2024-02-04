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

def calculate_heikin_ashi_colors(nifty50_ohlc):
    if not nifty50_ohlc.empty:
        ha_close = (nifty50_ohlc.iloc[-1]['Close'] + nifty50_ohlc.iloc[-1]['High'] + nifty50_ohlc.iloc[-1]['Low'] + nifty50_ohlc.iloc[-1]['Open']) / 4
        ha_yclose = (nifty50_ohlc['Open'].shift(1) + nifty50_ohlc['Close'].shift(1)) / 2
    else:
        ha_close, ha_yclose = None, None
    
    return ha_close, ha_yclose
    
dayprinter(*today_data, previous_day_close, nifty50_ohlc)
    total_length = 24

    # Calculate the lengths of different segments as percentages
    if c > o:
        n = round(((o - (l - 1)) / ((h + 1) - (l - 1))) * 100)
        x = round(((c - o) / ((h + 1) - (l - 1))) * 100)
        m = 100 - n - x
    else:
        n = round(((c - (l - 1)) / ((h + 1) - (l - 1))) * 100)
        x = round(((o - c) / ((h + 1) - (l - 1))) * 100)
        m = 100 - n - x
    ha_close, ha_yclose = calculate_heikin_ashi_colors(nifty50_ohlc)
    haarrow = f"{Fore.GREEN}👆" if ha_close > ha_yclose else f"{Fore.RED}👇"
    arrow = (f"{Fore.GREEN}ﮩ٨ـﮩﮩ٨ـ") if c > prev_close else ("-", f"{Fore.RED}ﮩ٨ـﮩﮩ٨ـ")
    print((f"{Fore.GREEN}{'▌' * int((x / 100) * total_length)}" if c > o else f"{Fore.RED}{'▌' * int((x / 100) * total_length)}" if o > c else "") + f"{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}{'=' * int((m / 100) * total_length)}" + f"{Fore.LIGHTWHITE_EX}{int(prev_close)}{arrow}{int(c)}{haarrow}"+f"{'=' * int((n / 100) * total_length)}")

def option_to_trade(today_data):
    today_open = today_data['Open']
    today_close = today_data['Close']
    option_value = round(today_close / 50) * 50
    return option_value

# Example usage in the main program
nifty50_ohlc = get_nifty50_data()
previous_day_close = get_previous_day_close()
today_close = get_today_close()

if not nifty50_ohlc.empty and previous_day_close is not None and today_close is not None:
    today_data = nifty50_ohlc.iloc[-1][OHLC_COLUMNS]
    dayprinter(*today_data, previous_day_close

