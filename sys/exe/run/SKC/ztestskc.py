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
        print(f"Error fetching stock action data: {e}")

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

from rich.console import Console

# Initialize the console object from rich
console = Console()

# Define the ticker symbol and width for alignment
ticker_symbol = 'AAPL'  # Replace with actual ticker symbol
width_left = 21  # Adjust width for left-aligned fields
width_right = 21  # Adjust width for right-aligned fields

# Get stock action and depth value
ha_action, stock_power, day_change, open_change = get_stock_action(ticker_symbol)
market_signal = get_market_check(ticker_symbol)  # Added definition
sma = check_index_status(ticker_symbol)  # Added definition
depth_value, _ = calculate_consecutive_candles(ticker_symbol)  # Added definition

# Define colors, emojis, and arrows based on context
def get_color_for_value(value, positive_color='green', negative_color='red', default_color='white'):
    if value > 0:
        return positive_color
    elif value < 0:
        return negative_color
    else:
        return default_color

def get_color_for_context(context):
    context_colors = {
        'Bullish': 'green',
        'Bearish': 'red',
        'Up': 'blue',
        'Down': 'yellow',
        'Bull': 'cyan',
        'Bear': 'magenta',
        'Buy': 'green',
        'Sell': 'red',
        'None': 'white',
    }
    return context_colors.get(context, 'white')

def get_emoji_for_context(context):
    context_emojis = {
        'Bullish': '📈',
        'Bearish': '📉',
        'Up': '🔼',
        'Down': '🔽',
        'Bull': '🐂',
        'Bear': '🐻',
        'Buy': '🛒',
        'Sell': '💸',
        'None': '⚪',
    }
    return context_emojis.get(context, '⚪')

def get_arrow_for_value(value):
    if value > 0:
        return '🔼'  # Up arrow
    elif value < 0:
        return '🔽'  # Down arrow
    else:
        return '→'   # Right arrow (no change)

# Colors and emojis for specific values and contexts
power_color = get_color_for_value(stock_power)
day_change_color = get_color_for_value(day_change)
open_change_color = get_color_for_value(open_change)
ha_action_color = get_color_for_context(ha_action)
market_signal_color = get_color_for_context(market_signal)
sma_color = get_color_for_context(sma)

# Arrows for specific numerical values
power_arrow = get_arrow_for_value(stock_power)
day_change_arrow = get_arrow_for_value(day_change)
open_change_arrow = get_arrow_for_value(open_change)

# Print statements with alignment, color, emojis, and arrows
console.print(f"{'Ticker:' + ticker_symbol:<{width_left}}{'Action:' + ha_action + ' ' + ha_action_emoji:>{width_right}}", style='white on black')
console.print(f"{'Power:' + f'{stock_power:.2f}' + ' ' + power_arrow:<{width_left}}{'Day%:' + f'{day_change:.2f}' + ' ' + day_change_arrow:>{width_right}}", style=power_color)
console.print(f"{'Open%:' + f'{open_change:.2f}' + ' ' + open_change_arrow:<{width_left}}{'Signal:' + market_signal + ' ' + market_signal_emoji:>{width_right}}", style=open_change_color)
console.print(f"{'Move:' + sma + ' ' + sma_emoji:<{width_left}}{'Depth:' + str(depth_value):>{width_right}}", style='white on black')
