from rich import print
import sys
import yfinance as yf
import time
import warnings
import logging

# Set the python3IOENCODING environment variable to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Configure logging for better error visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_data(symbol, period="5d", interval="1m"):
    """Fetch historical data for the given symbol."""
    try:
        data = yf.Ticker(symbol).history(period=period, interval=interval)
        if data.empty:
            raise ValueError(f"No data retrieved for symbol {symbol}.")
        return data
    except Exception as e:
        logging.error(f"Error fetching data for {symbol}: {e}")
        return None

def calculate_heikin_ashi_colors(data):
    """Calculate the Heikin-Ashi colors based on historical data."""
    try:
        if data is None or data.empty:
            raise ValueError("Invalid or empty data provided.")

        # Calculate Heikin-Ashi candles
        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

        # Calculate the colors of the last 3 closed candles (oldest to latest)
        colors = ['🟥' if ha_close.iloc[-i] < ha_open.iloc[-i] else '🟩' for i in range(1, min(4, len(ha_close) + 1))][::-1]

        current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
        last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'

        # Return the sequence and status
        candle_sequence = "".join(colors)
        return candle_sequence, current_color, last_closed_color
    except Exception as e:
        logging.error(f"Error calculating Heikin-Ashi colors: {e}")
        return None, None, None

def get_market_check(symbol):
    """Determine market trend based on Heikin-Ashi colors."""
    try:
        data = fetch_data(symbol, period="5d", interval="5m")
        candle_sequence, current_color, last_closed_color = calculate_heikin_ashi_colors(data)

        if not candle_sequence or not current_color or not last_closed_color:
            raise ValueError("Failed to retrieve valid candle colors.")

        # Determine the market signal based on the candle colors
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
    except Exception as e:
        logging.error(f"Error determining market check for {symbol}: {e}")
        return None, None

def get_stock_action(ticker):
    """Analyze the stock action based on Heikin-Ashi and price movements."""
    ha_action = None
    stock_power = 0.0
    day_change = 0.0
    open_change = 0.0

    try:
        # Fetch historical data
        data = fetch_data(ticker, period="5d")

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
        logging.error(f"Error in stock action calculation for {ticker}: {e}")

    return ha_action, stock_power, day_change, open_change

# Example usage
ticker_symbol = '^NSEI'  # You can change this to any valid ticker symbol

# Get stock action analysis
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
