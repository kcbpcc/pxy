import warnings

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import yfinance as yf
import pandas as pd
import colorama
import subprocess
import sys
from colorama import Fore, Style

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

def dayprinter(o, h, l, c, prev_close):
    max_total_length = 43  # Maximum total length allowed for printing
    color_code_length = 7  # Length of color codes such as Fore.GREEN
    
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
    
        # Adjust for the length of color codes
        available_length = max_total_length - color_code_length * 3
        
        # Calculate the actual lengths to be printed
        n_length = min(int((n / 100) * available_length), available_length)
        x_length = min(int((x / 100) * available_length), available_length)
        m_length = min(int((m / 100) * available_length), available_length)
        
        # Print both the previous day's close and today's close in a single sentence with color
        print(Fore.LIGHTWHITE_EX + '━' * n_length, end='')
        
        if c > o:
            print(Fore.GREEN + '=' * x_length + Style.RESET_ALL, end='')
        elif o > c:
            print(Fore.RED + '=' * x_length + Style.RESET_ALL, end='')
        
        print(Fore.LIGHTWHITE_EX + '━' * m_length)
    
        
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

