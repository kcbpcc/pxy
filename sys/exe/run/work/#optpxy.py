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

# Constants
START_TIME = 223
END_TIME = 245

def fetch_data(symbol):
    # Fetch real-time data for the specified interval and symbol
    data = yf.Ticker(symbol).history(period="5d", interval="1m")
    return data

def calculate_heikin_ashi_colors(data):
    # Calculate Heikin-Ashi candles
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    # Calculate the colors of the last 20 closed candles (oldest to latest)
    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
    # Rich print statement for all 20 candle colors

    return current_color, last_closed_color

def calculate_last_twenty_heikin_ashi_colors(symbol):
    # Check if the current time is within the specified time range (3:45 AM to 4:00 AM UTC)
    current_utc_time = time.gmtime().tm_hour * 60 + time.gmtime().tm_min

    if START_TIME <= current_utc_time < END_TIME:
        # Download data for the specified number of days (fixed to 20 days) with a 1-minute interval
        data = yf.Ticker(symbol).history(period="5d", interval="5m")
    else:
        data = fetch_data(symbol)

    return calculate_heikin_ashi_colors(data)

def get_opt_check(symbol):
    # Call the function calculate_last_twenty_heikin_ashi_colors to get colors
    current_color, last_closed_color = calculate_last_twenty_heikin_ashi_colors(symbol)

    # Determine the market check based on the candle colors
    if current_color == 'Bear' and last_closed_color == 'Bear':
        optpxy = 'Bear'
    elif current_color == 'Bull' and last_closed_color == 'Bull':
        optpxy = 'Bull'
    elif current_color == 'Bear' and last_closed_color == 'Bull':
        optpxy = 'Sell'
    elif current_color == 'Bull' and last_closed_color == 'Bear':
        optpxy = 'Buy'
    else:
        optpxy = 'None'

    return optpxy
