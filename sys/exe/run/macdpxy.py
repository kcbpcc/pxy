import yfinance as yf
import pandas as pd

def calculate_macd_signal(ticker_symbol):
    # Create a Ticker object
    nifty_ticker = yf.Ticker(ticker_symbol)

    # Fetch one-minute intraday data for the current day
    data = nifty_ticker.history(period='1d', interval='1m')

    # Calculate MACD
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

    # Determine if MACD crossed above or below signal line
    current_macd_histogram = macd_histogram.iloc[-1]
    previous_macd_histogram = macd_histogram.iloc[-2]
    current_macd_line = macd_line.iloc[-1]

    if previous_macd_histogram < 0 and current_macd_histogram > 0 and current_macd_line > 0:
        macd_signal = "⤴"
    elif previous_macd_histogram > 0 and current_macd_histogram < 0 and current_macd_line < 0:
        macd_signal = "⤵"
    else:
        macd_signal = "⤴"

    return macd_signal



