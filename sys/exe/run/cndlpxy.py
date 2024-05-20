import warnings
import yfinance as yf
import pandas as pd
from rich.console import Console
from colorama import Fore, Style, init, deinit
from mktpxy import get_market_check
from utcpxy import peak_time
from macdpxy import calculate_macd_signal
from smapxy import check_index_status
from depthpxy import calculate_consecutive_candles

init(autoreset=True)  # Initialize Colorama

console = Console()

warnings.simplefilter(action='ignore', category=FutureWarning)

OHLC_COLUMNS = ['Open', 'High', 'Low', 'Close']

def get_nifty50_data(period="5d"):
    ticker_symbol = "^NSEI"  # NIFTY50 index symbol on Yahoo Finance
    try:
        nifty_data = yf.Ticker(ticker_symbol).history(period=period)
        ohlc_data = nifty_data[OHLC_COLUMNS]
        return ohlc_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

def get_previous_day_close(df):
    if len(df) >= 2:
        return df.iloc[-2]['Close']
    else:
        return None

def get_today_close():
    nifty50_ohlc = get_nifty50_data(period="1d")
    if not nifty50_ohlc.empty:
        prev_close = get_previous_day_close(nifty50_ohlc)
        return nifty50_ohlc.iloc[-1]['Close'], prev_close
    else:
        return None, None

def dayprinter(o, h, l, c, prev_close):
    max_total_length = 42
    try:
        candle_length = h - l
        if c > o:
            n = round(((o - l) / candle_length) * 100)
            x = round(((c - o) / candle_length) * 100)
            m = 100 - n - x
        else:
            n = round(((c - l) / candle_length) * 100)
            x = round(((o - c) / candle_length) * 100)
            m = 100 - n - x
        
        n_length = round((n / 100) * max_total_length)
        x_length = round((x / 100) * max_total_length)
        m_length = max_total_length - n_length - x_length
        
        print(Fore.LIGHTBLACK_EX + '█' * n_length, end='')
        if c > o:
            print(Fore.GREEN + '█' * x_length + Style.RESET_ALL, end='')
        elif o > c:
            print(Fore.RED + '█' * x_length + Style.RESET_ALL, end='')
        print(Fore.LIGHTBLACK_EX + '█' * m_length)
    
    except Exception as e:
        pass

def option_to_trade():
    today_data = get_nifty50_data().iloc[-1][OHLC_COLUMNS]
    today_close = today_data['Close']
    option_value = round(today_close / 50) * 50
    return option_value

previous_day_close = get_previous_day_close(get_nifty50_data())
today_close = get_today_close()

if previous_day_close is not None and today_close is not None:
    nifty50_ohlc = get_nifty50_data(period="1d")
    today_data = nifty50_ohlc.iloc[-1][OHLC_COLUMNS]
    dayprinter(*today_data, previous_day_close)
else:
    print("Unable to fetch data.")

if previous_day_close is not None and today_close is not None:
    close = today_close[0]
    open_price = nifty50_ohlc.iloc[-1]['Open']
    close_color = Fore.GREEN if close > open_price else Fore.RED
else:
    close_color = Fore.YELLOW

deinit()  # Reset Colorama settings


