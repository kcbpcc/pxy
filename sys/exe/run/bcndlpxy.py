import warnings

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Rest of your code here
import yfinance as yf
import pandas as pd
import colorama
from colorama import Fore, Style  # Add Style to the imports
from bnkpxy import bnk_action, bnk_power, Day_bnk_Change, Open_bnk_Change, OPTIONS
from utcpxy import peak_time
from macdpxy import calculate_macd_signal
from smapxy import check_index_status
import subprocess
import sys
from mktpxy import get_market_check
bnk_onemincandlesequance, bktpxy = get_market_check('^NSEBANK')
peak = peak_time()
macd = calculate_macd_signal('^NSEBANK')
bsma = check_index_status('^NSEBANK')
from depthpxy import calculate_consecutive_candles
cedepth, pedepth = calculate_consecutive_candles('^NSEBANK')

colorama.init(autoreset=True)

OHLC_COLUMNS = ['Open', 'High', 'Low', 'Close']

def get_nifty50_data(period="7d"):
    ticker_symbol = '^NSEBANK'  # NIFTY50 index symbol on Yahoo Finance

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
Day_bnk_Change_sign = '+' if Day_bnk_Change >= 0 else ''
Open_bnk_Change_sign = '+' if Open_bnk_Change >= 0 else ''

def dayprinter(o, h, l, c, prev_close):
    max_total_length = 42  # Maximum total length allowed for printing
    
    try:
        # Calculate the lengths of different segments as percentages of H - L
        candle_length = h - l
        if c > o:
            n = round(((o - l) / candle_length) * 100)
            x = round(((c - o) / candle_length) * 100)
            m = 100 - n - x
        else:
            n = round(((c - l) / candle_length) * 100)
            x = round(((o - c) / candle_length) * 100)
            m = 100 - n - x
    
        # Calculate the actual lengths to be printed
        n_length = round((n / 100) * max_total_length)
        x_length = round((x / 100) * max_total_length)
        m_length = max_total_length - n_length - x_length
        
        # Print both the previous day's close and today's close in a single sentence with color
        print(Fore.LIGHTWHITE_EX + '━' * n_length, end='')
        if c > o:
            print(Fore.GREEN + '━' * x_length + Style.RESET_ALL, end='')
        elif o > c:
            print(Fore.RED + '━' * x_length + Style.RESET_ALL, end='')
        print(Fore.LIGHTWHITE_EX + '━' * m_length)
    
    except Exception as e:
        pass
    
    # Determine the color based on the comparison of today's close with yesterday's close
    color = Fore.GREEN if c > prev_close else Fore.RED
    bsmawave = f"{Fore.GREEN}ﮩ٨ﮩ٨ـ{Style.RESET_ALL}" if bsma == 'up' else f"{Fore.RED}ﮩ٨ﮩ٨ـ{Style.RESET_ALL}"
    print(f"🔆{Day_bnk_Change_sign}{Day_bnk_Change:.2f}⌛️{Open_bnk_Change_sign}{Open_bnk_Change:.2f}⚡{bnk_power:.2f}{bsmawave}🚦{macd}PE{pedepth}|CE{cedepth}{bnk_onemincandlesequance}")


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
