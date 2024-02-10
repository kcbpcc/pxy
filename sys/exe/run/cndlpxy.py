import warnings

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Rest of your code here
import yfinance as yf
import pandas as pd
import colorama
from colorama import Fore, Style  # Add Style to the imports
from mktpxy import get_market_check
from nftpxy import nse_action, nse_power, Day_Change, Open_Change, OPTIONS
from optpxy import get_optpxy
from utcpxy import peak_time
from macdpxy import calculate_macd_signal
from smaftypxy import check_nifty_status
import subprocess
import sys

onemincandlesequance, mktpxy = get_market_check()
optpxy = get_optpxy()
peak = peak_time()
macd = calculate_macd_signal("^NSEI")
SMAfty = check_nifty_status()

colorama.init(autoreset=True)

OHLC_COLUMNS = ['Open', 'High', 'Low', 'Close']

def get_nifty50_data(period="7d"):
    ticker_symbol = "^NSEI"  # NIFTY50 index symbol on Yahoo Finance

    try:
        # Fetch historical data for the specified period
        nifty_data = yf.Ticker(ticker_symbol).history(period=period)

        # Extract OHLC data
        ohlc_data = nifty_data[OHLC_COLUMNS]

        return ohlc_data

    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error

def get_previous_day_close(df):
    if len(df) >= 2:
        return df.iloc[-2]['Close']
    else:
        # Handle the case when there are not enough rows in the DataFrame
        return None  # Or any default value or error handling you prefer

def get_today_close():
    nifty50_ohlc = get_nifty50_data(period="1d")  # Fetch data for 1 day
    if not nifty50_ohlc.empty:
        prev_close = get_previous_day_close(nifty50_ohlc)
        return nifty50_ohlc.iloc[-1]['Close'], prev_close
    else:
        return None, None  # Handle the case when data is not available

from colorama import Fore, Style
day_change_sign = '+' if Day_Change > 0 else ''
open_change_sign = '+' if Open_Change > 0 else ''
def dayprinter(o, h, l, c, prev_close):
    total_length = 40
    
    try:
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
        SMAftywave = (f"{Fore.GREEN}ﮩﮩ٨") if SMAfty == 'up' else (f"{Fore.RED}ﮩﮩ٨")
        print(f"🔆{day_change_sign}{Day_Change}⌛️{open_change_sign}{Open_Change}⚡{nse_power}|", end='')   
        print (f"{SMAftywave}{onemincandlesequance}🚦{macd}")
        print(Fore.LIGHTWHITE_EX + '━' * int((n / 100) * total_length), end='')
    
        if c > o:
            print(Fore.GREEN + '━' * int((x / 100) * total_length) + Style.RESET_ALL, end='')
        elif o > c:
            print(Fore.RED + '━' * int((x / 100) * total_length) + Style.RESET_ALL, end='')
        
        print(Fore.LIGHTWHITE_EX + '━' * int((m / 100) * total_length) + SMAftywave)
    except Exception as e:
        pass
    
    
    # Determine the color based on the comparison of today's close with yesterday's close
    color = Fore.GREEN if c > prev_close else Fore.RED

def option_to_trade():
    today_data = get_nifty50_data().iloc[-1][OHLC_COLUMNS]
    today_open = today_data['Open']
    today_close = today_data['Close']
    option_value = round(today_close / 50) * 50
    return option_value

# Example usage in the main program
previous_day_close = get_previous_day_close(get_nifty50_data())
today_close = get_today_close()

if previous_day_close is not None and today_close is not None:
    today_data = get_nifty50_data(period="1d").iloc[-1][OHLC_COLUMNS]
    dayprinter(*today_data, previous_day_close)
else:
    print("Unable to fetch data.")


