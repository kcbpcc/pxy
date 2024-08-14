import warnings
import yfinance as yf
import pandas as pd
from rich.console import Console
from colorama import Fore, Style, init
from depthpxy import calculate_consecutive_candles
from macdpxy import calculate_macd_signal
from smapxy import check_index_status

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

def fetch_data(symbol):
    data = yf.Ticker(symbol).history(period="5d", interval="1m")
    return data

def calculate_heikin_ashi_colors(data):
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    colors = ['🟥' if ha_close.iloc[-i] < ha_open.iloc[-i] else '🟩' for i in range(1, min(4, len(ha_close) + 1))][::-1]

    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'

    candle_sequence = f'{"".join(colors)}'
    return candle_sequence, current_color, last_closed_color

def calculate_last_twenty_heikin_ashi_colors(symbol):
    data = fetch_data(symbol)
    return calculate_heikin_ashi_colors(data)

def get_market_check(symbol):
    candle_sequence, current_color, last_closed_color = calculate_last_twenty_heikin_ashi_colors(symbol)

    if current_color == 'Bear' and last_closed_color == 'Bear':
        market_signal = 'Bear'
    elif current_color == 'Bull' and last_closed_color == 'Bull':
        market_signal = 'Bull'
    elif current_color == 'Bear' and last_closed_color == 'Bull':
        market_signal = 'Sell'
    elif current_color == 'Bull' and last_closed_color == 'Bear':
        market_signal = 'Buy'
    else:
        market_signal = 'None'

    return candle_sequence, market_signal

def get_stock_action(ticker):
    ha_action = None
    stock_power = 0.0
    day_change = 0.0
    open_change = 0.0

    try:
        data = yf.Ticker(ticker).history(period="5d")

        today_open = data['Open'].iloc[-1]
        today_high = data['High'].iloc[-1]
        today_low = data['Low'].iloc[-1]
        current_price = data['Close'].iloc[-1]

        yesterday_close = data['Close'].iloc[-2]
        yesterday_open = data['Open'].iloc[-2']

        raw_stock_power = (current_price - (today_low - 0.01)) / (abs(today_high + 0.01) - abs(today_low - 0.01))
        stock_power = round(max(0.1, min(raw_stock_power, 1.0)), 2)
        day_change = round(((current_price - yesterday_close) / yesterday_close) * 100, 2)
        open_change = round(((current_price - today_open) / today_open) * 100, 2)

        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

        ha_action = "Bullish" if ha_close.iloc[-1] > ha_open.iloc[-1] else "Bearish"

    except Exception as e:
        pass

    return ha_action, stock_power, day_change, open_change

ticker_symbol = '^NSEI'
ha_action, stock_power, day_change, open_change = get_stock_action(ticker_symbol)

print(f"Ticker: {ticker_symbol}")
print(f"Heikin-Ashi Action: {ha_action}")
print(f"Stock Power: {stock_power}")
print(f"Day Change (%): {day_change}")
print(f"Open Change (%): {open_change}")

candle_sequence, market_signal = get_market_check(ticker_symbol)
print(f"Candle Sequence: {candle_sequence}")
print(f"Market Signal: {market_signal}")

# Additional functions for MACD signal, SMA check, and consecutive candles
def get_macd_signal(symbol):
    return calculate_macd_signal(symbol)

def check_index_trend(symbol):
    return check_index_status(symbol)

def get_consecutive_candles(symbol):
    return calculate_consecutive_candles(symbol)

# Example calls for additional functions
macd_signal = get_macd_signal(ticker_symbol)
index_trend = check_index_trend(ticker_symbol)
consecutive_candles = get_consecutive_candles(ticker_symbol)

print(f"MACD Signal: {macd_signal}")
print(f"Index Trend: {index_trend}")
print(f"Consecutive Candles: {consecutive_candles}")

