import warnings
import importlib
import subprocess
import time
import warnings
from rich.console import Console
console = Console()
warnings.simplefilter(action='ignore', category=FutureWarning)
import yfinance as yf
import pandas as pd
import colorama
from colorama import Fore, Style  # Add Style to the imports
from mktpxy import get_market_check
from nftpxy import nse_action, nse_power, Day_Change, Open_Change, OPTIONS
from utcpxy import peak_time
from macdpxy import calculate_macd_signal
from smapxy import check_index_status
import subprocess
import sys
onemincandlesequance, mktpxy = get_market_check("^NSEI")
peak = peak_time()
macd = calculate_macd_signal("^NSEI")
nsma = check_index_status("^NSEI")
from depthpxy import calculate_consecutive_candles
cedepth, pedepth = calculate_consecutive_candles("^NSEI")
colorama.init(autoreset=True)
OHLC_COLUMNS = ['Open', 'High', 'Low', 'Close']
def get_nifty50_data(period="7d"):
    ticker_symbol = "^NSEI"  # NIFTY50 index symbol on Yahoo Finance
    try:
        nifty_data = yf.Ticker(ticker_symbol).history(period=period)
        ohlc_data = nifty_data[OHLC_COLUMNS]
        return ohlc_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error
def get_previous_day_close(df):
    if len(df) >= 2:
        return df.iloc[-2]['Close']
    else:
        return None  # Or any default value or error handling you prefer
def get_today_close():
    nifty50_ohlc = get_nifty50_data(period="1d")  # Fetch data for 1 day
    if not nifty50_ohlc.empty:
        prev_close = get_previous_day_close(nifty50_ohlc)
        return nifty50_ohlc.iloc[-1]['Close'], prev_close
    else:
        return None, None  # Handle the case when data is not available

previous_day_close = get_previous_day_close(get_nifty50_data())
today_close = get_today_close()
day_change_sign = '+' if Day_Change > 0 else ''
open_change_sign = '+' if Open_Change > 0 else ''
if previous_day_close is not None and today_close is not None:
    close = today_close[0]
    open_price = nifty50_ohlc.iloc[-1]['Open']
    close_color = Fore.GREEN if close > open_price else Fore.RED
else:
    close_color = Fore.YELLOW
# Now you can use nifty50_ohlc outside of the function
print(f"🔆{day_change_sign}{Fore.GREEN if Day_Change >= 0 else Fore.RED}{Day_Change:.2f}{Style.RESET_ALL}⌛{open_change_sign}{Fore.GREEN if Open_Change >= 0 else Fore.RED}{Open_Change:.2f}{Style.RESET_ALL}⚡{Fore.GREEN if nse_power > 0.5 else Fore.RED}{nse_power:.2f}{Style.RESET_ALL}🟥-{pedepth}🚦📈:{close_color}{int(today_close[0])}{macd}🚦{cedepth}+🟩")
