# Import necessary modules
from rich import print
import sys
import yfinance as yf
import warnings
import pandas as pd

# Set the python3IOENCODING environment variable to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def fetch_data(symbol, period="5d", interval="1m"):
    # Fetch real-time data for the specified interval and symbol
    data = yf.Ticker(symbol).history(period=period, interval=interval)
    return data

def calculate_heikin_ashi_colors(data):
    # Calculate Heikin-Ashi candles
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'

    return current_color, last_closed_color

def get_market_check(current_color, last_closed_color):
    # Determine the market check based on the candle colors
    if current_color == 'Bear' and last_closed_color == 'Bear':
        return 'Bear'
    elif current_color == 'Bull' and last_closed_color == 'Bull':
        return 'Bull'
    elif current_color == 'Bear' and last_closed_color == 'Bull':
        return 'Sell'
    elif current_color == 'Bull' and last_closed_color == 'Bear':
        return 'Buy'
    else:
        return 'None'

def calculate_stock_metrics(data):
    # Extract today's open, yesterday's close, and current price
    today_open = data['Open'].iloc[-1]
    today_high = data['High'].iloc[-1]
    today_low = data['Low'].iloc[-1]
    current_price = data['Close'].iloc[-1]
    yesterday_close = data['Close'].iloc[-2]

    # Calculate stock power
    raw_stock_power = (current_price - (today_low - 0.01)) / (abs(today_high + 0.01) - abs(today_low - 0.01))
    stock_power = round(max(0.1, min(raw_stock_power, 1.0)), 2)
    day_change = round(((current_price - yesterday_close) / yesterday_close) * 100, 2)
    open_change = round(((current_price - today_open) / today_open) * 100, 2)

    return stock_power, day_change, open_change

def get_stock_action(data):
    # Calculate stock metrics
    stock_power, day_change, open_change = calculate_stock_metrics(data)

    # Calculate Heikin-Ashi values
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2
    
    # Define Heikin-Ashi day candle status
    ha_action = "Bullish" if ha_close.iloc[-1] > ha_open.iloc[-1] else "Bearish"

    return ha_action, stock_power, day_change, open_change

def check_index_status(data):
    # Calculate SMA
    data['50SMA'] = data['Close'].rolling(window=50).mean()
    data['200SMA'] = data['Close'].rolling(window=200).mean()

    # Get the last values of SMA and current price
    last_50sma = data['50SMA'].iloc[-1]
    last_200sma = data['200SMA'].iloc[-1]
    current_price = data['Close'].iloc[-1]

    # Check SMA
    if current_price > last_50sma:
        return "Up"
    elif current_price < last_50sma:
        return "Down"
    else:
        return "Side"

def calculate_consecutive_candles(data):
    # Calculate Heikin Ashi candles
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = ha_close.shift(1)
    ha_color = pd.Series('green', index=ha_close.index)
    ha_color[ha_close < ha_open] = 'red'

    # Calculate consecutive candles sequence
    consecutive_count = 1
    current_color = ha_color.iloc[-1]

    for i in range(1, len(ha_color)):
        if ha_color[i] == ha_color[i - 1]:
            consecutive_count += 1
        else:
            consecutive_count = 1
            current_color = ha_color[i]

    # Calculate cedepth and pedepth
    if consecutive_count > 9:
        consecutive_count = 9
    cedepth = consecutive_count if current_color == 'green' else 1
    pedepth = 1 if current_color == 'green' else consecutive_count

    return cedepth, pedepth

def calculate_macd(data):
    # Calculate MACD values
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    
    # Determine if MACD is trending up or down
    macd_trend = "Up" if macd.iloc[-1] > signal.iloc[-1] else "Down"

    return macd_trend

# Define the ticker symbol and width for alignment
ticker_symbol = '^NSEI'  # Replace with actual ticker symbol
width_left = 21  # Adjust width for left-aligned fields
width_right = 21  # Adjust width for right-aligned fields

# Fetch the data once
data = fetch_data(ticker_symbol)

# Calculate all required metrics using the fetched data
ha_action, stock_power, day_change, open_change = get_stock_action(data)
current_color, last_closed_color = calculate_heikin_ashi_colors(data)
market_signal = get_market_check(current_color, last_closed_color)
sma = check_index_status(data)
depth_value, _ = calculate_consecutive_candles(data)
macd_trend = calculate_macd(data)

# Print statements with alignment
print(f"{'MACD:' + macd_trend:<{width_left}}{'Act:' + ha_action:>{width_right}}")
print(f"{'Power:' + f'{stock_power:.2f}':<{width_left}}{'Day%:' + f'{day_change:.2f}':>{width_right}}")
print(f"{'Open%:' + f'{open_change:.2f}':<{width_left}}{'Depth:' + str(depth_value):>{width_right}}")
print(f"{'OnSMA:' + sma:<{width_left}}{'Sign:' + market_signal:>{width_right}}")

