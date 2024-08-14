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

def fetch_data(symbol):
    # Fetch real-time data for the specified interval and symbol
    data = yf.Ticker(symbol).history(period="5d", interval="1m")
    return data

def calculate_heikin_ashi_colors(data):
    # Calculate Heikin-Ashi candles
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'

    return current_color, last_closed_color

def get_market_check(symbol):
    # Call the function to get colors
    data = fetch_data(symbol)
    current_color, last_closed_color = calculate_heikin_ashi_colors(data)

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

    return market_signal

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

        yesterday_close = data['Close'].iloc[-2]

        # Calculate stock power
        raw_stock_power = (current_price - (today_low - 0.01)) / (abs(today_high + 0.01) - abs(today_low - 0.01))
        stock_power = round(max(0.1, min(raw_stock_power, 1.0)), 2)
        day_change = round(((current_price - yesterday_close) / yesterday_close) * 100, 2)
        open_change = round(((current_price - today_open) / today_open) * 100, 2)

        # Calculate Heikin-Ashi values
        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2
        
        # Define Heikin-Ashi day candle status
        ha_action = "Bullish" if ha_close.iloc[-1] > ha_open.iloc[-1] else "Bearish"

    except Exception as e:
        # Ignore errors during data download
        pass

    return ha_action, stock_power, day_change, open_change  # Return calculated values

def check_index_status(index_symbol):
    try:
        # Download historical data
        data = yf.Ticker(index_symbol).history(period="5d", interval="1m")

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
    except Exception as e:
        return f"An error occurred: {e}"

def calculate_consecutive_candles(tickerSymbol):
    try:
        # Get data on this ticker
        tickerData = yf.Ticker(tickerSymbol)
        tickerDf = tickerData.history(period='5d', interval='1m')

        # Calculate Heiken Ashi candles
        ha_close = (tickerDf['Open'] + tickerDf['High'] + tickerDf['Low'] + tickerDf['Close']) / 4
        ha_open = ha_close.shift(1)
        ha_color = pd.Series('green', index=ha_close.index)
        ha_color[ha_close < ha_open] = 'red'

        # Calculate consecutive candles sequence
        consecutive_count = 1
        current_color = None

        for i in range(1, len(ha_color)):
            if ha_color[i] == ha_color[i - 1]:
                consecutive_count += 1
            else:
                consecutive_count = 1
                current_color = ha_color[i]

        # Calculate cedepth and pedepth
        if current_color is not None:
            if consecutive_count > 9:
                consecutive_count = 9
            if current_color == 'green':
                cedepth = consecutive_count
                pedepth = 1
            else:
                cedepth = 1
                pedepth = consecutive_count
            return cedepth, pedepth
    except Exception as e:
        return f"An error occurred: {e}"

# Assuming you have a function to get the depth value
depth_value = get_depth_value(ticker_symbol)  # Replace with your actual method

# Print statements with alignment
print(f"{'Ticker:' + ticker_symbol:<{width}}")
print(f"{'Action:' + ha_action:<{width}}")
print(f"{'Power:' + f'{stock_power:.2f}':<{width}}")
print(f"{'Day%:' + f'{day_change:.2f}':<{width}}")
print(f"{'Open%:' + f'{open_change:.2f}':<{width}}")

market_signal = get_market_check(ticker_symbol)
print(f"{'Signal:' + market_signal:<{width}}")

sma = check_index_status(ticker_symbol)
print(f"{'Move:' + sma:<{width}}")

# Print the actual depth value
print(f"{'Depth:':<{width}} {depth_value:>{width}}")

