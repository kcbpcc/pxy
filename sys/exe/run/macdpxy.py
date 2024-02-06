import yfinance as yf
import pandas as pd
import numpy as np

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

    return macd_line, signal_line, macd_histogram

macd_line, signal_line, macd_histogram = calculate_macd(data)

# Print MACD values for the current minute
current_minute_macd = macd_histogram.iloc[-1]
print("MACD Histogram for the current minute:", current_minute_macd)
# Print MACD line, signal line, and MACD histogram
print("MACD Line:", macd_line.iloc[-1])
print("Signal Line:", signal_line.iloc[-1])
print("MACD Histogram:", macd_histogram.iloc[-1])
