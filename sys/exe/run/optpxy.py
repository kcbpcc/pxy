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

def fetch_data():
    # Fetch real-time data for the specified interval
    data = yf.Ticker('^NSEI').history(period="5d", interval="1m")
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

def calculate_last_twenty_heikin_ashi_colors():
    # Check if the current time is within the specified time range (3:45 AM to 4:00 AM UTC)
    current_utc_time = time.gmtime().tm_hour * 60 + time.gmtime().tm_min

    data = fetch_data()
    return calculate_heikin_ashi_colors(data)
def get_optpxy():
    # Call the function calculate_last_twenty_heikin_ashi_colors to get colors
    current_color, last_closed_color = calculate_last_twenty_heikin_ashi_colors()

    # Determine the market check based on the candle colors
    if is_market_bearish(current_color, last_closed_color):
        optpxy = 'Bear'
    elif is_market_bullish(current_color, last_closed_color):
        optpxy = 'Bull'
    elif is_market_sell(current_color, last_closed_color):
        optpxy = 'Sell'
    elif is_market_buy(current_color, last_closed_color):
        optpxy = 'Buy'
    else:
        optpxy = 'None'

    return optpxy

# Example usage
#optpxy = get_optpxy()

# Print the individual components
#print("Market Status:", optpxy)
