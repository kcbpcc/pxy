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
    
        # Calculate the actual lengths to be printed
        n_length = min(int((n / 100) * max_total_length), max_total_length)
        x_length = min(int((x / 100) * max_total_length), max_total_length)
        m_length = min(int((m / 100) * max_total_length), max_total_length)
        
        # Print both the previous day's close and today's close in a single sentence with color
        
        
        print(Fore.LIGHTWHITE_EX + '━' * n_length, end='')
        
        if c > o:
            print(Fore.GREEN + '=' * x_length + Style.RESET_ALL, end='')
        elif o > c:
            print(Fore.RED + '=' * x_length + Style.RESET_ALL, end='')
        
        print(Fore.LIGHTWHITE_EX + '━' * m_length)
    
        
    except Exception as e:
        pass


