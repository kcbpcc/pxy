import warnings
import yfinance as yf
import pandas as pd
import colorama
from colorama import Fore, Style
from mktpxy import get_market_check
from nftpxy import nse_action, nse_power, Day_Change, Open_Change, OPTIONS
from optpxy import get_optpxy
from utcpxy import peak_time
from macdpxy import calculate_macd_signal
from smaftypxy import check_nifty_status

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Initialize colorama for colored output
colorama.init(autoreset=True)

# Get market data
onemincandlesequance, mktpxy = get_market_check()
optpxy = get_optpxy()
peak = peak_time()
macd = calculate_macd_signal("^NSEI")
SMAfty = check_nifty_status()

OHLC_COLUMNS = ['Open', 'High', 'Low', 'Close']

def get_nifty50_data(period="2d"):
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

def get_today_close(df):
    if not df.empty:
        return df.iloc[-1]['Close']
    else:
        return None

def dayprinter(o, h, l, c, prev_close):
    max_total_length = 10  # Maximum total length allowed for printing
    
    try:
        # Calculate candle lengths based on the difference between open and close
        candle_length = abs(c - o)
        upper_length = max(0, h - max(c, o))
        lower_length = max(0, min(c, o) - l)
        
        # Calculate the actual lengths to be printed
        n_length = int((lower_length / max_total_length) * 100)
        x_length = int((candle_length / max_total_length) * 100)
        m_length = int((upper_length / max_total_length) * 100)
        
        # Print both the previous day's close and today's close in a single sentence with color
        if c >= o:
            candle_color = Fore.GREEN  # Set candle color to green for upward movement
        else:
            candle_color = Fore.RED  # Set candle color to red for downward movement
        
        print(f"🔆{day_change_sign}{Day_Change:.2f}⌛️{open_change_sign}{Open_Change:.2f}", end='') 
        print(Fore.LIGHTWHITE_EX + '━' * n_length, end='')
        print(candle_color + '█' * x_length + Style.RESET_ALL, end='')
        print(Fore.LIGHTWHITE_EX + '━' * m_length, end='')
        print (f"⚡{nse_power:.2f}{onemincandlesequance}🚦{macd}{SMAftywave}")
    except Exception as e:
        print("Error in dayprinter:", e)

# Example usage in the main program
nifty50_ohlc = get_nifty50_data()
previous_day_close = get_previous_day_close(nifty50_ohlc)
today_close = get_today_close(nifty50_ohlc)

if previous_day_close is not None and today_close is not None:
    today_data = nifty50_ohlc.iloc[-1][OHLC_COLUMNS]
    dayprinter(*today_data, previous_day_close)
else:
    print("Unable to fetch data.")
