from rich import print
import sys
import yfinance as yf
import time
import warnings

# Set the python3IOENCODING environment variable to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def fetch_data(symbol, period="5d", interval="5m"):
    # Fetch real-time data for the specified interval
    data = yf.Ticker(symbol).history(period=period, interval=interval)
    return data

def calculate_heikin_ashi_colors(data):
    # Calculate Heikin-Ashi candles
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'

    return current_color, last_closed_color

def is_market_bearish(current_color, last_closed_color):
    return current_color == 'Bear' and last_closed_color == 'Bear'

def is_market_bullish(current_color, last_closed_color):
    return current_color == 'Bull' and last_closed_color == 'Bull'

def is_market_sell(current_color, last_closed_color):
    return current_color == 'Bear' and last_closed_color == 'Bull'

def is_market_buy(current_color, last_closed_color):
    return current_color == 'Bull' and last_closed_color == 'Bear'

def calculate_last_twenty_heikin_ashi_colors(symbol, period="5d", interval="5m"):
    data = fetch_data(symbol, period, interval)
    return calculate_heikin_ashi_colors(data)

def get_market_status(current_color, last_closed_color):
    if is_market_bearish(current_color, last_closed_color):
        return 'Bear'
    elif is_market_bullish(current_color, last_closed_color):
        return 'Bull'
    elif is_market_sell(current_color, last_closed_color):
        return 'Sell'
    elif is_market_buy(current_color, last_closed_color):
        return 'Buy'
    else:
        return 'None'

def get_market_status_for_symbol(symbol, period="5d", interval="5m"):
    current_color, last_closed_color = calculate_last_twenty_heikin_ashi_colors(symbol, period, interval)
    return get_market_status(current_color, last_closed_color)


