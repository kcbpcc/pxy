import yfinance as yf
import pandas as pd

# Define the ticker symbol for Nifty 50
ticker_symbol = "^NSEI"  # Ticker symbol for Nifty 50 index

# Create a Ticker object
nifty_ticker = yf.Ticker(ticker_symbol)

# Fetch one-minute intraday data for the current day
data = nifty_ticker.history(period='1d', interval='1m')

# Calculate MACD
def calculate_macd(data):
    short_window = 12
    long_window = 26

    # Calculate short-term exponential moving average
    short_ema = data['Close'].ewm(span=short_window, min_periods=1, adjust=False).mean()

    # Calculate long-term exponential moving average
    long_ema = data['Close'].ewm(span=long_window, min_periods=1, adjust=False).mean()

    # Calculate MACD line
    macd_line = short_ema - long_ema

    # Calculate signal line
    signal_line = macd_line.ewm(span=9, min_periods=1, adjust=False).mean()

    # Calculate MACD histogram
    macd_histogram = macd_line - signal_line

    return macd_histogram, macd_line

macd_histogram, macd_line = calculate_macd(data)

# Determine if MACD crossed above or below signal line
current_macd_histogram = macd_histogram.iloc[-1]
previous_macd_histogram = macd_histogram.iloc[-2]
current_macd_line = macd_line.iloc[-1]

if previous_macd_histogram < 0 and current_macd_histogram > 0 and current_macd_line > 0:
    print("MACD crossed above signal line while MACD > 0")
    macd = Buy
elif previous_macd_histogram > 0 and current_macd_histogram < 0 and current_macd_line < 0:
    print("MACD crossed below signal line while MACD < 0")
    macd = Sell
else:
    print("No such crossing occurred")

# Now you can use the values of macdbuy and macdsell as needed.

