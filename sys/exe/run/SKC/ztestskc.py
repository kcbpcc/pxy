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

# Constants for market check time
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

    # Calculate the colors of the last 3 closed candles (oldest to latest)
    colors = ['🟥' if ha_close.iloc[-i] < ha_open.iloc[-i] else '🟩' for i in range(1, min(4, len(ha_close) + 1))][::-1]

    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'

    # Rich print statement for all candle colors
    candle_sequence = f'{"".join(colors)}'
    return candle_sequence, current_color, last_closed_color

def calculate_last_twenty_heikin_ashi_colors(symbol):
    # Check if the current time is within the specified time range (3:45 AM to 4:00 AM UTC)
    current_utc_time = time.gmtime().tm_hour * 60 + time.gmtime().tm_min

    if START_TIME <= current_utc_time < END_TIME:
        # Download data for the specified number of days (fixed to 20 days) with a 5-minute interval
        data = yf.Ticker(symbol).history(period="5d", interval="5m")
    else:
        data = fetch_data(symbol)

    return calculate_heikin_ashi_colors(data)

def get_market_check(symbol):
    # Call the function calculate_last_twenty_heikin_ashi_colors to get colors
    candle_sequence, current_color, last_closed_color = calculate_last_twenty_heikin_ashi_colors(symbol)

    # Determine the market check based on the candle colors
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
        # Download data for a fixed 5-day period
        data = yf.Ticker(ticker).history(period="5d")

        # Extract today's open, yesterday's close, and current price
        today_open = data['Open'].iloc[-1]
        today_high = data['High'].iloc[-1]
        today_low = data['Low'].iloc[-1]
        current_price = data['Close'].iloc[-1]

        today_average = (today_open + today_high + today_low + current_price) / 4
        
        yesterday_close = data['Close'].iloc[-2]
        yesterday_open = data['Open'].iloc[-2]

        yesterday_average = (yesterday_close + yesterday_open + today_open) / 3
        
        # Calculate stock power
        raw_stock_power = (current_price - (today_low - 0.01)) / (abs(today_high + 0.01) - abs(today_low - 0.01))
        stock_power = round(max(0.1, min(raw_stock_power, 1.0)), 2)
        day_change = round(((current_price - yesterday_close) / yesterday_close) * 100, 2)
        open_change = round(((current_price - today_open) / today_open) * 100, 2)

        # Calculate Heikin-Ashi values
        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2
        ha_high = data[['High', 'Open', 'Close']].max(axis=1)
        ha_low = data[['Low', 'Open', 'Close']].min(axis=1)
        
        # Define Heikin-Ashi day candle status
        ha_action = "Bullish" if ha_close.iloc[-1] > ha_open.iloc[-1] else "Bearish"

    except Exception as e:
        # Ignore errors during data download
        pass

    return ha_action, stock_power, day_change, open_change  # Return calculated values

# Call the function with the ticker as an argument
ticker_symbol = '^NSEI'  # You can change this to any valid ticker symbol
ha_action, stock_power, day_change, open_change = get_stock_action(ticker_symbol)

# Print the results for stock action
print(f"Ticker: {ticker_symbol}")
print(f"Heikin-Ashi Action: {ha_action}")
print(f"Stock Power: {stock_power}")
print(f"Day Change (%): {day_change}")
print(f"Open Change (%): {open_change}")

# Call the market check function and print the candle sequence and market signal
candle_sequence, market_signal = get_market_check(ticker_symbol)
print(f"Candle Sequence: {candle_sequence}")
print(f"Market Signal: {market_signal}")
